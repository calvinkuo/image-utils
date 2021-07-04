"""Find the parameters for a levels adjustment between two images."""

import concurrent.futures

from PIL import Image
import numpy as np
from scipy.optimize import curve_fit

from level import LevelsAdjustment, level_array


def match_histogram(x: np.ndarray, y: np.ndarray, *,
                    xtol: float = 1 / 1024, samples: int = 2048) -> LevelsAdjustment:
    """
    Find the levels adjustments for arrays representing a single band by comparing quantiles of the image.
    This is roughly equivalent to the histogram plots provided in image editing software.

    For large images, this method can speed up the fit by reducing the size of the data significantly.
    Note that it does *not* take into account the position of pixels when calculating error.

    :param x: The array to be leveled, with values in the range [0, 255].
    :param y: The array to match, with values in the range [0, 255].
    :param xtol: The tolerance for the curve fit.
    :param samples: The number of quantiles to compare.
    :return: The levels adjustment for the array.
    """
    # Take quantiles and scale to [0, 1]
    xdata = np.divide(np.quantile(x, np.linspace(0, 1, samples)), 255)
    ydata = np.divide(np.quantile(y, np.linspace(0, 1, samples)), 255)

    # Find the optimal values for the parameters
    popt, pcov = curve_fit(level_array, xdata, ydata, method='dogbox', xtol=xtol,
                           p0=[0, 1, 0, 1, 1], bounds=([0, 0, 0, 0, 0], [1, 1, 1, 1, np.inf]))
    return LevelsAdjustment(*popt)


def match_array(x: np.ndarray, y: np.ndarray, *,
                xtol: float = 1 / 1024, samples: int = 2048) -> LevelsAdjustment:
    """
    Find the levels adjustments for arrays representing a single band by comparing pixels in the image.
    This is roughly equivalent to the histogram plots provided in image editing software.

    For large images, the data is sub-sampled using a histogram and fit to provide an improved initial guess.
    Note that this method *does* take into account the position of pixels when calculating error.

    :param x: The array to be leveled, with values in the range [0, 255].
    :param y: The array to match, with values in the range [0, 255].
    :param xtol: The tolerance for the curve fit.
    :param samples: The number of quantiles to compare.
    :return: The levels adjustment for the array.
    """
    # If the image size is greater than the number of samples,
    # find an initial guess based on the sub-sampled histogram
    p0 = (match_histogram(x, y, xtol=1 / 256, samples=samples)
          if x.size > samples else [0, 1, 0, 1, 1])

    # Scale to [0, 1]
    xdata = np.divide(x.ravel(), 255)
    ydata = np.divide(y.ravel(), 255)

    # Find the optimal values for the parameters
    popt, pcov = curve_fit(level_array, xdata, ydata, method='dogbox', xtol=xtol,
                           p0=p0, bounds=([0, 0, 0, 0, 0], [1, 1, 1, 1, np.inf]))
    return LevelsAdjustment(*popt)


def match_images(x: Image.Image, y: Image.Image, *, histogram: bool = False) -> list[LevelsAdjustment]:
    """
    Find the levels adjustments for each band from one image to another.

    :param x: The original image to be leveled.
    :param y: The leveled image to compare to.
    :param histogram: Whether to level the image based solely on the histogram.
    :return: A list of levels adjustments for each band.
    """
    # If dimensions do not match, resize down to match
    if x.size != y.size:
        new_size = min(x.size[0], y.size[0]), min(x.size[1], y.size[1])
        x = x.resize(new_size, resample=Image.BICUBIC)
        y = y.resize(new_size, resample=Image.BICUBIC)

    # Curve fit each band separately using multiprocessing
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if not histogram:
            match = match_array
        else:
            match = match_histogram
        futures = [executor.submit(match, np.asarray(x), np.asarray(y))
                   for x, y in zip(x.split(), y.split())]

    # Print each result
    results = [future.result() for future in futures]
    for b, adj in zip(x.getbands(), results):
        t = tuple(list(np.multiply(adj, 255))[:4] + [adj[4]])
        print(b + ":", t)  # print the parameters for each band
    return results
