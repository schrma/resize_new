import resize_new.compare_and_resize


def test___get_all_folders___test_folder_input___number_of_directories(test_folder):
    folders = resize_new.compare_and_resize.get_all_folders(test_folder.input)
    assert len(folders) == 11


def test___check_compare_and_resize___with_default_structure___expect_no_error(test_folder):
    resize_new.compare_and_resize.compare_and_resize(test_folder.input, test_folder.output)
