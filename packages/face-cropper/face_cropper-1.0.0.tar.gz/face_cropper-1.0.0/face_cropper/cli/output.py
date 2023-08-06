import dlib
from termcolor import colored


def colored_detection_output(detection: dlib.rectangle):
    """Outputs the colored detection dimensions and coordinates in CLI.

    :param detection: The detected face to be outputed
    :type detection: dlib.rectangle
    """
    height = detection.bottom() - detection.top()
    width = detection.right() - detection.left()

    print(
        f"""{colored("Coordinates:", "cyan")}
    Left: {colored(detection.left(), "magenta")}
    Right: {colored(detection.right(), "magenta")}
    Top: {colored(detection.top(),"magenta")}
    Bottom: {colored(detection.bottom(), "magenta")}
{colored("Dimensions:", "cyan")}
    Height: {colored(height, "magenta")}{colored("px", "red")}
    Width: {colored(width, "magenta")}{colored("px", "red")}
    Area: {colored(height * width, "magenta")}{colored("px", "red")}"""
    )
