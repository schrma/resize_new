

def get_all_folders(folder):
    all_folders = ["folder1", "folder2", "folder3"]
    return all_folders


def get_all_photos_from_folder(folder):
    all_photos = ["Foto1", "Foto2"]
    return all_photos


def folder_exists_in_dst(src_album_folder, dst_folder):
    return True


def get_dst_folder_out_of_src_folder(src_album_folder, dst_folder):
    return "dst_folder"


def folder_exists(folder):
    return True


def redefine_src_album_folder(src_album_folder):
    redefined_name = src_album_folder
    return redefined_name


def find_new_photos(src_photos, dst_photos,):
    photo_data_to_resize = "Ok"
    return photo_data_to_resize


def get_photos_to_resize(src_album_folder, dst_folder):
    redefined_src_album_folder = redefine_src_album_folder(src_album_folder)
    dst_folder = get_dst_folder_out_of_src_folder(redefined_src_album_folder, dst_folder)
    dst_photos = []
    src_photos = get_all_photos_from_folder(src_album_folder)
    if folder_exists(dst_folder):
        dst_photos = get_all_photos_from_folder(redefined_src_album_folder)
    photo_data_to_resize = find_new_photos(src_photos, dst_photos)
    return photo_data_to_resize


def has_to_be_resized_or_created(photo, dst_photos):
    return True


def resize_photo(photo_data_to_resize):
    pass


def compare_and_resize(src_folder, dst_folder):
    src_album_folders = get_all_folders(src_folder)

    for folder in src_album_folders:
        photo_data_to_resize = get_photos_to_resize(folder, dst_folder)
        resize_photo(photo_data_to_resize)



