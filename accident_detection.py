import cv2
import numpy as np
import winsound

# Load YOLO
import os  # Make sure this is at the top of your file

# Step 1: Set full paths to the YOLO files
cfg_path = r"C:\Users\aditi\Downloads\Accident detection project\yolov4-tiny.cfg"
weights_path = r"C:\Users\aditi\Downloads\Accident detection project\yolov4-tiny.weights"

# Step 2: Check if the files are actually found
print("Config file exists:", os.path.exists(cfg_path))       # This will say True or False
print("Weights file exists:", os.path.exists(weights_path))  # This will say True or False

# Step 3: Load the YOLO model
net = cv2.dnn.readNet(weights_path, cfg_path) 
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Load class names from coco.names
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


# Load the video
cap = cv2.VideoCapture("test_video.mp4")
if not cap.isOpened():
    print("Error:Could not open video.")
    exit()

# Resize output for display
frame_width = 640
frame_height = 480

vehicle_classes = ['car', 'motorbike', 'bus', 'truck']

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (frame_width, frame_height))
    height, width, _ = frame.shape

    # Detect objects
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
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

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    accident_detected = False

    # Draw boxes
    for i in range(len(boxes)):
        if i in indexes:
            x1, y1, w1, h1 = boxes[i]
            label1 = str(classes[class_ids[i]])
            cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            cv2.putText(frame, label1, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

            for j in range(i + 1, len(boxes)):
                if j in indexes:
                    x2, y2, w2, h2 = boxes[j]
                    label2 = str(classes[class_ids[j]])
                    
                    # Check for collision
                    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
                        accident_detected = True

    #from twilio.rest import Client
    #def send_sms_alert():
        #account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        #auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        #client = Client(account_sid, auth_token)

        #message = client.messages.create(
            #body="🚨 Accident Detected! Immediate attention required.",
            #from_="xxxxxxxxxxx",
            #to="xxxxxxxxxxx"
    

        #print("SMS sent:", message.sid)

    if accident_detected:
         winsound.Beep(1000, 1000)
         send_sms_alert()
         cv2.putText(frame, "ACCIDENT DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Detection", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
   
 

cap.release()
cv2.destroyAllWindows()

