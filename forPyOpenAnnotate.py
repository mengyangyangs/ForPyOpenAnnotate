import os
from PIL import Image

# 路径配置
norm_labels_dir = "/Users/yang/Desktop/labels"     # YOLO格式标注目录（归一化坐标）
image_dir = "/Users/yang/Desktop/zhao"             # 对应图片目录
output_dir = "/Users/yang/Desktop/zhao_abs"        # 输出绝对坐标标注目录

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def yolo_to_abs_coords(yolo_file_path, img_size):
    w_img, h_img = img_size
    output_lines = []

    with open(yolo_file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            parts = line.strip().split()
            if len(parts) != 5:
                print(f"[⚠️ 跳过无效行 {line_num}] {line.strip()}")
                continue

            try:
                class_id = int(parts[0])
                x_center, y_center, w_box, h_box = map(float, parts[1:])
            except ValueError:
                print(f"[❌ 数据格式错误，跳过行 {line_num}]: {line.strip()}")
                continue

            # YOLO归一化 → 绝对坐标
            xmin = int((x_center - w_box / 2) * w_img)
            xmax = int((x_center + w_box / 2) * w_img)
            ymin = int((y_center - h_box / 2) * h_img)
            ymax = int((y_center + h_box / 2) * h_img)

            # 坐标裁剪，防止越界
            xmin = max(0, xmin)
            ymin = max(0, ymin)
            xmax = min(w_img - 1, xmax)
            ymax = min(h_img - 1, ymax)

            if xmax <= xmin or ymax <= ymin:
                print(f"[⚠️ 跳过无效框] 第{line_num}行，坐标: {xmin},{ymin},{xmax},{ymax}")
                continue

            output_lines.append(f"{class_id} {xmin} {ymin} {xmax} {ymax}")
            print(f"✅ 转换: class={class_id}, xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")

    return output_lines

def convert_all():
    for fname in os.listdir(norm_labels_dir):
        if not fname.endswith(".txt"):
            continue
        base = os.path.splitext(fname)[0]

        # 支持 .jpg 和 .png
        img_path = None
        for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
            test_path = os.path.join(image_dir, base + ext)
            if os.path.exists(test_path):
                img_path = test_path
                break

        if not img_path:
            print(f"[❌ 错误] 找不到对应图片: {base}")
            continue

        try:
            with Image.open(img_path) as img:
                w, h = img.size
        except Exception as e:
            print(f"[❌ 打开图片失败] {img_path}，错误: {e}")
            continue

        print(f"📷 处理图片: {img_path}，尺寸: {w}x{h}")

        yolo_path = os.path.join(norm_labels_dir, fname)
        converted = yolo_to_abs_coords(yolo_path, (w, h))

        out_path = os.path.join(output_dir, fname)
        with open(out_path, 'w') as f:
            for line in converted:
                f.write(line + "\n")

        print(f"💾 写入完成: {out_path}")

if __name__ == "__main__":
    convert_all()
