import resize_new.compare_and_resize


def test___check_compare_and_resize___with_default_structure___expect_no_error(test_folder):
    resize_new.compare_and_resize.compare_and_resize(test_folder.input, test_folder.output)