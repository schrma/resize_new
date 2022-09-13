import os

import pytest

import resize_new
import resize_new.compare_and_resize


# https://stackoverflow.com/questions/70543525/pytest-how-to-create-and-read-a-file-inside-a-test
@pytest.fixture
def output_file(tmp_path):
    # create your file manually here using the tmp_path fixture
    # or just import a static pre-built mock file
    # something like :
    target_output = os.path.join(tmp_path, "mydoc.csv")
    with open(target_output, "w+"):
        pass
    return target_output


def test_function_second(output_file):
    # with open(output_file) as ...
    pass


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

    # def test___file_has_to_be_resized(tmpdir):
    #     src_photo =
    has_to_be_resized = resize_new.compare_and_resize.file_has_to_be_resized(src_photo, dst_photo)


# def test___check_compare_and_resize___with_default_structure___expect_no_error(test_folder):
#     src_dst_folder = resize_new.compare_and_resize.SrcDstFolder(test_folder.input, test_folder.output)
#     resize_new.compare_and_resize.compare_and_resize(src_dst_folder)
