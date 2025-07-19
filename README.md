🧠 Brain Tumour Classification & Prognosis Using Deep Learning and Explainable AI

This repository presents the culmination of my Summer Research Internship at IIT Kharagpur under the mentorship of Prof. Aritra Hazra, focused on developing AI-driven tools for brain tumour analysis through deep learning and explainability.

📌 Abstract

This research aimed to develop an AI-driven framework for classifying brain tumours using deep learning, while focusing on explainability for clinical transparency. Seven models—ranging from CNN classifiers to YOLO-based object detectors—were trained on multiple public MRI datasets. Key tasks included tumour classification, grading, onset prediction, and progression estimation. LIME and SHAP were used to provide interpretability to the models. The final model using the UPENN GBM dataset introduced a novel approach to temporal tumour prognosis.

🙏 Acknowledgment

I express my deepest gratitude to Prof. Aritra Hazra, Department of Computer Science and Engineering, IIT Kharagpur, for his invaluable mentorship. I also thank open-source contributors for their datasets.

📚 Table of Contents

Introduction

Problem Statement

Literature Review

Datasets Used

Methodology

Results and Evaluation

Discussion and Insights

Challenges Faced

Conclusion and Future Scope

References

Appendix

1. 🧠 Introduction

Early and accurate brain tumour diagnosis is critical for patient outcomes. This project leverages CNNs and YOLO to classify tumours and adds explainable AI (XAI) for trustworthy model decisions. We also tackle the novel problem of predicting tumour onset and progression using longitudinal MRI data.

2. 🎯 Problem Statement

Classify brain tumours from MRI scans.

Differentiate tumour types and grades.

Predict approximate onset of tumour.

Estimate risk of progression or deterioration.

Apply LIME/SHAP for explainability.

Implement YOLO for real-time detection.

Explore transfer learning on histopathology data.

3. 📖 Literature Review

Shift from traditional classifiers (Naïve Bayes, SVM) → CNNs.

Adoption of YOLOv5 in medical detection.

XAI models (LIME, SHAP) are increasingly vital for clinical use.

Few studies address temporal modelling of tumours.

Key References:

BMC, PMC, Elsevier, Springer papers on tumour classification

YOLOv5 GitHub: https://github.com/ultralytics/yolov5

SHAP: Lundberg et al.

LIME: Ribeiro et al.

4. 📁 Datasets Used

Dataset

Description

Dataset A

Masoud Nickparvar MRI Dataset (Kaggle) – 7022 images, 4 classes

Dataset B

BTD-600 (Kaggle) – 600 binary MRI scans

Dataset C

UCSF-PDGM – Graded gliomas (Grade II/III/IV)

Dataset D

Breast Histopathology – 277k histopathology images

Dataset E

UPENN-GBM – Longitudinal MRI for temporal modelling

5. ⚙️ Methodology

🧼 Data Preprocessing

Image resizing, scaling, and augmentation

Custom pipelines for temporal MRI alignment

🏗 Model Architectures

Model 1: 4-class tumour classifier (Dataset A)

Model 2: Benign vs Malignant (Dataset B)

Model 3: Glioma grading (Dataset C)

Model 4: Transfer learning for IDC histology (Dataset D)

Model 5: Tumour onset & deterioration prediction using 3D CNNs (Dataset E)

Model 6: CNN + LIME/SHAP (Dataset A)

Model 7: YOLOv5 for bounding box tumour detection

🧠 Explainable AI

LIME: Superpixel masking and heatmaps

SHAP: Global pixel importance using Deep SHAP

Combined insights validated model trustworthiness

6. 📊 Results and Evaluation

Model

Task

Key Metric(s)

Outcome

1

4-class classification

Accuracy

~94%

2

Benign vs Malignant

Accuracy

High (Exact not noted)

3

Glioma Grading

Confusion Matrix

Misclassifications between III & IV

4

IDC detection

Accuracy

~87% (10 epochs)

5

Tumour Onset & Deterioration

MAE, Accuracy

MAE for onset; classifier for deterioration (Preliminary)

6

XAI-enhanced CNN

Accuracy

~94%; Clear LIME & SHAP heatmaps

7

YOLO Detection

mAP@0.5

0.9800





Precision

0.9189





Recall

0.9556

7. 💡 Discussion and Insights

CNNs are effective for tumour type and grade prediction.

Model 5’s temporal approach introduces early prediction potential.

YOLO achieves near real-time detection.

XAI tools confirm medically relevant decisions.

8. ⚠️ Challenges Faced

Limited annotated data for onset/progression.

Complex temporal alignment of MRI sequences.

Manual annotations for YOLO.

High compute needs for 3D CNNs and SHAP.

9. 🚀 Conclusion and Future Scope

This research demonstrates:

Viable AI models for brain tumour classification & detection.

Explainability is essential for clinical adoption.

First steps into temporal tumour modelling (Model 5).

Future directions:

Explore transformer-based models.

Integrate patient metadata.

Build deployable diagnostic tools.

Collaborate with radiologists for clinical validation.

10. 📚 References

See the full list in the final PDF report or source citations:

Masoud Nickparvar (Kaggle)

SRINIVASBECE (Kaggle)

UCSF-PDGM, UPENN-GBM (TCIA)

YOLOv5 GitHub, SHAP, LIME papers

11. 📎 Appendix

Full Report: 📄 Final_Report.pdfRepository: 🔗 GitHub Project Link

This project showcases a fusion of AI and healthcare with a strong emphasis on model trust, transparency, and real-world diagnostic value.
