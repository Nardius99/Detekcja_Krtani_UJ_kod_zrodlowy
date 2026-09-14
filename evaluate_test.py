from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"runs\detect\runs_krtan\baseline_yolov8n-3\weights\best.pt")
    metrics = model.val(data="data.yaml", split="test")