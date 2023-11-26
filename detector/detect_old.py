from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

# image_path = "train/images/download_jpg.rf.09ea86daf304f9b5bf5fbe3e6c03a7e7.jpg"
# image_path = "train/images/Acyrthosiphon-lactucae-129151_jpg.rf.f22487b4ed1848dd7b72a89ee2fa74f3.jpg"
# image_path = "train/images/Screenshot-2023-11-25-112646_png.rf.93a729dfb87840ef7c75be0b5f02a2b0.jpg"
# image_path = "train/images/images-13-_jpg.rf.11ed3b01cf7bf5e91dfcaae8c86a3981.jpg"
image_path = "images (26).jpg"

results = model.predict(image_path)

result = results[0]

# Load the image
image = cv2.imread(image_path)

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