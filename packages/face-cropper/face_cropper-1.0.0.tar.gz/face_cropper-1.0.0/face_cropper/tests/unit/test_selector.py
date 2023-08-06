import dlib

from face_cropper.core.selector import select
from face_cropper.core import THRESHOLD_IMAGE_SIZE


def test_selector_selects_adequat_rectangle():
    rectangle_1 = dlib.rectangle(127, 2, 248, 120)
    rectangle_2 = dlib.rectangle(10, 2, 30, 50)
    rectangle_3 = dlib.rectangle(120, 45, 200, 110)

    selected = select([rectangle_1, rectangle_2, rectangle_3])
    assert selected == rectangle_1


def test_selector_selects_adequat_rectangle_below_threshold():
    rectangle_1 = dlib.rectangle(127, 2, 248, 120)
    rectangle_2 = dlib.rectangle(10, 2, 30, 50)
    rectangle_3 = dlib.rectangle(120, 45, 200, 110)
    rectangle_4 = dlib.rectangle(
        120,
        45,
        (120 + (THRESHOLD_IMAGE_SIZE + 1)),
        (45 + (THRESHOLD_IMAGE_SIZE + 1))
    )

    selected = select([rectangle_1, rectangle_2, rectangle_3, rectangle_4])
    assert selected == rectangle_1
