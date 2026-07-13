import os
import cv2
import numpy as np
from ultralytics import YOLO
import random
from datetime import datetime

UPLOAD_FOLDER = 'backend/uploads'
MODEL_PATH = 'D:/Microsoft VS Code/backend/best(3).pt'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO(MODEL_PATH)

GSD = 0.05  # Ground Sampling Distance in meters per pixel

def process_image(file_path):
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + "_" + os.path.basename(file_path)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    os.rename(file_path, filepath)

    image = cv2.imread(filepath)
    if image is None:
        raise ValueError("Invalid image")

    results = model(image, conf=0.7)

    class_names = list(model.names.values())
    colors = {class_names[0]: [0, 165, 255]}
    for cname in class_names[1:]:
        colors[cname] = [random.randint(0, 255) for _ in range(3)]

    counts, real_areas, confidences = {}, {}, {}
    image_area = image.shape[0] * image.shape[1]

    for r in results:
        if r.masks is None:
            continue
        for box, mask in zip(r.boxes, r.masks.data):
            cls_id = int(box.cls[0].item())
            class_name = r.names[cls_id]

            counts.setdefault(class_name, [0, 0.0])
            real_areas.setdefault(class_name, 0.0)
            confidences.setdefault(class_name, 0.0)

            counts[class_name][0] += 1
            mask = mask.cpu().numpy()
            mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
            mask_pixels = np.sum(mask > 0.5)
            mask_percentage = (mask_pixels / image_area) * 100
            counts[class_name][1] += mask_percentage
            real_areas[class_name] += mask_pixels * (GSD ** 2)

            confidences[class_name] = (confidences[class_name] * (counts[class_name][0] - 1) + box.conf[0].item()) / counts[class_name][0]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = colors[class_name]
            label = f"{class_name} {box.conf[0]:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            mask = (mask > 0.5).astype(np.uint8)
            color_mask = np.zeros_like(image, dtype=np.uint8)
            color_mask[mask == 1] = color
            image = cv2.addWeighted(image, 1.0, color_mask, 0.5, 0)

    output_path = os.path.join(UPLOAD_FOLDER, "output_" + filename)
    cv2.imwrite(output_path, image)

    return {
        'output_path': output_path,
        'counts': counts,
        'areas': real_areas,
        'confidences': confidences
    }

# Example usage
# result = process_image("path_to_your_image.jpg")
# print(result)