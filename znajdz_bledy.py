import os, glob, shutil
from ultralytics import YOLO

MODEL = r"runs\detect\runs_krtan\baseline_yolov8n-3\weights\best.pt"
IMG_DIR = "dataset/images/test"
LBL_DIR = "dataset/labels/test"
OUT_DIR = "analiza_bledow"
CONF = 0.25
IOU_PROG = 0.3

def iou(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
    inter = iw * ih
    if inter == 0:
        return 0.0
    union = (ax2-ax1)*(ay2-ay1) + (bx2-bx1)*(by2-by1) - inter
    return inter / union

def yolo_to_xyxy(parts):
    _, xc, yc, w, h = [float(v) for v in parts[:5]]
    return (xc - w/2, yc - h/2, xc + w/2, yc + h/2)

if __name__ == "__main__":
    for sub in ["falszywe_pozytywy", "zle_miejsce", "przegapione"]:
        os.makedirs(os.path.join(OUT_DIR, sub), exist_ok=True)

    model = YOLO(MODEL)
    images = sorted(glob.glob(os.path.join(IMG_DIR, "*.png")))
    stats = {"fp": 0, "zle": 0, "fn": 0, "ok": 0}
    raport = []

    for img_path in images:
        name = os.path.splitext(os.path.basename(img_path))[0]
        lbl_path = os.path.join(LBL_DIR, name + ".txt")

        gt = []
        if os.path.exists(lbl_path):
            for line in open(lbl_path):
                if line.strip():
                    gt.append(yolo_to_xyxy(line.split()))

        r = model.predict(img_path, conf=CONF, verbose=False, device=0)[0]
        preds = []
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxyn[0].tolist()
            preds.append(((x1, y1, x2, y2), float(box.conf[0])))

        if not gt and preds:
            best = max(preds, key=lambda p: p[1])
            stats["fp"] += 1
            raport.append(f"FALSZYWY POZYTYW | {name} | conf={best[1]:.2f}")
            shutil.copy(img_path, os.path.join(OUT_DIR, "falszywe_pozytywy", os.path.basename(img_path)))

        elif gt and not preds:
            stats["fn"] += 1
            raport.append(f"PRZEGAPIONE     | {name}")
            shutil.copy(img_path, os.path.join(OUT_DIR, "przegapione", os.path.basename(img_path)))

        elif gt and preds:
            best_iou = max(iou(p[0], g) for p, _ in [(p, 0) for p in preds] for g in gt)
            if best_iou < IOU_PROG:
                stats["zle"] += 1
                conf = max(c for _, c in preds)
                raport.append(f"ZLE MIEJSCE     | {name} | IoU={best_iou:.2f} conf={conf:.2f}")
                shutil.copy(img_path, os.path.join(OUT_DIR, "zle_miejsce", os.path.basename(img_path)))
            else:
                stats["ok"] += 1

    with open(os.path.join(OUT_DIR, "raport.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(raport))

    print(f"Poprawne:          {stats['ok']}")
    print(f"Falszywe pozytywy: {stats['fp']}")
    print(f"Zle miejsce:       {stats['zle']}")
    print(f"Przegapione:       {stats['fn']}")
    print(f"\nSzczegoly w {OUT_DIR}/raport.txt")