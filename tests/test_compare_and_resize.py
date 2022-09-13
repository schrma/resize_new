import os

import pytest

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


def test___check_compare_and_resize___with_default_structure___expect_no_error(test_folder):
    resize_new.compare_and_resize.compare_and_resize(test_folder.input, test_folder.output)
