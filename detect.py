from ultralytics import YOLO

model = YOLO("best.pt")

results = model.predict("dataset/train/images/Screenshot-2023-11-23-160854_png.rf.bf41b83ff987a976d8936356c1bb6dd5.jpg")

result = results[0]

for box in result.boxes:
  class_id = result.names[box.cls[0].item()]
  cords = box.xyxy[0].tolist()
  cords = [round(x) for x in cords]
  conf = round(box.conf[0].item(), 2)
  print("Object type:", class_id)
  print("Coordinates:", cords)
  print("Probability:", conf)
  print("---------------------")