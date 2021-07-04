"""Attempt to find the parameters for a levels adjustment between two images."""

import sys
from typing import Optional

from PIL import Image

from match import match_images
from level import level_image
from modes import determine_common_mode


def main(to_level: str = "tolevel.png", to_match: str = "tomatch.png", output_filename: str = "output.png",
         input_image: Optional[str] = None, output_mode: Optional[str] = None) -> None:
    """
    Main method.

    :param to_level: The filename of the original image to be leveled.
    :param to_match: The filename of the leveled image to compare to.
    :param output_filename: The filename the leveled image should be saved to.
    :param input_image: The input image to level, if different from `to_level`.
    :param output_mode: The output image mode.
    """
    # Open each image
    to_level: Image.Image = Image.open(to_level)
    to_match: Image.Image = Image.open(to_match)
    if input_image is not None:
        input_image: Image.Image = Image.open(input_image)
    else:
        input_image: Image.Image = to_level

    # Handle images with different modes
    if output_mode is None:
        output_mode = determine_common_mode(to_level, to_match, input_image)
    if output_mode == '1':
        output_mode = 'L'  # Convert 1-bit color images to 8-bit color
    to_level = to_level.convert(output_mode)
    to_match = to_match.convert(output_mode)
    if input_image is not to_level:
        input_image = input_image.convert(output_mode)
    else:
        input_image = to_level

    # Process images
    adjustments = match_images(to_level, to_match)
    output_image = level_image(input_image, adjustments)
    output_image.save(output_filename, mode=output_mode)
    print(output_filename + " saved")


if __name__ == "__main__":
    main(*sys.argv[1:])
