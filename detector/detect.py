from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train8/weights/best.pt")

results = model.predict("fimmu-13-907088-g001.jpg")

result = results[0]

# Load the image
image = cv2.imread("../detector/train/images/d9ef5e-1_jpg.rf.78f0ae0b4473c13f4ee5458fc217cc5e.jpg")

for box in result.boxes:
    class_id = result.names[box.cls[0].item()]
    cords = box.xyxy[0].tolist()
    cords = [round(x) for x in cords]
    conf = round(box.conf[0].item(), 2)

    # Extract coordinates
    x_min, y_min, x_max, y_max = cords

    # Draw bounding box
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Add label and confidence
    label = f"{class_id} {conf}"
    cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    print("Object type:", class_id)
    print("Coordinates:", cords)
    print("Probability:", conf)
    print("---------------------")

# Display the image with bounding boxes
cv2.imshow("Detected Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
