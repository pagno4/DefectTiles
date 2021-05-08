import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

CANNY = "Canny"
MEDIAN_BLUR = "Median"
GAUSSIAN_BLUR = "Gaussian"
PATH_IMAGES = "Resources/Histogram/Hist"
CRACKS = "Cracks"
BLOBS = "Blobs"


def start(img_original, filter):
    r"""
    Performs pre-processing operations
    :param img_original: image to be processed
    :param filter: type of filter to apply
    :return: pre-processed image to detect defects
    """

    # Conversion color from RGB to grayscale
    img = cv.cvtColor(img_original, cv.COLOR_BGR2GRAY)

    avg_luminance = cv.mean(img)[0]
    r"""
    Low luminance: <= 120
    Hight luminance: > 120
    """

    # Normalization
    if avg_luminance <= 120:
        img_norm = cv.normalize(img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    else:
        img_norm = cv.normalize(img, None, alpha=0, beta=120, norm_type=cv.NORM_MINMAX)

    # Applying the filter (noise reduction)
    # Median
    if filter == MEDIAN_BLUR:
        img_filt = cv.medianBlur(img_norm, 3)

    # Gaussian
    elif filter == GAUSSIAN_BLUR:
        img_filt = cv.GaussianBlur(img_norm, (3, 3), 0)

    # Bilateral filter
    else:
        img_filt = cv.bilateralFilter(img_norm, 3, 75, 75)

    img_denoised = cv.fastNlMeansDenoising(img_filt, 10, 8, 7, 21)

    # Edge Detection
    img_edge = cv.Canny(img_denoised, 50, 150)

    # Closing
    kernel = np.ones((5, 5), np.uint8)
    dilate = cv.dilate(img_edge, (3, 3))
    erode = cv.dilate(dilate, (3, 3))
    img_closing = cv.morphologyEx(erode, cv.MORPH_CLOSE, kernel)

    return img_closing


def histogram(img, file_name):
    r"""
    Create the histogram and save it.
    :param img: image of histogram to be created
    :param file_name: file name to save it
    """

    plt.title("Histogram")
    plt.xlabel("Grayscale values")
    plt.ylabel("Pixels")
    plt.xlim([0.0, 255.0])

    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.normalize(img, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)

    hist, bin_edges = np.histogram(img, bins=256, range=(0, 255))
    plt.plot(bin_edges[0:-1], hist)
    plt.savefig(PATH_IMAGES + file_name)
    plt.clf()
