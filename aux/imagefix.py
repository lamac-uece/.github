import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from PIL import Image


def on_hover(event):
    if event.inaxes is not None:
        x, y = int(event.xdata), int(event.ydata)
        pixel_value = img.getpixel((x, y))
        r, g, b, a = pixel_value
        plt.xlabel(f"X: {x}, Y: {y}\nRGB: ({r}, {g}, {b})\nAlpha: {a}")

def convert_low_alpha_pixels(image, threshold=205):
    img_data = image.getdata()
    converted_data = []

    for r, g, b, a in img_data:
        if (r, g, b) == (0, 0, 0):
            converted_data.append((r, g, b, a))  # Preserve background pixels
        elif (r > 50) and (a < threshold):
            converted_data.append((r, g, b, 255))  # Set alpha to 255
        else:
            converted_data.append((r, g, b, a))

    converted_img = Image.new(image.mode, image.size)
    converted_img.putdata(converted_data)
    return converted_img

image_path = '../profile/assets/logotipo_lamac_black-nobg.png'
img = Image.open(image_path)
thickened_img = convert_low_alpha_pixels(img)

fig, ax = plt.subplots()
ax.imshow(thickened_img)

cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

fig.canvas.mpl_connect('motion_notify_event', on_hover)

plt.title("Visualização da Imagem com Valores RGB e Canal Alfa")
plt.show()
thickened_img.save('../profile/assets/logotipo_lamac_black-fixed.png')
