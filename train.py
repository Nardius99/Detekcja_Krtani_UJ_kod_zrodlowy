from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8n.pt")

    model.train(
        data="data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        patience=20,
        device=0,
        project="runs_krtan",
        name="baseline_yolov8n"
    )