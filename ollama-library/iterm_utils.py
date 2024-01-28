import base64

def display_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        print(f'\x1b]1337;File=inline=1:{encoded_string}\a')