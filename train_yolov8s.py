from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO("yolov8s.pt")

    model.train(
        data="data.yaml",
        epochs=100,
        imgsz=640,
        batch=16,
        patience=20,
        device=0,
        project="runs_krtan",
        name="yolov8s_experiment"
    )