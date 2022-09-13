import dataclasses
import os

import swissarmyknife.file_handling


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


def file_has_to_be_resized(src_photo, dst_photo):
    if os.path.exists(dst_photo):
        return False
    else:
        return True


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
            resize_info_single_item = ResizeInfo(src_photo, dst_photo)
            files_to_resize.append(resize_info_single_item)
    return files_to_resize


def resize_photo_to_dst_folder(src_photo, dst_photo):
    print("Src: " + src_photo)
    print("Dst: " + dst_photo)


def compare_and_resize(src_dst_folder):
    src_album_folders = get_all_folders(src_dst_folder.src)

    for folder in src_album_folders:
        resize_and_copy_if_new(folder, src_dst_folder)
