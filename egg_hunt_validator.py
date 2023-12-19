# from PIL import Image
# from PIL.ExifTags import TAGS
import os
import pyexiv2

def list_files(folder_path):
    try:
        # Get a list of all files in the specified folder
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except OSError as e:
        print(f"Error: {e}")
        return None


def get_image_metadata(image_path):
    metadata = pyexiv2.ImageMetadata('test.jpg')
    metadata.read()

    # try:
    #     with Image.open(image_path) as img:
    #         metadata = {}
    #         exif_data = img._getexif()
    #
    #         if exif_data is not None:
    #             for tag, value in exif_data.items():
    #                 tag_name = TAGS.get(tag, tag)
    #                 metadata[tag_name] = value
    #
    #         return metadata
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None


file_list = list_files('egg_hunt_images_tish')
print(file_list)

for item in file_list:

    image_path = item
    get_image_metadata('egg_hunt_images_tish/' + item)

    # print("Image Metadata:")
    # for key, value in metadata.items():
    #     print(f"{key}: {value}")
