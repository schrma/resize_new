import dataclasses
import os
import sys
import shutil

import cv2
import pyexiv2
import swissarmyknife.file_handling
from loguru import logger

LOGGER_FORMAT = "{time} | {level} | {module} | {function} | {message}"
logger.remove()
logger.add(sys.stdout, format=LOGGER_FORMAT, level="INFO")


@dataclasses.dataclass
class SrcDstFolder:
    src: str
    dst: str


@dataclasses.dataclass
class ResizeInfo:
    src: str
    dst: str


def get_all_folders(folder):
    all_folders = [x[0] for x in os.walk(folder)]
    return all_folders


def get_all_photos_from_folder(folder):
    all_photos_without_path = swissarmyknife.file_handling.get_all_files_from_folder(
        folder, ".jpg"
    )
    suffix = folder + "/"
    all_photos = [suffix + sub for sub in all_photos_without_path]
    return all_photos


def convert_to_dst_folder(src_album_folder, src_dst_folder: SrcDstFolder):
    prefix = os.path.commonprefix([src_dst_folder.src, src_album_folder])
    folder_to_add_dst = src_album_folder.replace(prefix, "")
    if folder_to_add_dst.startswith("\\"):
        folder_to_add_dst = folder_to_add_dst[1::]
    full_dst_folder = os.path.join(src_dst_folder.dst, folder_to_add_dst)
    return full_dst_folder


def remove_jpg_folder_for_dst(src_album_folder):
    if os.path.split(src_album_folder)[1].lower() == "jpg":
        redefined_name = os.path.split(src_album_folder)[0]
    else:
        redefined_name = src_album_folder
    return redefined_name


def dst_photo_is_older(src_photo, dst_photo):
    if os.path.exists(dst_photo):
        dst_older_than_src_in_seconds = os.stat(src_photo).st_mtime - os.stat(dst_photo).st_mtime
        if dst_older_than_src_in_seconds > 0:
            return True
    return False


def dst_photo_does_not_exist(dst_photo):
    if os.path.exists(dst_photo):
        return False
    return True


def file_has_to_be_resized(src_photo, dst_photo):
    return bool(dst_photo_does_not_exist(dst_photo) or dst_photo_is_older(src_photo, dst_photo))


def get_dst_photo_filename(photo, src_dst_folder: SrcDstFolder):
    (src_album_folder, photo_name) = os.path.split(photo)
    redefined_src_album_folder = remove_jpg_folder_for_dst(src_album_folder)
    dst_folder = convert_to_dst_folder(redefined_src_album_folder, src_dst_folder)
    return dst_folder + "/" + photo_name


def find_new_photos(
    src_photos,
    dst_photos,
):
    photo_data_to_resize = list(set(src_photos).difference(set(dst_photos)))
    return photo_data_to_resize


def resize_and_copy_if_new(src_album_folder: str, src_dst_folder: SrcDstFolder):
    src_photos = get_all_photos_from_folder(src_album_folder)
    files_to_resize = []
    for src_photo in src_photos:
        dst_photo = get_dst_photo_filename(src_photo, src_dst_folder)
        if file_has_to_be_resized(src_photo, dst_photo):
            logger.info("Src: " + src_photo)
            logger.info("Dst: " + dst_photo)
            resize_info_single_item = ResizeInfo(src_photo, dst_photo)
            files_to_resize.append(resize_info_single_item)
    return files_to_resize


def check_if_file_was_loaded(image):
    try:
        image_size = image.size  # noqa
    except AttributeError as exception:
        raise FileNotFoundError from exception


def read_metadata(filename):
    with pyexiv2.Image(filename) as img:
        metadata_exif = img.read_exif()
        metadata_xmp = img.read_xmp()
    return metadata_exif, metadata_xmp


def write_metadata(filename, metadata_exif, metadata_xmp):
    with pyexiv2.Image(filename) as img:
        img.modify_exif(metadata_exif)
        for item in metadata_xmp.items():
            try:
                img.modify_xmp({item[0] : item[1] })
            except:
                pass

def write_xmp(filename, metadata):
    with pyexiv2.Image(filename) as img:
        for item in metadata:
            img.modify_xmp(item)


def shorten_xmp(metadata_xmp, caption):
    metadata = dict()
    try:
        metadata['Xmp.exif.UserComment'] = caption
        metadata['Xmp.tiff.ImageDescription'] = caption
    except:
        pass
    return metadata

def resize_photo(src_photo, dst_photo, max_target=1920):
    shutil.copy(src_photo, dst_photo)
    image = cv2.imread(dst_photo, cv2.IMREAD_UNCHANGED)

    metadata, metadata_xmp = read_metadata(dst_photo)
    try:
        check_if_file_was_loaded(image)
    except FileNotFoundError as exception:
        raise FileNotFoundError(src_photo + " not found") from exception

    height_org, width_org = image.shape[:2]

    width_target, height_target = calculate_target_size(width_org, height_org, max_target)

    # dsize
    dsize = (width_target, height_target)

    metadata['Exif.Photo.PixelXDimension'] = width_target
    metadata['Exif.Photo.PixelYDimension'] = height_target
    metadata['Exif.Image.ImageWidth'] = width_target
    metadata['Exif.Image.ImageLength'] = height_target

    caption = ''
    for my_item in metadata_xmp['Xmp.dc.subject']:
        caption = caption + my_item+ ","

    metadata['Exif.Image.ImageDescription'] = caption
    metadata[]
    # resize image
    output = cv2.resize(image, dsize)

    os.makedirs(os.path.dirname(dst_photo), exist_ok=True)

    cv2.imwrite(dst_photo, output)

    write_metadata(dst_photo, metadata, metadata_xmp)

def calculate_target_size(width_org, height_org, max_target=1920):
    if width_org > height_org:
        scale = float(max_target) / width_org
        width_target = max_target
        height_target = height_org * scale
    else:
        scale = float(max_target) / height_org
        height_target = max_target
        width_target = width_org * scale
    if scale > 1:
        width_target = width_org
        height_target = height_org
    return int(width_target), int(height_target)


def compare_and_resize(src_dst_folder):
    src_album_folders = get_all_folders(src_dst_folder.src)

    for folder in src_album_folders:
        logger.info(folder)
        files_to_resize = resize_and_copy_if_new(folder, src_dst_folder)
        for item in files_to_resize:
            resize_photo(item.src, item.dst)
