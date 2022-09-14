import argparse
import sys

import resize_new
import resize_new.compare_and_resize
from resize_new import __version__


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input_folder", help="Source directory of the images", type=str)
    parser.add_argument(
        "-out", "--output_folder", help="Directory to save resized images", type=str
    )
    parser.add_argument(
        "-log",
        "--loglevel",
        default="info",
        help="Provide logging level. Example --log debug, default=info",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"resize_new {__version__}",
    )
    return parser


def parse_command_line_args(args=None):
    parsed_args = get_parser().parse_args(args)
    return vars(parsed_args)


def main(**kwargs):
    input_folder = kwargs["input_folder"]
    output_folder = kwargs["output_folder"]
    src_dst_folder = resize_new.compare_and_resize.SrcDstFolder(input_folder, output_folder)
    resize_new.compare_and_resize.compare_and_resize(src_dst_folder)
    return 0


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`
    This function can be used as entry point to create console scripts with setuptools.
    """
    return main(**parse_command_line_args())


if __name__ == "__main__":
    sys.exit(run())
