import os
import cv2
import shutil

def compare_images(image1, image2):

    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Calculate histograms
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    hist1 = cv2.normalize(hist1, hist1)
    hist2 = cv2.normalize(hist2, hist2)

    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity > 0.9

def validate_images(master_folder, data_folder, dump_folder, subfolder_names):

    master_images = {}
    for subfolder_name in subfolder_names:
        subfolder_path = os.path.join(master_folder, subfolder_name)
        if not os.path.isdir(subfolder_path):
            print(f"Subfolder '{subfolder_name}' does not exist in the Master folder. Skipping...")
            continue

        reference_image = None
        for file_name in os.listdir(subfolder_path):
            file_path = os.path.join(subfolder_path, file_name)
            if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                reference_image = cv2.imread(file_path)
                master_images[subfolder_name] = reference_image
                print(f"Reference image found for '{subfolder_name}': {file_name}")
                break
        
        if reference_image is None:
            print(f"No reference image found in subfolder '{subfolder_name}'. Skipping...")

    for subfolder_name in subfolder_names:
        subfolder_path = os.path.join(data_folder, subfolder_name)
        if not os.path.isdir(subfolder_path):
            print(f"Subfolder '{subfolder_name}' does not exist in the Data folder. Skipping...")
            continue

        if subfolder_name not in master_images:
            print(f"No reference image for '{subfolder_name}'. Skipping...")
            continue

        reference_image = master_images[subfolder_name]
        for image_name in os.listdir(subfolder_path):
            image_path = os.path.join(subfolder_path, image_name)
            image = cv2.imread(image_path)
            
            if image is None or not compare_images(reference_image, image):
                # Move mismatched image to Dump folder
                os.makedirs(dump_folder, exist_ok=True)
                dump_path = os.path.join(dump_folder, image_name)
                shutil.move(image_path, dump_path)
                print(f"Moved mismatched image: {image_name} -> {dump_folder}")
    
    print("Validation and organization complete.")

master_folder = "C:\\Users\\Hp\\Downloads\\Online Assignment\\Segregation\\Master"
data_folder = "C:\\Users\\Hp\\Downloads\\Online Assignment\\Segregation\\Data"
dump_folder = "C:\\Users\\Hp\\Downloads\\Online Assignment\\Segregation\\Dump"
subfolder_names = [
    "RealGuavaJuice1L",
    "glucon-d-all flavours",
    "dabur red toothpaste",
    "dabur herbal"
]

validate_images(master_folder, data_folder, dump_folder, subfolder_names)
