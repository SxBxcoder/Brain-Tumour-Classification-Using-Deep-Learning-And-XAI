# -*- coding: utf-8 -*-
"""Tumourpart5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Nm4d2LEGvO5JLbV7QbwXrou-kF6_cGPO
"""

from google.colab import drive
drive.mount('/content/drive')
# Path to your uploaded NBIA download folder
dicom_dir = '/content/drive/MyDrive/UPENN_GBM_Top10'

# Path where converted NIfTI files will go
nifti_output_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'

!pip install dicom2nifti pydicom nibabel

import dicom2nifti
import os
import pydicom

def clean_modality_name(name):
    name = name.upper()
    if 'FLAIR' in name:
        return 'FLAIR'
    if 'T1' in name and ('C' in name or 'CE' in name or 'POST' in name):
        return 'T1CE'
    if 'T1' in name:
        return 'T1'
    if 'T2' in name:
        return 'T2'
    if 'ADC' in name:
        return 'ADC'
    if 'DWI' in name:
        return 'DWI'
    if 'MRS' in name or 'SPECTRO' in name:
        return 'MRS'
    return 'UNKNOWN'

# ✅ Corrected path
base_dir = '/content/drive/MyDrive/UPENN_GBM_Top10/manifest-1669766397961/UPENN-GBM'
output_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'
os.makedirs(output_dir, exist_ok=True)

for patient in os.listdir(base_dir):
    patient_path = os.path.join(base_dir, patient)
    if not os.path.isdir(patient_path):
        continue

    for series_folder in os.listdir(patient_path):
        series_path = os.path.join(patient_path, series_folder)
        if not os.path.isdir(series_path):
            continue

        for sub in os.listdir(series_path):
            sub_path = os.path.join(series_path, sub)
            if not os.path.isdir(sub_path):
                continue

            try:
                dicom_files = [f for f in os.listdir(sub_path) if f.endswith('.dcm')]
                if not dicom_files:
                    continue

                dcm_sample = pydicom.dcmread(os.path.join(sub_path, dicom_files[0]), stop_before_pixels=True)
                modality = clean_modality_name(str(dcm_sample.SeriesDescription))

                nifti_filename = f"{patient}_{modality}_{sub}.nii.gz"
                output_path = os.path.join(output_dir, nifti_filename)

                dicom2nifti.convert_directory(sub_path, output_dir, compression=True, reorient=True)
                print(f"✅ Converted: {patient}/{sub} → {modality}")

            except Exception as e:
                print(f"❌ Failed to convert {sub_path}: {e}")

import os

nifti_output_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'

files = sorted([f for f in os.listdir(nifti_output_dir) if f.endswith('.nii.gz')])

print(f"🧠 Total NIfTI files: {len(files)}")
print("\n".join(files[:10]))  # Show first 10 files

import os
from collections import defaultdict

nifti_output_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'
key_modalities = {"T1", "T1CE", "T2"}

patient_modalities = defaultdict(set)

def identify_modality(name):
    name = name.upper()
    if 'FLAIR' in name:
        return 'FLAIR'
    if 'T1' in name and ('C' in name or 'CE' in name or 'POST' in name or 'STEALTH' in name):
        return 'T1CE'
    if 'T1' in name:
        return 'T1'
    if 'T2' in name:
        return 'T2'
    return 'UNKNOWN'

# Parse all .nii.gz files
for fname in os.listdir(nifti_output_dir):
    if not fname.endswith('.nii.gz'):
        continue
    parts = fname.split('_')
    patient_id = parts[0]
    modality = identify_modality(fname)
    if modality in key_modalities:
        patient_modalities[patient_id].add(modality)

# Keep patients with at least 2 modalities
selected_patients = []
for pid, mods in patient_modalities.items():
    if len(mods) >= 2:
        selected_patients.append((pid, sorted(mods)))

# Output result
print(f"\n✅ Found {len(selected_patients)} patients with at least 2 key modalities:\n")
for pid, mods in selected_patients:
    print(f"🧠 Patient {pid}: {mods}")

import os
import numpy as np
import nibabel as nib
import tensorflow as tf
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from sklearn.model_selection import train_test_split
from collections import defaultdict

# NIfTI file directory
nifti_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'
TARGET_SHAPE = (64, 64, 32)

def identify_modality(filename):
    name = filename.lower()
    if 'stealth' in name or 'post' in name:
        return 'T1CE'
    if 't1' in name:
        return 'T1'
    if 't2' in name:
        return 'T2'
    return 'UNKNOWN'

def load_nifti(path):
    img = nib.load(path).get_fdata()
    img = np.nan_to_num(img)
    return (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-5)

def resize_volume(img, target_shape=TARGET_SHAPE):
    zoom_factors = [t/s for t, s in zip(target_shape, img.shape)]
    return zoom(img, zoom_factors, order=1)

# Group modalities per patient
patient_files = defaultdict(dict)

for fname in os.listdir(nifti_dir):
    if not fname.endswith('.nii.gz'):
        continue
    patient_id = fname.split('_')[0]  # e.g., '14'
    modality = identify_modality(fname)
    if modality in ['T1CE', 'T2']:
        patient_files[patient_id][modality] = os.path.join(nifti_dir, fname)

# Load patients that have both T1CE and T2
X, Y = [], []

for pid, modalities in patient_files.items():
    if 'T1CE' in modalities and 'T2' in modalities:
        try:
            t1ce = resize_volume(load_nifti(modalities['T1CE']))
            t2 = resize_volume(load_nifti(modalities['T2']))
            X.append(t1ce[..., np.newaxis])  # Add channel dim
            Y.append(t2[..., np.newaxis])
            print(f"✅ Loaded Patient {pid}")
        except Exception as e:
            print(f"❌ Error loading {pid}: {e}")

X = np.array(X, dtype=np.float32)
Y = np.array(Y, dtype=np.float32)

# Check and split
if len(X) == 0:
    raise ValueError("❌ No patients found with both T1CE and T2 modalities.")

X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.3, random_state=42)
train_ds = tf.data.Dataset.from_tensor_slices((X_train, Y_train)).shuffle(10).batch(1)
val_ds = tf.data.Dataset.from_tensor_slices((X_val, Y_val)).batch(1)

# ✅ Visualize a sample
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.title("T1CE Input")
plt.imshow(X_train[0][:, :, 16, 0], cmap='gray')  # use middle slice index 16

plt.subplot(1, 2, 2)
plt.title("T2 Target")
plt.imshow(Y_train[0][:, :, 16, 0], cmap='gray')
plt.show()

from tensorflow.keras import layers, models

def build_mini_cnn_3d_fixed():
    inputs = tf.keras.layers.Input(shape=(64, 64, 32, 1))

    x = tf.keras.layers.Conv3D(8, (3,3,3), activation='relu', padding='same')(inputs)
    x = tf.keras.layers.MaxPooling3D((2,2,2))(x)

    x = tf.keras.layers.Conv3D(16, (3,3,3), activation='relu', padding='same')(x)
    x = tf.keras.layers.UpSampling3D((2,2,2))(x)

    x = tf.keras.layers.Conv3D(1, (3,3,3), activation='linear', padding='same')(x)  # <- no sigmoid!

    return tf.keras.models.Model(inputs, x)

model = build_mini_cnn_3d_fixed()
model.compile(optimizer='adam', loss='mae')  # Try MAE instead of MSE

sample_x = X_train[:1]
sample_y = Y_train[:1]

ds = tf.data.Dataset.from_tensor_slices((sample_x, sample_y)).repeat().batch(1)
model.fit(ds, steps_per_epoch=1, epochs=50, verbose=1)

pred = model.predict(sample_x)

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(sample_x[0][:, :, 16, 0], cmap='gray')
plt.title("T1CE")

plt.subplot(1, 3, 2)
plt.imshow(sample_y[0][:, :, 16, 0], cmap='gray')
plt.title("True T2")

plt.subplot(1, 3, 3)
plt.imshow(pred[0][:, :, 16, 0], cmap='gray')
plt.title("Predicted T2")

plt.tight_layout()
plt.show()

import os
import numpy as np
import nibabel as nib
from collections import defaultdict
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt

nifti_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'
TARGET_SHAPE = (128, 128)

def identify_modality(filename):
    name = filename.lower()
    if 'stealth' in name or 'post' in name:
        return 'T1CE'
    if 't2' in name:
        return 'T2'
    return 'UNKNOWN'

def load_nifti(path):
    img = nib.load(path).get_fdata()
    img = np.nan_to_num(img)
    img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-5)
    return img.astype(np.float32)

def resize_2d(slice_2d, target_shape=TARGET_SHAPE):
    from scipy.ndimage import zoom
    zoom_factors = [t / s for t, s in zip(target_shape, slice_2d.shape)]
    return zoom(slice_2d, zoom_factors, order=1)

# Group files
patient_files = defaultdict(dict)

for fname in os.listdir(nifti_dir):
    if not fname.endswith('.nii.gz'):
        continue
    pid = fname.split('_')[0]
    modality = identify_modality(fname)
    if modality in ['T1CE', 'T2']:
        patient_files[pid][modality] = os.path.join(nifti_dir, fname)

# Extract 2D axial slices
X_slices, Y_slices = [], []

for pid, mods in patient_files.items():
    if 'T1CE' in mods and 'T2' in mods:
        try:
            t1ce_vol = load_nifti(mods['T1CE'])
            t2_vol = load_nifti(mods['T2'])
            for z in range(min(t1ce_vol.shape[2], t2_vol.shape[2])):
                t1_slice = resize_2d(t1ce_vol[:, :, z])
                t2_slice = resize_2d(t2_vol[:, :, z])
                X_slices.append(t1_slice[..., np.newaxis])
                Y_slices.append(t2_slice[..., np.newaxis])
            print(f"✅ Sliced patient {pid}")
        except Exception as e:
            print(f"❌ Error with {pid}: {e}")

X = np.array(X_slices, dtype=np.float32)
Y = np.array(Y_slices, dtype=np.float32)

# Train-test split
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=42)
train_ds = tf.data.Dataset.from_tensor_slices((X_train, Y_train)).shuffle(100).batch(8)
val_ds = tf.data.Dataset.from_tensor_slices((X_val, Y_val)).batch(8)

print(f"✅ Total slices: {len(X)}")

import os
import pandas as pd

# ✅ Update metadata path to match your Google Drive structure
metadata_path = '/content/drive/MyDrive/UPENN_GBM_Top10/manifest-1669766397961/metadata.csv'
metadata_df = pd.read_csv(metadata_path)

# Step 2: Check available columns
print("📋 Metadata columns:", metadata_df.columns.tolist())

# Step 3: Extract folder names (patient IDs) from the mounted DICOM directory
dicom_dir = '/content/drive/MyDrive/UPENN_GBM_Top10/manifest-1669766397961/UPENN-GBM'
folder_names = os.listdir(dicom_dir)

# Step 4: Filter valid patient folders (ignore system files)
patient_ids = [f for f in folder_names if f.startswith('UPENN-GBM')]

# Step 5: Match with metadata's "Subject ID" column
if 'Subject ID' in metadata_df.columns:
    metadata_ids = metadata_df['Subject ID'].astype(str).tolist()
elif 'ID' in metadata_df.columns:
    metadata_ids = metadata_df['ID'].astype(str).tolist()
else:
    raise ValueError("❌ Could not find a column for patient ID in the metadata.")

# Step 6: Remove suffix from folder names like "_11" or "_21"
base_patient_ids = [pid.split('_')[0] for pid in patient_ids]
matched = [pid for pid in base_patient_ids if pid in metadata_ids]

# Step 7: Show results
print(f"✅ Matched patients: {matched}")
print(f"➡️ Total matched: {len(matched)} / {len(base_patient_ids)}")

!pip install pydicom

import os
from collections import defaultdict

nifti_dir = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'
patient_modalities = defaultdict(set)

def is_t1ce(name):
    return any(k in name.lower() for k in ['post', 'stealth', 'mprage'])

def is_t2(name):
    return 't2' in name.lower() and 'flair' in name.lower()

# Scan filenames
for fname in os.listdir(nifti_dir):
    if fname.endswith('.nii.gz'):
        patient_id = fname.split('_')[0]
        if is_t1ce(fname):
            patient_modalities[patient_id].add('T1CE')
        if is_t2(fname):
            patient_modalities[patient_id].add('T2')

# Get only those with both
qualified_patients = [pid for pid, mods in patient_modalities.items() if {'T1CE', 'T2'}.issubset(mods)]

print(f"✅ Found {len(qualified_patients)} patients with both T1CE and T2:")
print(qualified_patients)

base_path = '/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'
patient_ids = ['32', '33', '31', '36', '8']

for pid in patient_ids:
    print(f"\n🔍 Patient {pid}")
    for f in os.listdir(base_path):
        if f.startswith(pid):
            print(f"  - {f}")

##TUMOUR ONSET CLASSIFICATION

import pandas as pd
import numpy as np

# Load the clinical metadata (replace with your actual path)
metadata_path = '/content/drive/MyDrive/UPENN-GBM_clinical_info_v2.1 (1).csv'
metadata_df = pd.read_csv(metadata_path)

# Ensure the relevant column is numeric
metadata_df['Time_since_baseline_preop'] = pd.to_numeric(metadata_df['Time_since_baseline_preop'], errors='coerce')

# Drop rows with NaNs in required columns
metadata_df = metadata_df.dropna(subset=['ID', 'Time_since_baseline_preop'])

# Define time bins and labels
bins = [-np.inf, 0, 90, 180, 365, np.inf]  # Modify as needed
labels = ['Pre-op', '<3 months', '3-6 months', '6-12 months', '>1 year']

# Create onset class column
metadata_df['onset_class'] = pd.cut(
    metadata_df['Time_since_baseline_preop'],
    bins=bins,
    labels=labels
)

print("Labeled metadata sample:")
print(metadata_df[['ID', 'Time_since_baseline_preop', 'onset_class']].head())

import os

# Your filtered image samples (ensure this list contains filenames or paths)
image_patient_ids = ['UPENN-GBM-00001_11', 'UPENN-GBM-00002_11', 'UPENN-GBM-00003_11',
                     'UPENN-GBM-00004_11', 'UPENN-GBM-00005_11', 'UPENN-GBM-00006_11']  # etc.

# Filter metadata to those image IDs
metadata_filtered = metadata_df[metadata_df['ID'].isin(image_patient_ids)].copy()

# Verify results
print("Filtered metadata with onset labels:")
print(metadata_filtered[['ID', 'Time_since_baseline_preop', 'onset_class']])

# Find post-op samples (time > 0)
post_op_df = metadata_df[metadata_df['Time_since_baseline_preop'] > 0].copy()

# Bin post-op samples into onset classes
post_op_df['onset_class'] = pd.cut(
    post_op_df['Time_since_baseline_preop'],
    bins=[-1, 90, 180, 365, 10000],  # days
    labels=['<3 months', '3-6 months', '6-12 months', '>1 year']
)

# Display some samples
print(post_op_df[['ID', 'Time_since_baseline_preop', 'onset_class']].head(10))

# List all defined variables
import gc

defined_vars = [var for var in globals() if isinstance(eval(var), pd.DataFrame)]
print("Available DataFrames:", defined_vars)

# Step 1: Extract pre-op patients (Time_since_baseline_preop == 0)
preop_df = metadata_df[metadata_df['Time_since_baseline_preop'] == 0].copy()
preop_df['onset_class'] = 'Pre-op'

# Step 2: Reuse existing labeled post_op_df (with onset_class from earlier)
# post_op_df is already assumed to have the onset_class column

# Step 3: Combine both into a single labeled metadata DataFrame
metadata_df_full = pd.concat([preop_df, post_op_df], axis=0).reset_index(drop=True)

# Step 4: Check final result
print("Final labeled metadata sample:")
print(metadata_df_full[['ID', 'Time_since_baseline_preop', 'onset_class']].sample(10))

# Optional: Save to CSV if needed
# metadata_df_full.to_csv('/content/drive/MyDrive/labeled_onset_metadata.csv', index=False)

import nibabel as nib
import os
import numpy as np

def load_modalities(patient_id, modalities=['T1CE', 'FLAIR'], base_path='/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality'):
    data = {}
    for mod in modalities:
        mod_path = os.path.join(base_path, mod, f"{patient_id}_{mod}.nii.gz")
        if os.path.exists(mod_path):
            img = nib.load(mod_path).get_fdata()
            data[mod] = img
    return data
def extract_central_slices(modality_data, slice_range=(40, 70)):
    stacked_slices = []
    for i in range(slice_range[0], slice_range[1]):
        slice_stack = []
        for mod in modality_data:
            slice_stack.append(modality_data[mod][:, :, i])
        stacked_slices.append(np.stack(slice_stack, axis=-1))  # (H, W, C)
    return stacked_slices  # List of (H, W, C)


from tensorflow.keras.utils import to_categorical

def create_dataset(metadata_df, label_encoder, slice_range=(40, 70)):
    images, labels = [], []
    for _, row in metadata_df.iterrows():
        patient_id = row['ID']
        label = row['onset_class']
        try:
            modality_data = load_modalities(patient_id.split('_')[0])
            slices = extract_central_slices(modality_data, slice_range)
            images.extend(slices)
            labels.extend([label_encoder[label]] * len(slices))
        except Exception as e:
            print(f"Failed for {patient_id}: {e}")
    return np.array(images), to_categorical(labels)


label_map = {'Pre-op': 0, '<3 months': 1, '3-6 months': 2, '6-12 months': 3, '>1 year': 4}

import os

# Define the root directory containing all NIfTI files
nifti_dir = "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality"
all_files = os.listdir(nifti_dir)

# Extract sample IDs
sample_ids = ['UPENN-GBM-00001', 'UPENN-GBM-00002', 'UPENN-GBM-00003', 'UPENN-GBM-00004',
              'UPENN-GBM-00005', 'UPENN-GBM-00006', 'UPENN-GBM-00007', 'UPENN-GBM-00008',
              'UPENN-GBM-00009', 'UPENN-GBM-00010']

# Match based on filename prefixes
valid_samples = []
for sid in sample_ids:
    patient_num = sid.split('-')[-1].lstrip('0')  # e.g., '00001' → '1'

    # Find files for this patient
    patient_files = [f for f in all_files if f.startswith(patient_num + "_") or f.startswith(patient_num + "-") or f.startswith(patient_num)]

    # Detect T1CE and T2/FLAIR from filenames
    t1ce_file = next((f for f in patient_files if 'post' in f.lower() and 't1' in f.lower()), None)
    t2_file = next((f for f in patient_files if 'flair' in f.lower() or ('t2' in f.lower() and 'tse' not in f.lower())), None)

    if t1ce_file and t2_file:
        valid_samples.append({
            'ID': sid,
            't1ce_path': os.path.join(nifti_dir, t1ce_file),
            't2_path': os.path.join(nifti_dir, t2_file)
        })

print(f"✅ Found {len(valid_samples)} patients with both T1CE and T2/FLAIR:")
for vs in valid_samples:
    print(vs['ID'], "→", os.path.basename(vs['t1ce_path']), "|", os.path.basename(vs['t2_path']))

import os
import numpy as np
import nibabel as nib
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# --------------------- Step 1: Setup --------------------- #

# Ensure numeric type (will turn invalid strings into NaN if any)
df['Time_since_baseline_preop'] = pd.to_numeric(df['Time_since_baseline_preop'], errors='coerce')

# Then apply the onset classification
df['onset_class'] = df['Time_since_baseline_preop'].apply(label_onset)

def label_onset(val):
    if val == 0:
        return 'Pre-op'
    elif val <= 90:
        return '<3 months'
    elif val <= 180:
        return '3-6 months'
    elif val <= 365:
        return '6-12 months'
    else:
        return '>1 year'

# Apply it directly to the column
df['onset_class'] = df['Time_since_baseline_preop'].apply(label_onset)


# Use the confirmed patient matches
valid_samples = [
    {
        "ID": "UPENN-GBM-00001",
        "t1ce_path": "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality/16_t1_axial_stealth-post__processed_captk.nii.gz",
        "flair_path": "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality/11_axial_t2_flair_processed_captk.nii.gz"
    },
    {
        "ID": "UPENN-GBM-00003",
        "t1ce_path": "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality/33_ax_t1_3d_post_stealth__processed_captk.nii.gz",
        "flair_path": "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality/31_t2_axial_flair_processed_captk.nii.gz"
    },
    {
        "ID": "UPENN-GBM-00004",
        "t1ce_path": "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality/46_ax_t1_3d_post_stealth__processed_captk.nii.gz",
        "flair_path": "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality/44_t2_axial_flair_processed_captk.nii.gz"
    }
]

combined_metadata = df.copy()
combined_metadata['base_id'] = combined_metadata['ID'].apply(lambda x: x.split('_')[0])

label_map = {'Pre-op': 0, '<3 months': 1, '3-6 months': 2, '6-12 months': 3, '>1 year': 4}

# --------------------- Step 2: Load Modalities & Extract Slices --------------------- #

def load_modalities_and_slices(t1ce_path, flair_path, slice_range=(40, 70), target_size=(128, 128)):
    t1ce_img = nib.load(t1ce_path).get_fdata()
    flair_img = nib.load(flair_path).get_fdata()

    #Getting the minimum depth to avoid IndexErrors
    min_depth = min(t1ce_img.shape[2], flair_img.shape[2])
    end_slice = min(slice_range[1], min_depth)

    slices = []
    for i in range(slice_range[0], end_slice):
        t1ce_slice = t1ce_img[:, :, i]
        flair_slice = flair_img[:, :, i]

        if not np.any(t1ce_slice) or not np.any(flair_slice):
            continue

        #Resize each to 128x128
        t1ce_resized = tf.image.resize(t1ce_slice[..., np.newaxis], target_size).numpy().squeeze()
        flair_resized = tf.image.resize(flair_slice[..., np.newaxis], target_size).numpy().squeeze()

        combined = np.stack([t1ce_resized, flair_resized], axis=-1)
        slices.append(combined)

    return slices


X = []
y = []

for sample in valid_samples:
    base_id = sample['ID']
    onset_label = combined_metadata[combined_metadata['base_id'] == base_id]['onset_class'].values[0]

    slices = load_modalities_and_slices(sample['t1ce_path'], sample['flair_path'])
    X.extend(slices)
    y.extend([label_map[onset_label]] * len(slices))

X = np.array(X)
y = np.array(y)

# ------------------- Step 3: Normalize and Resize ------------------- #

print("X shape before resize:", X.shape)

X = (X - np.min(X)) / (np.max(X) - np.min(X) + 1e-5)
X = tf.image.resize(X, [128, 128]).numpy()


from tensorflow.keras.utils import to_categorical
y = to_categorical(y, num_classes=5)


# -------------------- Step 4: Train-Test Split -------------------- #

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# --------------------- Step 5: CNN Model --------------------- #

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 2)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(5, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# --------------------- Step 6: Train & Evaluate --------------------- #

history = model.fit(X_train, y_train, validation_split=0.2, epochs=10, batch_size=8)
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true_classes = np.argmax(y_test, axis=1)

from sklearn.metrics import classification_report

print(classification_report(
    y_true_classes,
    y_pred_classes,
    labels=[0, 1, 2, 3, 4],  #Expected class indices
    target_names=list(label_map.keys()),
    zero_division=0          #Avoiding divide-by-zero for missing classes
))

import random
import matplotlib.pyplot as plt
import numpy as np

def predict_random_slice(X, y, model, label_map):
    inverse_label_map = {v: k for k, v in label_map.items()}

    idx = random.randint(0, len(X) - 1)
    sample = X[idx]
    true_label = np.argmax(y[idx])
    pred = model.predict(np.expand_dims(sample, axis=0))
    pred_class = np.argmax(pred)

    #Result
    print(f"✅ True label: {inverse_label_map[true_label]}")
    print(f"🎯 Predicted label: {inverse_label_map[pred_class]}")

    #Show slice
    plt.imshow(sample[:, :, 0], cmap='gray')
    plt.title("T1CE (channel 0)")
    plt.axis("off")
    plt.show()

    plt.imshow(sample[:, :, 1], cmap='gray')
    plt.title("FLAIR (channel 1)")
    plt.axis("off")
    plt.show()

predict_random_slice(X, y, model, label_map)

##TUMOUR DETERIORATION CLASSIFICATION

import os
import numpy as np
import nibabel as nib
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# --------------------- Load Metadata --------------------- #
metadata_path = "/content/drive/MyDrive/UPENN-GBM_clinical_info_v2.1 (1).csv"
df = pd.read_csv(metadata_path)
df = df[['ID', 'PsP_TP_score', 'Time_since_baseline_preop']]
df = df[df['PsP_TP_score'].notna()]  # Filter out patients without labels
df['PsP_TP_score'] = df['PsP_TP_score'].astype(int)
df['base_id'] = df['ID'].apply(lambda x: x.split('_')[0])

# --------------------- Match Image Files --------------------- #
nifti_folder = "/content/drive/MyDrive/UPENN_GBM_Top10_NIfTI_Converted_Modality"
all_files = os.listdir(nifti_folder)
t1ce_files = [f for f in all_files if 't1' in f.lower() and 'post' in f.lower()]
t2_flair_files = [f for f in all_files if 'flair' in f.lower()]

image_matches = []
for _, row in df.iterrows():
    pid = row['base_id']
    t1ce = [f for f in t1ce_files if f.startswith(pid)]
    flair = [f for f in t2_flair_files if f.startswith(pid)]
    if t1ce and flair:
        image_matches.append({
            'base_id': pid,
            't1ce_path': os.path.join(nifti_folder, t1ce[0]),
            'flair_path': os.path.join(nifti_folder, flair[0])
        })

# --------------------- Load Images --------------------- #
def load_modalities_and_slices(t1ce_path, flair_path, slice_range=(20, 50), target_size=(128, 128)):
    t1ce_img = nib.load(t1ce_path).get_fdata()
    flair_img = nib.load(flair_path).get_fdata()
    t1ce_img = np.nan_to_num(t1ce_img)
    flair_img = np.nan_to_num(flair_img)
    slices = []
    for i in range(slice_range[0], min(slice_range[1], t1ce_img.shape[2], flair_img.shape[2])):
        t1ce_slice = t1ce_img[:, :, i]
        flair_slice = flair_img[:, :, i]
        if t1ce_slice.shape != flair_slice.shape:
            continue
        combined = np.stack([t1ce_slice, flair_slice], axis=-1)
        combined = tf.image.resize(combined, target_size).numpy()
        slices.append(combined)
    return slices

X = []
y = []
for sample in image_matches:
    base_id = sample['base_id']
    label = df[df['base_id'] == base_id]['PsP_TP_score'].values[0]
    slices = load_modalities_and_slices(sample['t1ce_path'], sample['flair_path'])
    X.extend(slices)
    y.extend([label] * len(slices))

X = np.array(X)
y = np.array(y)

# --------------------- Preprocess --------------------- #
X = (X - X.min()) / (X.max() - X.min())
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# --------------------- Build Model --------------------- #
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 2)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# --------------------- Train & Evaluate --------------------- #
history = model.fit(X_train, y_train, validation_split=0.2, epochs=10, batch_size=8)
y_pred = model.predict(X_test)
y_pred_classes = (y_pred > 0.5).astype(int).flatten()

print("\nClassification Report for Tumor Deterioration Prediction:")
print(classification_report(y_test, y_pred_classes, target_names=["PsP", "TP"]))