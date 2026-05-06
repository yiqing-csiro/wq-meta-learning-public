<div align="center">

# Region-adaptable water quality retrieval from in situ hyperspectral data using physics-aware meta-learning

</div>

## ✨ Introduction

Hyperspectral in situ sensing has shown promise in retrieving aquatic biogeochemical (BGC) parameters, such as total suspended solids, dissolved organic carbon, and total chlorophyll-a, for cost-effective monitoring of coastal water quality. However, generalising such retrieval algorithms across water bodies remains challenging, as the relationship between remote sensing reflectance ($R_{rs}$) and BGC parameters can vary considerably from one region to another due to regional distinctions in environmental conditions and biogeochemistry that lead to different BGC ranges and bio-optical properties. In this study, we propose a two-stage physics-aware meta-learning framework for retrieving coastal BGC parameters from near-surface $R_{rs}$ observations. In the first stage, a bio-optical forward model is used to generate a large synthetic dataset based on an in situ bio-optical spectral library with broad representativeness of Australian coastal waters. This dataset is then used to pretrain a region-agnostic base model with meta-learning, allowing the model to learn fundamental physical relationships. In the second stage, the pretrained base model is fine-tuned for specific regions with local samples. To evaluate the proposed approach, we collected in situ hyperspectral $R_{rs}$ and BGC measurements from five geographically distinct sites in Australian coastal waters. Our experimental results suggest the following: (1) the BGC parameters and their corresponding hyperspectral $R_{rs}$ signatures exhibited clear regional distinctions among the experimental sites; (2) the synthetic dataset, generated under guidance of the bio-optical forward model and the bio-optical spectral library, was physically plausible and closely aligned with real-world samples in both parameter distributions and inter-parameter correlations; (3) benefiting from its physics-aware pretraining and region-adaptable fine-tuning, the proposed approach outperformed five benchmark models in BGC retrieval; and (4) time series of in situ measured and model-predicted BGC parameters showed good agreement in both magnitude and temporal dynamics, highlighting the potential of in situ hyperspectral sensing as a cost-effective solution for continuous time-series monitoring of coastal water quality. These results demonstrate that the proposed physics-aware meta-learning framework provides a robust and adaptable approach for accurate BGC retrieval across diverse coastal environments using hyperspectral in situ sensing.

![](figures/graphic.jpg)

## 🎬 Sildes

Please see the slides below for an explanation of this work.

[Slides](https://yiqing-csiro.github.io/wq-meta-learning-public/slides/)

## 📢 News

[2026-03] The preprint manuscript is now available on arXiv.

[2026-03] The demo code is released; The pretrained model is available at ./models/ ; The demo datasets are available at ./datasets/ .

## 📈 Usage

- Create conda environment with python:

```
conda create --name wqmeta python=3.12.3
conda activate wqmeta
```

- Install required packages:

```
pip install -r requirements.txt
```

- Run the demo code:

```
python demo_run.py --data_dir datasets
```

The outputs will be stored in the ./outputs/ folder.

## 📝 Citation

If you find this repo or our work useful for your research, please consider citing the paper:

```tex
@article{guo2026region,
  title={Region-adaptable water quality retrieval from in situ hyperspectral data using physics-aware meta-learning},
  author={Guo, Yiqing and Cherukuru Nagur and Lehmann, Eric and Unnithan, S. L. Kesav and Malthus Tim and
Kerrisk, Gemma and Qi, Xiubin and Islam, Faisal and Dhar Tisham},
  journal={},
  year={2026}
}
```

## 🙏 Acknowledgements

The authors would like to sincerely thank the following organisations and services for their support to this work: Commonwealth Scientific and Industrial Research Organisation (CSIRO) AquaWatch Australia Mission, CSIRO AI4Missions, South Australian Research and Development Institute (SARDI), CSIRO Data61, CSIRO Environment, CSIRO Space and Astronomy, CSIRO Earth Analytics Science and Innovation (EASI) platform, and CSIRO AquaWatch Data Service (ADS). 

The authors would like to acknowledge the in situ data from Lucinda Jetty Coastal Observatory (Principal Investigator: Dr Thomas Schroeder with CSIRO Environment). These data were sourced from Australia’s Integrated Marine Observing System (IMOS). IMOS is enabled by the National Collaborative Research Infrastructure Strategy (NCRIS). It is operated by a consortium of institutions as an unincorporated joint venture, with the University of Tasmania as Lead Agent.

We acknowledge the SARDI field team (Mr Ian Moody and Mr Paul Malthouse) for their help with Boston Bay buoy setup and maintenance. Thanks also go to CSIRO's EASI team for their guidance on the ADS platform, and Ms Florina Richard with CSIRO Environment and Dr Foivos Diakogiannis with CSIRO Data61 for helpful discussions. We are grateful to Dr Albertina Dias with CSIRO Hydrochemistry Laboratories, Hobart, Tasmania, for analysing the grab water samples.

While preparing this manuscript, the authors used Generative AI to improve language clarity and readability. All AI-generated suggestions were carefully reviewed and edited as necessary, and the authors take full responsibility for the final content of the publication.

## 📪 Contact

If you have any question, please contact [yiqing.guo@csiro.au]().
