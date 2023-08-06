from face_cropper.core import THRESHOLD_IMAGE_SIZE


class AboveThresholdException(Exception):
    """Raised when the detected face(s) are bigger than the threshold."""

    def __init__(self):
        self.message = \
            f"The face has to be less than {THRESHOLD_IMAGE_SIZE}px * {THRESHOLD_IMAGE_SIZE}px maximum"  # noqa: E501
