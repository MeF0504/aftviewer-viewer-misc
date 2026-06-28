import os
from logging import getLogger
from pathlib import Path
import argparse

from aftviewer import (GLOBAL_CONF, Args, show_image_ndarray, help_template,
                       add_args_imageviewer)
from pymeflib import xpm_loader
from pymeflib.xpm_loader import XPMLoader
logger = getLogger(GLOBAL_CONF.logname)
if 'numpy' in GLOBAL_CONF.pack_list:
    use_numpy = True
else:
    use_numpy = False


def add_args(parser: argparse.ArgumentParser):
    add_args_imageviewer(parser)
    parser.add_argument('--make', help='force make the library.',
                        action='store_true')


def show_help():
    helpmsg = help_template('xpm', 'show an xpm file as an image.', add_args)
    print(helpmsg)


def main(fpath: Path, args: Args) -> int:
    if args.make:
        xpm_loader._update_lib = True
    xpm = XPMLoader(fpath, logger=logger)
    if use_numpy:
        xpm.xpm_to_ndarray()
        data = xpm.ndarray
    else:
        xpm.xpm_to_list()
        data = xpm.rgb_list

    ret = show_image_ndarray(data, os.path.basename(fpath), args)
    if ret is None:
        return 3
    elif ret:
        return 0
    else:
        return 2
