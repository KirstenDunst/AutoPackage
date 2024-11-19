# 提取avg中的base64图片生成png保存本地
import os
import re
import base64
from PIL import Image
from io import BytesIO


def save_base64_image_from_svg(svg_path, output_path):
    # 读取 SVG 文件内容
    with open(svg_path, "r", encoding="utf-8") as file:
        svg_content = file.read()

    # 查找 SVG 中的 base64 图像
    match = re.search(r"data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)", svg_content)
    if match:
        # 提取 base64 数据
        base64_data = match.group(2)

        # 解码 base64 数据
        image_data = base64.b64decode(base64_data)

        # 将解码的图像数据转换为 PNG 并保存
        image = Image.open(BytesIO(image_data))
        image.save(output_path, "png")
        print(f"Image saved as {output_path}")
    else:
        print("No base64 image found in SVG file.")


if __name__ == "__main__":
    svg_dir = input("输入svg文件夹的路径:")
    svg_dir = svg_dir.removeprefix("'")
    svg_dir = svg_dir.removesuffix("'")

    save_dir = svg_dir + "/new"
    if os.path.exists(save_dir):
        os.remove(save_dir)
    os.makedirs(save_dir, exist_ok=True)

    file_list = os.listdir(svg_dir)
    for file_name in file_list:
        if file_name.endswith(".svg"):
            file_path = os.path.join(svg_dir, file_name)
            save_base64_image_from_svg(
                file_path, save_dir + "/" + file_name.replace(".svg", ".png")
            )
