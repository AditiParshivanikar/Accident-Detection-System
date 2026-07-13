import os
import cv2
import numpy as np
import time
import logging

logger = logging.getLogger(__name__)

# Fallback imports
YOLO_AVAILABLE = False
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    logger.warning("ultralytics (YOLOv8) not installed. Only YOLOv4-Tiny will be available until installed.")

class ModelManager:
    def __init__(self):
        self.current_model_name = None
        self.yolo_tiny_net = None
        self.yolo_tiny_layers = None
        self.yolo_v8_model = None
        self.classes = []
        self.load_classes()

    def load_classes(self):
        # Load COCO classes for YOLOv4-Tiny
        coco_path = "coco.names"
        if os.path.exists(coco_path):
            with open(coco_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
        else:
            # Fallback standard COCO classes
            self.classes = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck"]
            logger.warning("coco.names not found. Loaded default classes subset.")

    def load_yolo_tiny(self):
        if self.yolo_tiny_net is not None:
            return
        
        cfg_path = "yolov4-tiny.cfg"
        weights_path = "yolov4-tiny.weights"
        
        # Verify paths
        if not os.path.exists(cfg_path) or not os.path.exists(weights_path):
            # Try workspace absolute paths
            alt_cfg = r"C:\Users\aditi\Downloads\Accident detection project\yolov4-tiny.cfg"
            alt_weights = r"C:\Users\aditi\Downloads\Accident detection project\yolov4-tiny.weights"
            if os.path.exists(alt_cfg) and os.path.exists(alt_weights):
                cfg_path = alt_cfg
                weights_path = alt_weights
            else:
                raise FileNotFoundError(f"YOLOv4-Tiny config/weights not found in root or absolute paths.")

        logger.info(f"Loading YOLOv4-Tiny: {cfg_path}, {weights_path}")
        self.yolo_tiny_net = cv2.dnn.readNet(weights_path, cfg_path)
        layer_names = self.yolo_tiny_net.getLayerNames()
        self.yolo_tiny_layers = [layer_names[i - 1] for i in self.yolo_tiny_net.getUnconnectedOutLayers().flatten()]
        logger.info("YOLOv4-Tiny loaded successfully.")

    def load_yolo_v8(self):
        if not YOLO_AVAILABLE:
            raise ImportError("Ultralytics package is not installed. Cannot load YOLOv8 model.")
        
        if self.yolo_v8_model is not None:
            return

        model_path = "best(3).pt"
        if not os.path.exists(model_path):
            alt_path = r"C:\Users\aditi\Downloads\Accident detection project\best(3).pt"
            if os.path.exists(alt_path):
                model_path = alt_path
            else:
                # Fallback to standard yolov8n.pt if custom model doesn't exist
                model_path = "yolov8n.pt"
                logger.warning(f"best(3).pt not found. Falling back to {model_path}")
        
        logger.info(f"Loading YOLOv8 model: {model_path}")
        self.yolo_v8_model = YOLO(model_path)
        logger.info("YOLOv8 loaded successfully.")

    def detect(self, frame, model_name="yolov4-tiny", conf_threshold=0.5, nms_threshold=0.4):
        """
        Runs object detection and accident detection on a single frame.
        Returns:
            processed_frame: Annotated image (numpy array)
            stats: Dict containing vehicle counts, accident status, etc.
        """
        start_time = time.time()
        height, width, _ = frame.shape
        vehicle_classes = ['car', 'motorbike', 'bus', 'truck', 'motorcycle']
        
        boxes = []
        confidences = []
        class_ids = []
        detected_names = []

        # Switch/Load model if name changed
        if model_name != self.current_model_name:
            if model_name == "yolov8" and YOLO_AVAILABLE:
                try:
                    self.load_yolo_v8()
                    self.current_model_name = "yolov8"
                except Exception as e:
                    logger.error(f"Failed to load YOLOv8: {e}. Falling back to YOLOv4-Tiny.")
                    self.load_yolo_tiny()
                    self.current_model_name = "yolov4-tiny"
            else:
                self.load_yolo_tiny()
                self.current_model_name = "yolov4-tiny"

        accident_detected = False
        accident_from_class = False

        if self.current_model_name == "yolov8" and self.yolo_v8_model is not None:
            # YOLOv8 Inference
            # predict returns a list of Results objects
            results = self.yolo_v8_model(frame, conf=conf_threshold, iou=nms_threshold, verbose=False)
            r = results[0]
            
            # Read names from model
            model_classes = r.names
            
            for box in r.boxes:
                cls_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                cname = model_classes.get(cls_id, str(cls_id)).lower()

                # If model has direct accident detection class (e.g. custom model)
                if cname in ['accident', 'crash', 'collision']:
                    accident_detected = True
                    accident_from_class = True
                
                # Check if it is a vehicle class
                is_vehicle = cname in vehicle_classes or any(vc in cname for vc in vehicle_classes)
                
                if is_vehicle or cname in ['accident', 'crash', 'collision']:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w = x2 - x1
                    h = y2 - y1
                    boxes.append([x1, y1, w, h])
                    confidences.append(confidence)
                    # Use index in self.classes if it matches, otherwise append dynamically
                    if cname not in self.classes:
                        self.classes.append(cname)
                    class_ids.append(self.classes.index(cname))
                    detected_names.append(cname)

        else:
            # YOLOv4-Tiny Inference (OpenCV DNN)
            if self.yolo_tiny_net is None:
                self.load_yolo_tiny()
            
            blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True, crop=False)
            self.yolo_tiny_net.setInput(blob)
            outs = self.yolo_tiny_net.forward(self.yolo_tiny_layers)

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > conf_threshold:
                        cname = self.classes[class_id] if class_id < len(self.classes) else "unknown"
                        if cname in vehicle_classes:
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)
                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)

                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                            detected_names.append(cname)

        # Run NMS (If YOLOv8, it is already filtered but running NMS again is safe or can be bypassed. 
        # For uniformity and custom NMS slider control, we run NMS on all extracted boxes)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        
        # Flatten index array
        if len(indexes) > 0:
            indexes = indexes.flatten()
        else:
            indexes = []

        # Count vehicle types
        vehicle_counts = {"car": 0, "bus": 0, "truck": 0, "motorcycle": 0}
        active_boxes = []

        # Draw boxes and calculate counts
        for i in indexes:
            x, y, w, h = boxes[i]
            label = detected_names[i]
            conf = confidences[i]
            
            # Map labels
            mapped_label = "motorcycle" if label in ["motorbike", "motorcycle"] else label
            if mapped_label in vehicle_counts:
                vehicle_counts[mapped_label] += 1
            
            active_boxes.append((x, y, w, h, label, conf))
            
            # Draw green bounding box for safe objects
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{mapped_label} {conf:.2f}", (x, y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Check vehicle collisions (Overlap algorithm)
        # Check every pair of active bounding boxes
        if not accident_from_class:
            for idx1 in range(len(active_boxes)):
                x1, y1, w1, h1, label1, conf1 = active_boxes[idx1]
                # Only check collision between vehicle classes
                if label1 not in vehicle_classes and not any(vc in label1 for vc in vehicle_classes):
                    continue
                
                for idx2 in range(idx1 + 1, len(active_boxes)):
                    x2, y2, w2, h2, label2, conf2 = active_boxes[idx2]
                    if label2 not in vehicle_classes and not any(vc in label2 for vc in vehicle_classes):
                        continue
                    
                    # Check overlap (AABB intersection check)
                    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
                        accident_detected = True
                        
                        # Draw overlap indicator or highlight colliding boxes in red
                        cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 3)
                        cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 3)

        latency = (time.time() - start_time) * 1000 # in ms
        total_vehicles = sum(vehicle_counts.values())
        avg_confidence = float(np.mean(confidences)) if confidences else 0.0

        if accident_detected:
            # Highlight accident warning on frame
            cv2.putText(frame, "ACCIDENT DETECTED!", (30, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        stats = {
            "vehicle_count": total_vehicles,
            "car_count": vehicle_counts["car"],
            "bus_count": vehicle_counts["bus"],
            "truck_count": vehicle_counts["truck"],
            "motorcycle_count": vehicle_counts["motorcycle"],
            "accident_detected": accident_detected,
            "confidence": avg_confidence,
            "latency_ms": latency,
            "fps": 1000.0 / latency if latency > 0 else 0.0
        }

        return frame, stats

# Single instance of model manager
model_manager = ModelManager()
