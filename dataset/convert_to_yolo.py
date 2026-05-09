import xml.etree.ElementTree as ET
import os

xml_file = r"/home/nour/Smart Parking YOLO/dataset/annotations.xml"
images_dir = r"/home/nour/Smart Parking YOLO/dataset/images"
labels_dir = r"/home/nour/Smart Parking YOLO/dataset/labels"

os.makedirs(labels_dir, exist_ok=True)

# =========================
# CLASS MAPPING
# =========================
class_map = {
    "free_parking_space": 0,        # empty
    "not_free_parking_space": 1,    # occupied
    "partially_free_parking_space": 1  # occupied
}

# =========================
# LOAD XML
# =========================
tree = ET.parse(xml_file)
root = tree.getroot()

# =========================
# LOOP OVER IMAGES
# =========================
for image in root.findall("image"):

    image_name = image.get("name")
    image_base_name = os.path.basename(image_name)

    width = float(image.get("width"))
    height = float(image.get("height"))

    # create label file name safely
    label_name = os.path.splitext(image_base_name)[0] + ".txt"
    label_file = os.path.join(labels_dir, label_name)

    with open(label_file, "w") as f:

        for polygon in image.findall("polygon"):

            label = polygon.get("label")

            if label not in class_map:
                continue

            class_id = class_map[label]

            # =========================
            # READ POLYGON POINTS
            # =========================
            points = polygon.get("points").split(";")

            x_coords = []
            y_coords = []

            for p in points:
                x, y = map(float, p.split(","))
                x_coords.append(x)
                y_coords.append(y)

            # =========================
            # POLYGON → BOUNDING BOX
            # =========================
            x_min = min(x_coords)
            y_min = min(y_coords)
            x_max = max(x_coords)
            y_max = max(y_coords)

            # =========================
            # CONVERT TO YOLO FORMAT
            # =========================
            x_center = ((x_min + x_max) / 2) / width
            y_center = ((y_min + y_max) / 2) / height
            w = (x_max - x_min) / width
            h = (y_max - y_min) / height

            # =========================
            # WRITE TO FILE
            # =========================
            f.write(f"{class_id} {x_center} {y_center} {w} {h}\n")

print("Conversion DONE successfully!")