from PIL import Image
from PIL.ExifTags import TAGS
import os
import stat
import time


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


file_list = list_files('egg_hunt_images_tish')
print(file_list)

for item in file_list:

    image_path = item
    metadata = get_image_metadata('egg_hunt_images_tish/' + item)

    print("Image Metadata:")
    for key, value in metadata.items():
        print(f"{key}: {value}")
