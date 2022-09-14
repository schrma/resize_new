import os
import time

import pytest

import resize_new
import resize_new.compare_and_resize


def create_temporary_file(tmp_path, filename):
    os.makedirs(tmp_path, exist_ok=True)
    target_output = os.path.join(tmp_path, filename)
    with open(target_output, "w+"):
        pass
    return target_output


def test___get_all_folders___test_folder_input___number_of_directories(test_folder):
    folders = resize_new.compare_and_resize.get_all_folders(test_folder.input)

    assert len(folders) == 11


@pytest.mark.parametrize(
    ("folder", "expected_nr_of_files"),
    (
        pytest.param("2022/2022_01/jpg", 3, id="2022_01"),
        pytest.param("2022", 0, id="Nothing"),
    ),
)
def test___get_all_photos_form_folder___test_folder_input___number_of_files(
    test_folder, folder, expected_nr_of_files
):
    photos = resize_new.compare_and_resize.get_all_photos_from_folder(
        os.path.join(test_folder.input, folder)
    )

    assert len(photos) == expected_nr_of_files


@pytest.mark.parametrize(
    ("folder", "expected_redefined_name"),
    (
        pytest.param("/test/folder/jpg", "/test/folder", id="folder with jpg in name"),
        pytest.param("/test/folder", "/test/folder", id="folder without jpg in name"),
    ),
)
def test___redefine_src_album_folder___folders___correct_redefinition(
    folder, expected_redefined_name
):
    redefined_name = resize_new.compare_and_resize.remove_jpg_folder_for_dst(folder)

    assert redefined_name == expected_redefined_name


@pytest.mark.parametrize(
    ("folder", "dst_folder", "expected_folder"),
    (
        pytest.param(
            "/root/src/2022/2022_01",
            resize_new.compare_and_resize.SrcDstFolder("/root/src/", "/root/dst/"),
            "/root/dst/2022/2022_01",
            id="Test One",
        ),
        pytest.param(
            r"D:\00-data\src\2022",
            resize_new.compare_and_resize.SrcDstFolder(r"D:\00-data\src", r"D:\00-data\dst"),
            r"D:\00-data\dst\2022",
            id="Test One",
        ),
        pytest.param(
            r"D:\00-data\src\2022",
            resize_new.compare_and_resize.SrcDstFolder(r"D:\00-data\src", r"F:\10-data\dst"),
            r"F:\10-data\dst\2022",
            id="Test One",
        ),
    ),
)
def test___convert_to_dst_folder___folders___correct_folder(folder, dst_folder, expected_folder):
    full_dst_folder = resize_new.compare_and_resize.convert_to_dst_folder(folder, dst_folder)

    assert full_dst_folder == expected_folder


@pytest.mark.parametrize(
    ("photo_filename", "dst_folder", "expected_dst_filename"),
    (
        pytest.param(
            "/root/src/2022/2022_01/jpg/test.jpg",
            resize_new.compare_and_resize.SrcDstFolder("/root/src/", "/root/dst/"),
            "/root/dst/2022/2022_01/test.jpg",
            id="Test linux with jpg folder",
        ),
        pytest.param(
            "/root/src/2022/2022_01/test.jpg",
            resize_new.compare_and_resize.SrcDstFolder("/root/src/", "/root/dst/"),
            "/root/dst/2022/2022_01/test.jpg",
            id="Test linux without jpg folder",
        ),
        pytest.param(
            r"D:\00-data\src\2022/jpg/test.jpg",
            resize_new.compare_and_resize.SrcDstFolder(r"D:\00-data\src", r"D:\00-data\dst"),
            r"D:\00-data\dst\2022/test.jpg",
            id="Test Windows with jpg folder",
        ),
        pytest.param(
            r"D:\00-data\src\2022/test.jpg",
            resize_new.compare_and_resize.SrcDstFolder(r"D:\00-data\src", r"D:\00-data\dst"),
            r"D:\00-data\dst\2022/test.jpg",
            id="Test Windows without jpg folder",
        ),
    ),
)
def test___get_dst_photo_filename___examples___correct_filename(
    photo_filename, dst_folder, expected_dst_filename
):
    dst_filename = resize_new.compare_and_resize.get_dst_photo_filename(photo_filename, dst_folder)

    assert dst_filename == expected_dst_filename


def test___dst_photo_is_older___created_files___is_older(tmp_path):
    dst_photo = create_temporary_file(os.path.join(tmp_path, "dst"), "test.jpg")
    time.sleep(1)
    src_photo = create_temporary_file(os.path.join(tmp_path, "src"), "test.jpg")

    dst_is_older = resize_new.compare_and_resize.dst_photo_is_older(src_photo, dst_photo)

    assert dst_is_older


def test___dst_photo_is_older___created_files___is_newer(tmp_path):
    src_photo = create_temporary_file(os.path.join(tmp_path, "src"), "test.jpg")
    time.sleep(1)
    dst_photo = create_temporary_file(os.path.join(tmp_path, "dst"), "test.jpg")

    dst_is_older = resize_new.compare_and_resize.dst_photo_is_older(src_photo, dst_photo)

    assert not dst_is_older


def test___file_has_to_be_resized___src_is_newer___resize(tmp_path):
    dst_photo = create_temporary_file(os.path.join(tmp_path, "dst"), "test.jpg")
    time.sleep(1)
    src_photo = create_temporary_file(os.path.join(tmp_path, "src"), "test.jpg")

    has_to_be_resized = resize_new.compare_and_resize.file_has_to_be_resized(src_photo, dst_photo)

    assert has_to_be_resized


def test___file_has_to_be_resized___dst_not_existing___resize(tmp_path):
    src_photo = create_temporary_file(os.path.join(tmp_path, "src"), "test.jpg")
    dst_photo = "test.jpg"

    has_to_be_resized = resize_new.compare_and_resize.file_has_to_be_resized(src_photo, dst_photo)

    assert has_to_be_resized


def test___file_has_to_be_resized___dst_newer___no_resize(tmp_path):
    src_photo = create_temporary_file(os.path.join(tmp_path, "src"), "test.jpg")
    time.sleep(1)
    dst_photo = create_temporary_file(os.path.join(tmp_path, "dst"), "test.jpg")

    has_to_be_resized = resize_new.compare_and_resize.file_has_to_be_resized(src_photo, dst_photo)

    assert not has_to_be_resized


def test___resize_and_copy_if_new___example_folder___correct_files(tmp_path):
    src_photo1 = create_temporary_file(os.path.join(tmp_path, "src"), "test1.jpg")
    src_photo2 = create_temporary_file(os.path.join(tmp_path, "src"), "test2.jpg")
    src_album_folder = os.path.split(src_photo1)[0]
    src_dst_folder = resize_new.compare_and_resize.SrcDstFolder(src_album_folder, r"c:/dst/")

    files_to_resize = resize_new.compare_and_resize.resize_and_copy_if_new(
        src_album_folder, src_dst_folder
    )

    assert files_to_resize[0].src.replace("/", "\\") == src_photo1
    assert files_to_resize[1].src.replace("/", "\\") == src_photo2
    assert files_to_resize[0].dst == src_dst_folder.dst + "/" + "test1.jpg"
    assert files_to_resize[1].dst == src_dst_folder.dst + "/" + "test2.jpg"


@pytest.mark.parametrize(
    ("width_org", "height_org", "width_target", "height_target"),
    (
        pytest.param(3840, 1000, 1920, 500, id="Width is bigger"),
        pytest.param(1000, 3840, 500, 1920, id="Height is bigger"),
        pytest.param(1920, 1000, 1920, 1000, id="Boarder width"),
        pytest.param(1000, 1920, 1000, 1920, id="Boarder height"),
        pytest.param(1000, 1500, 1000, 1500, id="Width and height smaller than max_target"),
    ),
)
def test___calculate_target_size___numbers___target_size(
    width_org, height_org, width_target, height_target
):
    width_calculated, height_calculated = resize_new.compare_and_resize.calculate_target_size(
        width_org, height_org
    )

    assert width_calculated == width_target
    assert height_calculated == height_target


def test___resize_photo___photo___size_reduced(test_folder):
    src_photo = os.path.join(test_folder.input, "2022/2022_02/foto2_2.JPG")
    dst_photo = os.path.join(test_folder.output, "test1.jpg")
    resize_new.compare_and_resize.resize_photo(src_photo, dst_photo)
