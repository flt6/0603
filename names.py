from PIL import Image, ImageDraw, ImageFont

def create_image_from_string(text, output_path):
    # 设置图片的尺寸和背景颜色
    width = 1800
    height = 847
    background_color = (255, 255, 255)  # 白色

    # 创建一个空白图片
    image = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # 设置字体样式和大小
    font_size = 480
    font = ImageFont.truetype('DingTalk JinBuTi.ttf', font_size)

    # 计算文本在图片上的位置居中显示
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    # 在图片上绘制文本
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # 保存图片
    image.save(output_path)

# 给定的字符串列表
ipt="NAN"
strings = []
while True:
    ipt=input("Name(EOF to stop): ").strip()
    if ipt=="EOF":
        break
    strings.append(ipt)

# 逐一转化为图片并保存
for i, text in enumerate(strings):
    output_path = f'{text}.png'  # 图片保存路径
    create_image_from_string(text, output_path)
    print(f'Image saved: {output_path}')
