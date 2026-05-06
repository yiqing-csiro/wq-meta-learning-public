import os
import re
import argparse
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import KFold


torch.manual_seed(42)
np.random.seed(42)

CKPT_PATH = "models/base_model.pt"
HIDDEN_DIM = 1024
EPS_POS = 1e-16

OUT_DIR = "outputs"
MAX_STEPS = 10
N_FOLDS = 10
LR = 1e-4

os.makedirs(OUT_DIR, exist_ok=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)


class RegressionModel(nn.Module):

    def __init__(self, input_dim, hidden_dim=1024, output_dim=3):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x):
        return self.net(x)


def compute_metrics(pred, true, eps=EPS_POS):

    mask = (~np.isnan(pred)) & (~np.isnan(true))

    pred = pred[mask]
    true = true[mask]

    if len(pred) == 0:
        print("WARNING: no valid samples for metrics")
        return np.nan, np.nan

    d = np.log10(np.maximum(pred, eps)) - np.log10(np.maximum(true, eps))

    rmse = 10 ** (np.sqrt(np.mean(d ** 2)))
    mae = 10 ** (np.mean(np.abs(d)))

    return rmse, mae


def run_dataset(csv_path, result_name, focus_channel):

    print("Processing:", csv_path)

    df = pd.read_csv(csv_path)

    input_cols = [
        c for c in df.columns
        if re.match(r"^\d+", c) and 400 <= int(re.match(r"^\d+", c).group()) <= 700
    ]

    output_cols = ["TSS (mg/L)", "DOC (mg/L)", "Chl (ug/L)"]

    X = df[input_cols].values.astype(np.float32)
    y = df[output_cols[focus_channel]].values.astype(np.float32)

    # remove NaN rows
    mask = ~np.isnan(y)
    X = X[mask]
    y = y[mask]

    print("Valid samples:", len(y))

    kf = KFold(n_splits=N_FOLDS, shuffle=True, random_state=42)

    preds = np.zeros_like(y)

    for fold, (train_idx, val_idx) in enumerate(kf.split(X)):

        print(f"\nFold {fold+1}/{N_FOLDS}")

        X_train = torch.tensor(X[train_idx], device=device)
        y_train = torch.tensor(y[train_idx], device=device).unsqueeze(1)

        X_val = torch.tensor(X[val_idx], device=device)
        y_val = torch.tensor(y[val_idx], device=device).unsqueeze(1)

        # normalization
        X_mu = X_train.mean(0, keepdim=True)
        X_std = X_train.std(0, keepdim=True).clamp_min(1e-6)

        X_train = (X_train - X_mu) / X_std
        X_val = (X_val - X_mu) / X_std

        y_mu = y_train.mean(0, keepdim=True)
        y_std = y_train.std(0, keepdim=True).clamp_min(1e-6)

        y_train = (y_train - y_mu) / y_std

        # load model
        model = RegressionModel(len(input_cols), HIDDEN_DIM, 1).to(device)

        state = torch.load(CKPT_PATH, map_location=device)

        # remove final layer
        state = {k: v for k, v in state.items() if not k.startswith("net.6")}

        model.load_state_dict(state, strict=False)

        optimizer = torch.optim.Adam(model.parameters(), lr=LR)
        loss_fn = nn.MSELoss()

        model.train()

        for _ in range(MAX_STEPS):

            optimizer.zero_grad()

            pred = model(X_train)

            loss = loss_fn(pred, y_train)

            loss.backward()
            optimizer.step()

        model.eval()

        with torch.no_grad():
            pred_val = model(X_val)

        pred_val = (pred_val * y_std + y_mu).cpu().numpy().flatten()

        preds[val_idx] = pred_val

    rmse, mae = compute_metrics(preds, y)

    name = output_cols[focus_channel]

    print(f"{name}: RMSE={rmse:.2f} MAE={mae:.2f}")

    save_path = os.path.join(OUT_DIR, f"{result_name}.csv")

    pd.DataFrame({
        "true": y,
        "pred": preds
    }).to_csv(save_path, index=False)

    print("Saved:", save_path)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data_dir",
        type=str,
        required=True,
        help="Directory containing Lucinda CSV datasets",
    )

    args = parser.parse_args()

    data_dir = args.data_dir

    lucinda_tasks = [
        ("lucinda_jetty_tss.csv", "lucinda_jetty_results_tss", 0),
        ("lucinda_jetty_doc.csv", "lucinda_jetty_results_doc", 1),
        ("lucinda_jetty_chl.csv", "lucinda_jetty_results_chl", 2),
    ]

    for file_name, result_name, channel in lucinda_tasks:

        run_dataset(
            os.path.join(data_dir, file_name),
            result_name,
            focus_channel=channel,
        )


if __name__ == "__main__":
    main()