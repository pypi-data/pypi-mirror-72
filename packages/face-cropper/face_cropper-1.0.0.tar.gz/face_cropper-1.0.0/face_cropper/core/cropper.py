import os

from PIL import Image

from ..exceptions import (AboveThresholdException,
                          InvalidSavingPathException,
                          NoFaceException)
from .detector import detect
from .selector import select


def crop(
    image_path: str,
    saving_path: str = None,
    verbose: bool = False
):
    """Crops an image to the largest face on it.

    :param image_path: Path to access the image to be cropped
    :type image_path: str
    :param saving_path: Path to save the cropped image, defaults to None
    :type saving_path: str, optional
    :param verbose: [description], defaults to False
    :type verbose: bool, optional

    :return: The cropped image
    :rtype: [PIL.Image.Image]
    """
    try:
        detections = detect(image_path, verbose)
    except RuntimeError:
        raise FileNotFoundError(
            "File not found : please check on the provided image path."
        )
    if len(detections) == 0:
        raise NoFaceException

    selected_detection = select(detections, verbose)
    if selected_detection is None:
        raise AboveThresholdException

    cropping_coordinates = (
        selected_detection.left(),
        selected_detection.top(),
        selected_detection.right(),
        selected_detection.bottom()
    )

    with Image.open(image_path) as non_cropped_image:
        cropped_image = non_cropped_image.crop(cropping_coordinates)
        filepath = os.path.basename(non_cropped_image.filename)
        filename, extension = os.path.splitext(filepath)
        if saving_path is not None:
            try:
                cropped_image.save(
                    os.path.join(
                        saving_path,
                        f"{filename}_cropped{extension}"
                    )
                )
            except FileNotFoundError:
                raise InvalidSavingPathException
        return cropped_image
