from PIL import Image, ImageDraw

window = Image.new('RGB', (960, 960), (255, 255, 255))
draw = ImageDraw.Draw(window)

with open('C:\\Users\\user\\Desktop\\Old_Storage\\Python\\affine_transformation\\DS4.txt', 'r') as dataset:
    for i in dataset:
        draw.point((int(i[:3]), int(i[3:])), fill='blue')

rotate_image = window.rotate(50, center = (480, 480))

rotate_image.save('C:\\Users\\user\\Desktop\\Old_Storage\\Python\\affine_transformation\\result.jpg', quality = 95)


