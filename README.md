<h1 align="center">🧠 Brain Tumor Classification using Deep Learning and Explainable AI</h1>

<p align="center">
  <em>Latency-aware modeling • Glioma grading • Tumor onset prediction • XAI with SHAP & LIME • YOLOv5</em>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/SxBxcoder/Brain-Tumour-Classification-Using-Deep-Learning-And-XAI/refs/heads/main/assets/%E2%80%94Pngtree%E2%80%94high-tech%20artificial%20intelligence%20digital%20brain_16429714.jpg" alt="Brain Tumor Deep Learning Project Banner" width="80%" />
</p>

---

## 🔬 **Abstract**
> This research internship aimed to develop an AI-driven framework for classifying brain tumours using deep learning, while also focusing on **explainability** to ensure clinical transparency.  
>
> ✅ Built **7 CNN models** for tasks like tumour detection, grading, onset estimation, and deterioration prediction  
> ✅ Utilized **LIME** and **SHAP** for explainable AI
> ✅ Object detection architectures such as YOLO (You Only Look Once) have been used to localise and classify anomalies in medical images in real-time.
> ✅ Worked with top datasets like **UPENN-GBM**, **UCSF-PDGM**, etc.  
> ✅ Developed a unique temporal model to estimate **glioblastoma progression**

---

## 📁 **Table of Contents**
1. [Introduction](#introduction)
2. [Problem Statement](#problem-statement)
3. [Literature Review](#literature-review)
4. [Datasets Used](#datasets-used)
5. [Methodology](#methodology)
6. [Results & Evaluation](#results--evaluation)
7. [Discussion & Insights](#discussion--insights)
8. [Challenges Faced](#challenges-faced)
9. [Conclusion & Future Scope](#conclusion--future-scope)
10. [References](#references)
11. [Appendix](#appendix)

---

## 📌 __**Introduction**__

Brain tumour detection is a critical challenge in medical diagnostics. The ability to automate tumour classification using **non-invasive imaging** like MRI improves early diagnosis and treatment. This project applies **Convolutional Neural Networks (CNNs)** to detect and classify tumours, enhanced by **Explainable AI** methods (SHAP, LIME) and **temporal modelling** to track progression.

---

## 🎯 __**Problem Statement**__

- 🔹 Build DL classifiers for tumour detection & classification  
- 🔹 Distinguish between multiple tumour types and grades  
- 🔹 Predict approximate **tumour onset**  
- 🔹 Forecast **deterioration risk**  
- 🔹 Enhance **transparency** with explainable AI (SHAP, LIME)  
- 🔹 Enable **transfer learning** for broader histopathological analysis

---

## 📚 __**Literature Review**__

Recent works show a transition from classical ML (Naive Bayes, SVM) to CNNs for medical imaging.  
Notable tools and findings:

- **YOLOv5** for tumour localization  
- **Hybrid deep learning + XAI** for transparency  
- Surveys from **MDPI**, **IEEE**, and **Elsevier** highlight trends in AI-driven neurodiagnostics

📖 _Key References_:
- [Hybrid Explainable Model for Brain Tumour Classification (2023)](https://bmcmedinformdecismak.biomedcentral.com/articles/10.1186/s12911-023-02114-6)  
- [Performance Evaluation of CNN Models (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10453020/)  
- [Deep Learning Tumour Classification Survey (2024)](https://www.sciencedirect.com/science/article/pii/S1746809424008322)  

---

📊 Datasets Used
<details> <summary><strong>🧠 Dataset A — Brain Tumor MRI (Kaggle)</strong></summary>
Use Case: Multiclass Tumor Classification

Images: 7022 T1-weighted contrast-enhanced MRIs

Classes: Glioma, Meningioma, Pituitary Tumor, No Tumor

Structure: Organized folder-wise, ideal for CNNs

Link: 🔗 Brain Tumor MRI Dataset

</details> <details> <summary><strong>🔍 Dataset B — Brain Tumor Database BTD-600 (Kaggle)</strong></summary>
Use Case: Binary Classification (Benign vs Malignant)

Images: 600 real-world MRI scans

Challenge: Requires augmentation & regularization due to small size

Link: 🔗 Brain Tumor BTD-600

</details> <details> <summary><strong>🏥 Dataset C — UCSF-PDGM (TCIA)</strong></summary>
Use Case: Glioma Grading

Modality: FLAIR, T1, T2

Labels: WHO Grades II, III, IV

Source: Preoperative Diffuse Glioma MRIs

Link: 🔗 UCSF-PDGM Dataset

</details> <details> <summary><strong>🧬 Dataset D — Breast Histopathology Images (Kaggle)</strong></summary>
Use Case: Binary IDC Detection via Transfer Learning

Images: 277,524 image patches

Classes: Invasive Ductal Carcinoma (0 or 1)

Note: RGB histology images, not MRI

Link: 🔗 Breast Histopathology Dataset

</details> <details> <summary><strong>🧪 Dataset E — UPENN-GBM (TCIA)</strong></summary>
Use Case: Tumor Onset Estimation & Progression Forecasting

Type: Longitudinal GBM MRIs (multiple time points)

Labels: Tumor progression & deterioration over time

Link: 🔗 UPENN-GBM Dataset

</details>

---

## 🧠 __**Methodology**__

### 🧹 **Preprocessing:**
- NIfTI & `.mat` formats
- Histogram equalization, resizing
- Masking, border extraction

### 🧠 **CNN Architectures:**
- 3D CNNs & ResNet-50 variations  
- Custom shallow CNN for fast inference  
- Final UPENN-based temporal model

### 💡 **Explainable AI:**
- **LIME:** Local Interpretable Model-agnostic Explanations  
- **SHAP:** SHapley Additive exPlanations  

![XAI Image](https://miro.medium.com/v2/resize:fit:1400/1*tPrfVu8YEdBMFvDYKPMgDQ.png)

---

## 🧠 Models Implemented

All the model architectures and training notebooks can be found inside the [Models/](./Models) folder.

Each model includes:
- `.ipynb` notebook with full explanation and outputs
- `.py` script version for production use

📌 **Models Included:**
- Model 1: CNN Classifier
- Model 2: Gaussian Naive Bayes
- Model 3: Glioblastoma grading
- Model 4: Transfer Learning to IDC Detection on Breast histopathology images
- Model 5: Tumour Onset Predictor and Deterioration Estimator
- Model 6: XAI with SHAP & LIME
- Model 7: YOLOv5 Tumor Localization

---

## 📈 __**Results & Evaluation**__

- Achieved up to **94% accuracy** in binary tumour detection  
- Tumour grading model (multi-class) reached reasonable accuracy  
- SHAP/LIME outputs aligned with clinical MRI regions  
- Temporal model predicted GBM deterioration window with high correlation

---

## 🔍 __**Discussion & Insights**__

- Explainable models outperform black-box CNNs in trust and usability  
- Transfer learning greatly reduced training time on small datasets  
- fMRI-based onset prediction remains a novel and promising field  

---

## ⚠️ __**Challenges Faced**__

- GPU & RAM limitations on Google Colab  
- Data imbalance in tumour grading tasks  
- Integrating SHAP for 3D models required advanced wrapper logic
- Lack of required datasets to be used to predict Tumour Onset and its Deterioration

---

## ✅ __**Conclusion & Future Scope**__

This research demonstrates the effectiveness of **XAI-enhanced deep learning** for tumour diagnostics.  
Future directions:
- Expand to **multi-modal data** (clinical + imaging)  
- Extend temporal modelling to other neuro-oncological conditions  
- Deploy web-based diagnostic interface for hospitals

---

## Acknowledgment

This research project was conducted under the mentorship of **Prof. Aritra Hazra**, Department of Computer Science and Engineering, **IIT Kharagpur**.  
I sincerely thank him for his valuable guidance, feedback, and support throughout the internship.

---

## 📎 **Appendix**

- 📄 [📘 Click here to read the Full Research Report (PDF)](./Internship-Report.pdf)

---

## 📌 **How to Cite This Work**

If this project contributes to your research, feel free to cite or acknowledge it via:

```bibtex
@misc{SxBxcoder2025braintumor,
  author       = {Sayandip Bhattacharya},
  title        = {Brain Tumor Classification Using Deep Learning and Explainable AI},
  year         = {2025},
  howpublished = {\url{https://github.com/SxBxcoder/Brain-Tumour-Classification-Using-Deep-Learning-And-XAI}},
  note         = {Summer Research Internship Project, IIT Kharagpur}
}
