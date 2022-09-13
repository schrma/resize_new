import os

import pytest

import resize_new
import resize_new.compare_and_resize


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
    redefined_name = resize_new.compare_and_resize.redefine_src_album_folder(folder)

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
def test___get_dst_folder_out_of_src_folder___folders___correct_folder(
    folder, dst_folder, expected_folder
):
    full_dst_folder = resize_new.compare_and_resize.get_dst_folder_out_of_src_folder(
        folder, dst_folder
    )

    assert full_dst_folder == expected_folder


def test___check_compare_and_resize___with_default_structure___expect_no_error(test_folder):
    pass
