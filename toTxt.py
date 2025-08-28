# 模型预测出来的图片的txt
from ultralytics import YOLO
import os

model = YOLO('/Users/yang/Desktop/yolov8_pcb.pt')

image_dir = "/Users/yang/Desktop/zhao"
output_dir = "/Users/yang/Desktop/zhao_i"
os.makedirs(output_dir, exist_ok=True)

for img_file in os.listdir(image_dir):
    if not img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
        continue
    img_path = os.path.join(image_dir, img_file)

    results = model(img_path)  # 结果是列表

    result = results[0]

    boxes = result.boxes  # Boxes对象

    # 生成YOLO格式txt文件 (class x_center y_center width height)，这里坐标是归一化的
    txt_name = os.path.splitext(img_file)[0] + '.txt'
    txt_path = os.path.join(output_dir, txt_name)

    with open(txt_path, 'w') as f:
        for box in boxes:
            cls = int(box.cls.cpu().numpy())  # 类别
            xywhn = box.xywhn.cpu().numpy().flatten()  # 归一化坐标 [x_center, y_center, width, height]
            x_center, y_center, w, h = xywhn.tolist()
            f.write(f"{cls} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
