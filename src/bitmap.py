import struct

def make_bitmap(file_path:str, width:int, height:int, pixel_data:list[int]):
    with open(file_path, "wb") as file:
        pad = 0
        if (width * 3) % 4 != 0:
           pad = 4 - (width * 3) % 4 
        row = width * 3 + pad
        data_size = row * height
        file_size = data_size + 54  # header=54b

        # insert padding
        pixel_array = []
        for i in range(height):
            start = i * width * 3
            end = (i + 1) * width * 3
            pixel_array.extend(pixel_data[start:end])
            pixel_array.extend([0]*pad)

        # BMP header
        file.write(bytearray([0x42, 0x4d]))             #   2   BM              ID field
        file.write(struct.pack("i", file_size))         #   4   54 + data       size of BMP file
        file.write(bytearray([0x00, 0x00]))             #   2   Unused          App specific
        file.write(bytearray([0x00, 0x00]))             #   2   Unused          App specific
        file.write(bytearray([0x36, 0x00, 0x00, 0x00])) #   4   54B (14+40)     offset to pixel array

        # DIB header
        file.write(bytearray([0x28, 0x00, 0x00, 0x00])) #   4   40B             DIB header size
        file.write(struct.pack("i", width))             #   4   width (L->R)   BMP width in pixels
        file.write(struct.pack("i", height))            #   4   height (B->U)  BMP height in pixels (positive bottom -> top)
        file.write(bytearray([0x01, 0x00]))             #   2   1 plane         number of color planes
        file.write(bytearray([0x18, 0x00]))             #   2   24 bpp          number of bits per pixel 
        file.write(bytearray([0x00, 0x00, 0x00, 0x00])) #   4   0               BI_RGB, no pixel array compression
        file.write(struct.pack("i", data_size))         #   4   data            size of raw bmp data (including padding)
        # 72 DPI
        file.write(bytearray([0x13, 0x0b, 0x00, 0x00])) #   4   2835ppm         horizontal print resolution (pixels per meter)
        file.write(bytearray([0x13, 0x0b, 0x00, 0x00])) #   4   2835ppm         vertical print resolution (pixels per meter)
        file.write(bytearray([0x00, 0x00, 0x00, 0x00])) #   4   0 colors        number of colors in palette
        file.write(bytearray([0x00, 0x00, 0x00, 0x00])) #   4   0 all           number of important colors

        # pixel array
        file.write(bytearray(pixel_array))


if __name__ == "__main__":
    width = 0xff
    height = 0xff
    pixel_data = []
    for r in range(height):
        for g in range(width):
            pixel_data.extend([0x00, g, r])
    make_bitmap("test.bmp", width, height, pixel_data)

