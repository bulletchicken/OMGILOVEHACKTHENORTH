import cv2
from ultralytics import YOLO
from serial import Serial
import os
import math
ser = Serial('/dev/cu.usbserial-120', 9600)
import time

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')  # 'n' for nano, you can change to 's', 'm', 'l', or 'x' for other model sizes

# Open the video capture
cap = cv2.VideoCapture(0)  # Use 0 for webcam, or provide a video file path

while cap.isOpened():
    time.sleep(0.5)
    # Read a frame from the video
    success, frame = cap.read()
    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)
        
        closest_person = None
        max_area = 0
        
        # Iterate through the detections
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Check if the detected object is a person (class 0 in COCO dataset)
                if int(box.cls) == 0:
                    # Get the bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Calculate area of bounding box
                    area = (x2 - x1) * (y2 - y1)
                    
                    # If this is the largest bounding box so far, update closest_person
                    if area > max_area:
                        max_area = area
                        closest_person = (x1, y1, x2, y2)
        
        if closest_person:
            x1, y1, x2, y2 = closest_person
            
            # Draw bounding box for the closest person
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Calculate and draw center point
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
            
            # Display the x-coordinate on the frame
            cv2.putText(frame, f"Closest Person X: {center_x}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Print the x-coordinate (you can modify this to send to Arduino)
            into = ("t" + str(math.floor((center_x*0.1125))))
            print(into)
            ser.write(into.encode())
        
        # Display the frame
        cv2.imshow("YOLOv8 Closest Person Detection", frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()