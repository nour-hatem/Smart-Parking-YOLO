import os
import shutil
import random

source_images_dir = r"/home/nour/Smart Parking YOLO/dataset/images"
source_labels_dir = r"/home/nour/Smart Parking YOLO/dataset/labels"

project_dir = r"/home/nour/Smart Parking YOLO"
dataset_dir = os.path.join(project_dir, "dataset")

for split in ["train", "valid", "test"]:
    os.makedirs(os.path.join(dataset_dir, "images", split), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, "labels", split), exist_ok=True)

image_files = []

for file in os.listdir(source_images_dir):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        name_without_ext = os.path.splitext(file)[0]
        label_file = name_without_ext + ".txt"
        label_path = os.path.join(source_labels_dir, label_file)

        if os.path.exists(label_path):
            image_files.append(file)
        else:
            print("Missing label for:", file)

random.seed(42)
random.shuffle(image_files)

total = len(image_files)

train_count = int(total * 0.7)
valid_count = int(total * 0.2)
test_count = total - train_count - valid_count

train_files = image_files[:train_count]
valid_files = image_files[train_count:train_count + valid_count]
test_files = image_files[train_count + valid_count:]

splits = {
    "train": train_files,
    "valid": valid_files,
    "test": test_files
}

for split_name, files in splits.items():
    for image_name in files:
        name_without_ext = os.path.splitext(image_name)[0]
        label_name = name_without_ext + ".txt"

        shutil.copy2(
            os.path.join(source_images_dir, image_name),
            os.path.join(dataset_dir, "images", split_name, image_name)
        )

        shutil.copy2(
            os.path.join(source_labels_dir, label_name),
            os.path.join(dataset_dir, "labels", split_name, label_name)
        )

data_yaml_content = """path: /home/nour/Smart Parking YOLO/dataset
train: images/train
val: images/valid
test: images/test

names:
  0: empty
  1: occupied
"""

with open(os.path.join(dataset_dir, "data.yaml"), "w", encoding="utf-8") as f:
    f.write(data_yaml_content)

print("Done")
print("Total valid image-label pairs:", total)
print("Train:", len(train_files))
print("Valid:", len(valid_files))
print("Test:", len(test_files))