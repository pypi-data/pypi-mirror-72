from face_cropper.core import DLIB_FACE_DETECTING_MIN_SCORE


class NoFaceException(Exception):
    """Raised when no face has been found in the provided image."""

    def __init__(self):
        self.message = \
            f"No face has been detected on the provided image.\nIf you are sure there is one, try adjusting the precision score from dlib\nCurrent minimum score: {DLIB_FACE_DETECTING_MIN_SCORE}"  # noqa: E501
