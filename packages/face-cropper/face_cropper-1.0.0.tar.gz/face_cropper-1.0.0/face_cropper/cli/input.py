import sys

import click
from termcolor import colored

from face_cropper.core.cropper import crop
from face_cropper.exceptions import (AboveThresholdException,
                                     InvalidSavingPathException,
                                     NoFaceException)


@click.command(name="crop")
@click.option(
    "--image_path",
    help="Path to the image to be cropped.",
    required=True
)
@click.option(
    "--saving_path",
    help="If provided, cropped image will be saved in the provided location",
    required=True
)
@click.option(
    "--verbose/--non-verbose",
    help="Command should output informations.",
    default=False
)
def crop_command(
        image_path: str,
        saving_path: str = None,
        verbose: bool = False):
    """Calls crop function from CLI.

    :param image_path: Path to access the image to be cropped
    :type image_path: str
    :param saving_path: Path to save the cropped image, defaults to None
    :type saving_path: str, optional
    :param verbose: [description], defaults to False
    :type verbose: bool, optional
    """
    try:
        crop(image_path, saving_path, verbose)
        print(
            colored(
                f"Image correctly cropped and save in location : {saving_path}"
            )
        )
    except (AboveThresholdException, InvalidSavingPathException,
            NoFaceException, FileNotFoundError) as exception:
        if isinstance(exception, FileNotFoundError):
            sys.exit(colored(exception, "red"))
        sys.exit(colored(exception.message, "red"))
