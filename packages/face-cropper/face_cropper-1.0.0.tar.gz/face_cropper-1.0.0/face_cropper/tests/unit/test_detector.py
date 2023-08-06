import os
from pathlib import Path

from face_cropper.core.detector import detect


def test_detector_detects_no_face():
    detection = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/no_face.jpeg"
        )
    )
    assert len(detection) == 0

    detection = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/arthur_fleck.jpg"
        )
    )
    assert len(detection) == 1


def test_detector_detects_one_face():
    detection = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/vincent_cassel.jpg"
        )
    )
    assert len(detection) == 1

    detection = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/arthur_fleck.jpg"
        )
    )
    assert len(detection) == 1


def test_detector_detects_two_faces():
    detections = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/aaron_paul_bryan_cranston.jpeg"
        )
    )
    assert len(detections) == 2

    detections = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/obama_michelle.jpeg"
        )
    )
    assert len(detections) == 2


def test_detector_detects_many_faces():
    detections = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/peaky_blinders.jpg"
        )
    )
    assert len(detections) == 3

    detections = detect(
        os.path.join(
            Path(__file__).parent.absolute(),
            "../samples/vikings.png"
        )
    )
    assert len(detections) == 3
