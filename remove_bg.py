from PIL import Image
import os

def remove_white_bg(input_path, output_path, tolerance=30):
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            # item is (R, G, B, A)
            # Check if pixel is "white-ish"
            if item[0] > (255 - tolerance) and item[1] > (255 - tolerance) and item[2] > (255 - tolerance):
                newData.append((255, 255, 255, 0))  # Transparent
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Successfully saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

input_file = os.path.join("image", "WETOPLOGO.png")
output_file = os.path.join("image", "WETOPLOGO_transparent.png")

if os.path.exists(input_file):
    remove_white_bg(input_file, output_file)
else:
    print(f"File not found: {input_file}")
