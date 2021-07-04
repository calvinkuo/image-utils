"""Determine a common mode that can support multiple images."""

import warnings

from PIL import Image
import numpy as np


SUPPORTED_MODES: dict[str, set[str]] = {
    '1': {'1'},
    'L': {'1', 'L'},
    'LA': {'1', 'L', 'LA'},
    'P': set(),
    'RGB': {'1', 'L', 'P', 'RGB'},
    'PA': set(),
    'RGBA': {'1', 'L', 'LA', 'P', 'PA', 'RGB', 'RGBA'},
}
"""Modes understood by this module."""

GRAYSCALE_MODES = {'1', 'L', 'LA'}
"""Modes that are always in grayscale."""

ALPHA_CHANNEL_MODES = {'LA', 'PA', 'RGBA'}
"""Modes that have an alpha channel."""


def is_grayscale(image: Image.Image) -> bool:
    """
    Check if an image is grayscale.

    Supports RGB and RGBA images, including images with palettes.

    :param image: Image to check.
    :return: Whether the image is grayscale.
    """
    # Images in grayscale modes are always grayscale
    if image.mode in GRAYSCALE_MODES:
        return True

    # Check the image palette if applicable
    palette = image.getpalette()
    if palette is not None:
        if palette.mode in GRAYSCALE_MODES:
            return True
        elif palette.mode != 'RGB' and image.mode != 'RGBA':
            raise ValueError("Unsupported image palette mode " + palette.mode)
        else:
            # Check each color used in the image is grayscale
            colors = np.asarray(palette).reshape((-1, len(image.mode)))[:, :3]
            for index, color in enumerate(colors):
                if np.any(color[:, :] != color[:, 0]) and index in np.asarray(image):  # type: ignore
                    return False
            return True

    # Otherwise, check all pixels in the image
    if image.mode != 'RGB' and image.mode != 'RGBA':
        raise ValueError("Unsupported image mode " + image.mode)
    colors = np.asarray(image).reshape((-1, len(image.mode)))[:, :3]  # type: ignore
    if np.any(colors != np.broadcast_to(colors[:, [0]], colors.shape)):
        return False
    return True


def has_alpha(image: Image.Image) -> bool:
    """
    Check if an image has a non-opaque alpha channel.

    :param image: Image to check.
    :return: Whether the image has a non-opaque alpha channel.
    """
    # Check all pixels in the alpha channel
    if image.mode in ALPHA_CHANNEL_MODES:
        band = np.asarray(image).reshape((-1, len(image.mode)))[:, -1]  # type: ignore
        if np.any(band != np.broadcast_to(255, band.shape)):
            return True
    return False


def superset_mode(mode_1: str, mode_2: str) -> str:
    """
    Find a mode that can support all images that can be stored in both `mode_1` and `mode_2`.

    :param mode_1: First mode.
    :param mode_2: Second mode.
    :return: Mode that is a superset of both modes.
    """
    if mode_2 in SUPPORTED_MODES[mode_1]:
        return mode_1
    elif mode_1 in SUPPORTED_MODES[mode_2]:
        return mode_2

    for mode in SUPPORTED_MODES:
        if mode_1 in SUPPORTED_MODES[mode] and mode_2 in SUPPORTED_MODES[mode]:
            return mode


def determine_common_mode(*images: Image.Image) -> str:
    """
    Find a mode that can support all of the given images.

    :param images: The images to check.
    :return: A mode that is a superset of the images' modes.
    """
    common_mode = '1'
    for image in images:
        current_mode = image.mode

        # Fallbacks for unsupported modes
        if current_mode not in SUPPORTED_MODES:
            if current_mode == 'La':
                current_mode = 'LA'
            elif current_mode == 'RGBa':
                current_mode = 'RGBA'
            elif current_mode == 'I' or current_mode == 'F' or current_mode.startswith('I;'):
                current_mode = 'L'
            else:
                current_mode = 'RGB'
            warnings.warn(f"Unsupported image mode {image.mode}, converting to {current_mode}",
                          RuntimeWarning, stacklevel=2)

        # Check if the image's mode can be converted losslessly to the common mode
        if current_mode not in SUPPORTED_MODES[common_mode]:
            # Convert image in unsupported mode
            if image.mode != current_mode:
                image = image.convert(current_mode)

            # Find the actual mode of the image data
            empirical_mode = ('L' if is_grayscale(image) else 'RGB') + ('A' if has_alpha(image) else '')
            common_mode = superset_mode(common_mode, empirical_mode)
    return common_mode
