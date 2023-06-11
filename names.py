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
strings = ['李语恒',
 '乔旺源',
 '庞惠铭',
 '宋佳怡',
 '樊乐天',
 '苏振宇',
 '王梁宇',
 '姚东',
 '宋雨蔓',
 '吴庆波',
 '娄晴',
 '徐子灏',
 '高镆',
 '姜樱楠',
 '阎展博',
 '于世函',
 '李怡萱',
 '于诗澳',
 '周巧冉',
 '杨颜聪',
 '李柏畅',
 '李善伊',
 '张文桦',
 '张濠亿',
 '刘雨鑫',
 '沈洁',
 '王明仁',
 '王子来',
 '潘一鸣',
 '张姝肜',
 '毕一聪',
 '王耀增',
 '丛金旺',
 '刘卓',
 '洛艺伟',
 '张潇艺',
 '李南卓阳',
 '黄卓琳',
 '崔子豪',
 '张妍',
 '焦祺',
 '张晓轩',
 '周含笑',
 '刘宇航',
 '宋智宪',
 '张日昊']

# 逐一转化为图片并保存
for i, text in enumerate(strings):
    output_path = f'{text}.png'  # 图片保存路径
    create_image_from_string(text, output_path)
    print(f'Image saved: {output_path}')
