import cv2
import numpy as np
import winsound
import tkinter as tk
from tkinter import messagebox
import os

# -----------------------------
# YOLO FILE PATHS
# -----------------------------
cfg_path = r"C:\Users\aditi\Downloads\Accident detection project\yolov4-tiny.cfg"
weights_path = r"C:\Users\aditi\Downloads\Accident detection project\yolov4-tiny.weights"

print("Config file exists:", os.path.exists(cfg_path))
print("Weights file exists:", os.path.exists(weights_path))

# -----------------------------
# LOAD YOLO MODEL
# -----------------------------
net = cv2.dnn.readNet(weights_path, cfg_path)

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# -----------------------------
# LOAD COCO NAMES
# -----------------------------
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

vehicle_classes = ['car', 'motorbike', 'bus', 'truck']

# -----------------------------
# ALERT FUNCTION
# -----------------------------
alert_shown = False

def show_alert():
    root = tk.Tk()
    root.withdraw()

    messagebox.showwarning(
        "ACCIDENT ALERT",
        "🚨 Accident Detected!\nImmediate attention required!"
    )

    root.destroy()

# -----------------------------
# OPEN WEBCAM
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    height, width, _ = frame.shape

    blob = cv2.dnn.blobFromImage(
        frame,
        1/255,
        (416,416),
        swapRB=True,
        crop=False
    )

    net.setInput(blob)
    outs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] in vehicle_classes:

                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        0.5,
        0.4
    )

    accident_detected = False

    if len(indexes) > 0:

        indexes = indexes.flatten()

        for i in indexes:

            x1, y1, w1, h1 = boxes[i]

            label = classes[class_ids[i]]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x1+w1, y1+h1),
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            for j in indexes:

                if i == j:
                    continue

                x2, y2, w2, h2 = boxes[j]

                if (
                    x1 < x2 + w2 and
                    x1 + w1 > x2 and
                    y1 < y2 + h2 and
                    y1 + h1 > y2
                ):

                    accident_detected = True

    if accident_detected:

        cv2.putText(
            frame,
            "ACCIDENT DETECTED!",
            (40,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            3
        )

        if not alert_shown:

            winsound.Beep(1000,1000)
            show_alert()

            alert_shown = True

    else:
        alert_shown = False

    cv2.imshow("Accident Detection - Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# RELEASE
# -----------------------------
cap.release()
cv2.destroyAllWindows()