"""Adjust the levels of an image."""

from typing import NamedTuple

from PIL import Image
import numpy as np


class LevelsAdjustment(NamedTuple):
    """
    Levels adjustment settings for a single band.

    :param input_black: The black point of the input band, in the range [0, 1].
    :param input_white: The white point of the input band, in the range [0, 1].
    :param output_black: The black point of the output band, in the range [0, 1].
    :param output_white: The white point of the output band, in the range [0, 1].
    :param gamma: The gamma adjustment, in the range (0, inf).
    """
    input_black: float
    input_white: float
    output_black: float
    output_white: float
    gamma: float


def level_array(array: np.ndarray, input_black: float, input_white: float,
                output_black: float, output_white: float, gamma: float) -> np.ndarray:
    """
    Apply the specified levels adjustment to an array representing a single band.

    :param array: The input array, with values in the range [0, 1].
    :param input_black: The black point of the input band, in the range [0, 1].
    :param input_white: The white point of the input band, in the range [0, 1].
    :param output_black: The black point of the output band, in the range [0, 1].
    :param output_white: The white point of the output band, in the range [0, 1].
    :param gamma: The gamma adjustment, in the range (0, inf).
    :return: The output array, with values in the range [0, 1].
    """
    # return np.clip(np.add(np.multiply(output_white - output_black, np.power(np.clip(np.divide(np.subtract(array,
    #            input_black), input_white - input_black), 0, 1), gamma)), output_black), 0, 1)
    return np.clip(np.clip((array - input_black) / (input_white - input_black), 0, 1) ** gamma
                   * (output_white - output_black) + output_black, 0, 1)


def level_image(image: Image.Image, adjustments: list[LevelsAdjustment]) -> Image.Image:
    """
    Apply the specified levels adjustments to each band of an image.

    :param image: The input image, with values in the range [0, 255].
    :param adjustments: The levels adjustments to apply for each band.
    :return: The output image, with values in the range [0, 255].
    """
    table = np.concatenate([np.rint(np.multiply(level_array(np.linspace(0, 1, 256), *t), 255)) for t in adjustments])
    return image.point(table)
