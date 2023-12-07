import sys


def get_pixel_from_decimal(value):
    pixel = 0
    return pixel


x_hex = '0x' + str(sys.argv[1])
y_hex = '0x' + str(sys.argv[2])
x_decimal = int(x_hex, 16)
y_decimal = int(y_hex, 16)

x_pixel = round((x_decimal / 65535) * 1080) * 2

y_pixel = round((y_decimal / 65535) * 2220) * 2
print(x_pixel, y_pixel)
