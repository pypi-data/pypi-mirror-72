import os
from pathlib import Path
from PIL import Image
import pytest

from face_cropper.core import (DLIB_FACE_DETECTING_MIN_SCORE,
                               THRESHOLD_IMAGE_SIZE)
from face_cropper.core.cropper import crop
from face_cropper.exceptions import (AboveThresholdException,
                                     NoFaceException,
                                     InvalidSavingPathException)


def test_crop_function_crops_adequatly():
    cropped = crop(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/child.jpeg"
        )
    )
    expected = Image.open(os.path.join(
        Path(__file__).parent.absolute(),
        "../samples/child_cropped.jpeg")
    )
    assert cropped.size == expected.size


def test_crop_function_saves_adequatly():
    crop(
        image_path=os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/mark_zuckerberg.jpeg"
        ),
        saving_path=os.path.join(
            Path(__file__).parent.absolute(),
            "../samples"
        )
    )
    assert os.path.isfile(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/mark_zuckerberg_cropped.jpeg"
        )
    )


def test_crop_function_without_face_raises_noface_exception():
    with pytest.raises(NoFaceException) as exception:
        crop(
            os.path.join(
                Path(__file__).parent.absolute(),
                "../samples/no_face.jpeg"
            )
        )
    assert exception.value.message == \
        f"No face has been detected on the provided image.\nIf you are sure there is one, try adjusting the precision score from dlib\nCurrent minimum score: {DLIB_FACE_DETECTING_MIN_SCORE}"  # noqa: E501


def test_crop_function_with_too_big_raises_above_threshold_exception():
    with pytest.raises(AboveThresholdException) as exception:
        crop(
            os.path.join(
                Path(__file__).parent.absolute(),
                "../samples/above_threshold.jpg"
            )
        )
    assert exception.value.message == \
        f"The face has to be less than {THRESHOLD_IMAGE_SIZE}px * {THRESHOLD_IMAGE_SIZE}px maximum"  # noqa: E501


def test_crop_function_crops_with_unexisting_file_raises_filenotfounderror():
    with pytest.raises(FileNotFoundError) as exception:
        crop(
            os.path.join(
                Path(__file__).parent.absolute(),
                "../samples/unexisting_image.jpeg"
            )
        )
    assert "File not found : please check on the provided image path." in \
        str(exception.value)


def test_crop_function_crops_with_unexisting_saving_path_raises_invalid_savingpath_exception():  # noqa: E501
    with pytest.raises(InvalidSavingPathException) as exception:
        crop(
            image_path=os.path.join(
                Path(__file__).parent.absolute(),
                "../samples/child.jpeg"
            ),
            saving_path=os.path.join(
                Path(__file__).parent.absolute(),
                "../unexisting_folder"
            )
        )
    assert exception.value.message == \
        "Folder not found : please check on the provided saving path."
