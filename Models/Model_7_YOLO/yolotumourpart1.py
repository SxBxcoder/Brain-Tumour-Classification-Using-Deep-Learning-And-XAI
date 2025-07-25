# -*- coding: utf-8 -*-
"""YOLOtumourpart1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nBxsRADyxhEHzmMiJEW537DSrdZrXm5O
"""

#Install and import Ultralytics YOLO
!pip install ultralytics --quiet

from ultralytics import YOLO
import os
import zipfile
import shutil
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import yaml

from google.colab import files
files.upload()  # Upload kaggle.json

!mkdir -p ~/.kaggle
!mv kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d masoudnickparvar/brain-tumor-mri-dataset

with zipfile.ZipFile("brain-tumor-mri-dataset.zip", 'r') as zip_ref:
    zip_ref.extractall("/content/brain_tumor_data")

#Convert classification data to YOLOv8 detection format (fake boxes)
import cv2

def create_fake_box(img_path):
    img = cv2.imread(img_path)
    h, w, _ = img.shape
    #Simulate a bounding box in the center
    box_w, box_h = w // 2, h // 2
    x_center = w // 2
    y_center = h // 2

    #Normalize
    x_center /= w
    y_center /= h
    box_w /= w
    box_h /= h
    return [x_center, y_center, box_w, box_h]

#Organize dataset for YOLO
classes = ['glioma', 'meningioma', 'notumor', 'pituitary']
class_to_id = {name: idx for idx, name in enumerate(classes)}

#Preparing directory structure
for split in ['train', 'val']:
    os.makedirs(f'dataset/images/{split}', exist_ok=True)
    os.makedirs(f'dataset/labels/{split}', exist_ok=True)

base_path = '/content/brain_tumor_data/Training'
split_ratio = 0.8

for class_name in classes:
    img_dir = os.path.join(base_path, class_name)
    imgs = os.listdir(img_dir)
    random.shuffle(imgs)
    split = int(len(imgs) * split_ratio)
    train_imgs = imgs[:split]
    val_imgs = imgs[split:]

    for phase, phase_imgs in zip(['train', 'val'], [train_imgs, val_imgs]):
        for img_name in phase_imgs:
            img_path = os.path.join(img_dir, img_name)
            dest_img_path = f'dataset/images/{phase}/{class_name}_{img_name}'
            shutil.copy(img_path, dest_img_path)

            #Writing fake label for detection
            box = create_fake_box(img_path)
            label_file = img_name.replace('.jpg', '.txt').replace('.png', '.txt')
            label_path = f'dataset/labels/{phase}/{class_name}_{label_file}'
            with open(label_path, 'w') as f:
                f.write(f"{class_to_id[class_name]} {' '.join(map(str, box))}\n")

#Create YAML config for YOLO
yaml_dict = {
    'path': '/content/dataset',
    'train': 'images/train',
    'val': 'images/val',
    'names': classes
}

with open('/content/dataset/data.yaml', 'w') as outfile:
    yaml.dump(yaml_dict, outfile)

#Train YOLOv8n model
model = YOLO('yolov8n.pt')
model.train(data='/content/dataset/data.yaml', epochs=10, imgsz=150)

metrics = model.val()

print(f"mAP@0.5: {metrics.box.map50:.4f}")
print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
print(f"Precision (mean): {metrics.box.mp:.4f}")
print(f"Recall (mean): {metrics.box.mr:.4f}")

#Run prediction on one image
import glob
import random

#Automatically pick a real validation image
val_images = glob.glob('/content/dataset/images/val/*.jpg') + glob.glob('/content/dataset/images/val/*.png')
test_image_path = random.choice(val_images)

results = model.predict(source=test_image_path, save=True)

#Display predicted image
from IPython.display import Image as IPyImage, display
import glob

predicted_img = glob.glob('runs/detect/*/*.jpg')[-1]
display(IPyImage(predicted_img))