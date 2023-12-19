from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS
import numpy as np
import os
import stat
import time

def resize_image(image, target_size):
    return image.resize(target_size, Image.BICUBIC)

def calculate_ela(original_image, resized_image):
    ela = ImageChops.difference(original_image, resized_image)
    extrema = ela.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff

    ela = ImageEnhance.Brightness(ela).enhance(scale)

    return ela

def perform_ela(image_path, resave_quality=90, scale=10, threshold=228):
    # Open the original image
    original_image = Image.open(image_path).convert('RGB')

    # Get the target size for resizing
    target_size = (original_image.width // scale, original_image.height // scale)

    # Resize the original image
    resized_image = resize_image(original_image, target_size)

    # Save the resized image with reduced quality
    temp_path = 'temp_resaved_image.jpg'
    resized_image.save(temp_path, quality=resave_quality)

    # Open the resaved image
    resaved_image = Image.open(temp_path)

    # Calculate ELA
    ela = calculate_ela(original_image, resaved_image)

    # Convert ELA image to grayscale (mode 'L') before saving as JPEG
    # ela = ela.convert('L')

    # Save the ELA image
    ela_path = 'ela.png'
    ela.save(ela_path)

    # Determine if the image is manipulated based on the ELA threshold
    # ela_array = list(ela.getdata())
    max_ela_value = max(ela.getextrema()[1])
    is_manipulated = max_ela_value > threshold

    # Clean up temporary resaved image
    os.remove(temp_path)

    return is_manipulated, ela_path

def list_files(folder_path):
    try:
        # Get a list of all files in the specified folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except OSError as e:
        print(f"Error: {e}")
        return None


def get_image_metadata(image_path):
    # Get file statistics
    file_stat = os.stat(image_path)

    # Extract basic file metadata
    metadata = {
        "File Path": image_path,
        "Size (bytes)": file_stat.st_size,
        "Mode": stat.filemode(file_stat.st_mode),
        "Owner UID": file_stat.st_uid,
        "Group GID": file_stat.st_gid,
        "Last Access Time": time.ctime(file_stat.st_atime),
        "Last Modification Time": time.ctime(file_stat.st_mtime),
        "Creation Time": time.ctime(file_stat.st_ctime)
    }

    try:
        # Open the image file
        with Image.open(image_path) as img:
            # Extract image-specific metadata
            exif_data = img.getexif()
            image_metadata = {
                "Image Format": img.format,
                "Image Size": img.size,
                "Color Mode": img.mode,
                "Exif Data": "\n".join([f"{TAGS[key]}: {exif_data[key]}" for key in exif_data if key in TAGS and exif_data[key] is not None])
            }

            # Update the metadata dictionary with image-specific metadata
            metadata.update(image_metadata)

    except Exception as e:
        print(f"Error extracting image metadata: {e}")

    return metadata

def ela_test(filename):

    is_manipulated, ela_image_path = perform_ela(filename)

    if is_manipulated:
        print("The image appears to be manipulated.")
    else:
        print("The image seems to be authentic.")



file_list = list_files('egg_hunt_images_tish')
print(file_list)

for item in file_list:

    image_path = item
    metadata = get_image_metadata('egg_hunt_images_tish/' + item)

    ela_test('egg_hunt_images_tish/' + item)

    print("Image Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")

    print("-"*8)
