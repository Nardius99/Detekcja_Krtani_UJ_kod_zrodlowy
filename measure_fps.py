import time
import glob
from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"runs\detect\runs_krtan\baseline_yolov8n-3\weights\best.pt")

    test_images = glob.glob("dataset/images/test/*.png")
    sample_image = test_images[0]

    for _ in range(10):
        model.predict(sample_image, verbose=False, device=0)

    n = 100
    start = time.time()
    for _ in range(n):
        model.predict(sample_image, verbose=False, device=0)
    end = time.time()

    avg_ms = (end - start) / n * 1000
    fps = n / (end - start)
    print(f"Sredni czas inferencji: {avg_ms:.2f} ms")
    print(f"Sredni FPS: {fps:.2f}")