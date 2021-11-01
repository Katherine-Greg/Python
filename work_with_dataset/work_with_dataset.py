from PIL import Image, ImageDraw

window = Image.new('RGB', (540, 960), (255, 255, 255))
draw = ImageDraw.Draw(window)

with open('DS4.txt', 'r') as dataset:
    for i in dataset:
        draw.point((int(i[:3]), int(i[3:])), 0)


window.show()
window.save('result.jpeg', quality=95)