import traceback

from ultralytics import YOLO
from PIL import ImageDraw, Image
import io
import os
import uuid

model = YOLO("../detector/best.pt")


def pest_detector(image_data):
    try:
        # Convert the image data bytes to a PIL Image object
        # image = Image.open(io.BytesIO(image_data))
        image = image_data
        # Perform object detection on the image
        results = model.predict(image)

        result = results[0]

        result_dict = {}

        for box in result.boxes:
            class_id = box.cls[0].item()
            class_name = result.names[class_id]
            cords = box.xyxy[0].tolist()
            cords = [round(x) for x in cords]
            conf = round(box.conf[0].item(), 2)

            obj_count = 1

            exist_obj = result_dict.get(class_id)
            if exist_obj:
                exist_obj['count'] = exist_obj['count'] + 1
            else:
                result_dict.update({class_id: {"class_name": class_name, "count": obj_count}})

            # Draw bounding boxes on the image
            draw = ImageDraw.Draw(image)
            draw.rectangle(cords, outline="red", width=3)
            draw.text((cords[0], cords[1]), f"{class_name} {conf}", fill="red")

        # Save the modified image
        unique_filename = f"{str(uuid.uuid4())}.jpg"
        saved_image_path = os.path.join("results/", unique_filename)  # Change this to your desired save path
        image.save(saved_image_path)

        print(result_dict)

        return saved_image_path, result_dict

    except:
        print(traceback.format_exc())

