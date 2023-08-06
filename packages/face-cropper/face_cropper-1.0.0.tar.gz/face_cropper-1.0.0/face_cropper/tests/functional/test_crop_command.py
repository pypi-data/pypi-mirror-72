import os
from pathlib import Path

from click.testing import CliRunner

from face_cropper.cli import crop_command


valid_saving_path = os.path.join(
    Path(__file__).parent.absolute(),
    "../samples"
)
invalid_saving_path = os.path.join(
    Path(__file__).parent.absolute(),
    "../unexisting_location"
)
valid_image_path = os.path.join(
    Path(__file__).parent.absolute(),
    "../samples/aaron_paul_bryan_cranston.jpeg"
)
invalid_image_path = os.path.join(
    Path(__file__).parent.absolute(),
    "../samples/unexisting_image.jpeg"
)


def test_crop_command_image_path_is_required():
    runner = CliRunner()
    result = runner.invoke(crop_command,
                           [f"--saving_path={valid_saving_path}"])

    assert result.exit_code == 2
    assert "Try 'crop --help' for help." in result.output
    assert "Error: Missing option '--image_path'." in result.output


def test_crop_command_saving_path_is_required():
    runner = CliRunner()
    result = runner.invoke(crop_command, [f"--image_path={valid_image_path}"])

    assert result.exit_code == 2
    assert "Try 'crop --help' for help." in result.output
    assert "Error: Missing option '--saving_path'." in result.output


def test_crop_command_output_with_invalid_image_path():
    runner = CliRunner()
    result = runner.invoke(crop_command,
                           [f"--image_path={invalid_image_path}",
                            f"--saving_path={valid_saving_path}"])

    assert result.exit_code == 1
    assert "File not found : please check on the provided image path." in result.output  # noqa: E501


def test_crop_command_output_with_invalid_saving_path():
    runner = CliRunner()
    result = runner.invoke(
        crop_command, [
            f"--image_path={valid_image_path}",
            f"--saving_path={invalid_saving_path}"
        ]
    )
    assert result.exit_code == 1
    assert "Folder not found : please check on the provided saving path." in result.output  # noqa: E501


def test_crop_command_output_non_verbose():
    runner = CliRunner()
    result = runner.invoke(
        crop_command, [
            f"--image_path={valid_image_path}",
            f"--saving_path={valid_saving_path}"
        ]
    )
    assert result.exit_code == 0
    assert f"Image correctly cropped and save in location : {valid_saving_path}" in result.output  # noqa: E501


def test_crop_command_output_verbose():
    runner = CliRunner()
    result = runner.invoke(
        crop_command, [
            f"--image_path={valid_image_path}",
            f"--saving_path={valid_saving_path}",
            f"--verbose"
        ]
    )
    assert result.exit_code == 0
    assert "Number of faces detected: 2" in result.output
    assert "Detection 1:" in result.output
    assert "Detection 2:" in result.output
    assert "Coordinates:" in result.output
    assert "Left:" in result.output
    assert "Right:" in result.output
    assert "Top:" in result.output
    assert "Bottom:" in result.output
    assert "Dimensions:" in result.output
    assert "Height:" in result.output
    assert "Width:" in result.output
    assert "Area:" in result.output
    assert f"Image correctly cropped and save in location : {valid_saving_path}" in result.output  # noqa: E501


def test_crop_command_saves_cropped_image():
    runner = CliRunner()
    runner.invoke(
        crop_command, [
            f"--image_path={valid_image_path}",
            f"--saving_path={valid_saving_path}"
        ]
    )
    assert os.path.isfile(os.path.join(
        Path(__file__).parent.absolute(),
        "../samples/aaron_paul_bryan_cranston_cropped.jpeg"
    ))
