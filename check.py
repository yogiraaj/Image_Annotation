import cv2
import os

folder_path = r"C:\Users\Hp\Downloads\Online Assignment\Segregation\Master\dabur red toothpaste"

image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

if not image_files:
    print(f"No image files found in folder: {folder_path}")
else:
    for image_file in image_files:
        img_path = os.path.join(folder_path, image_file)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"Failed to read image: {img_path}")
        else:
            print(f"Successfully read image: {img_path}")
