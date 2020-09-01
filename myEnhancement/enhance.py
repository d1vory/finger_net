import cv2
import numpy as np

from skimage.filters import gabor_kernel

def invertImage(img):
    mean = np.mean(img)
    _, inverted = cv2.threshold(img, mean, 255, 0)
    return inverted

def equalizeHistogram(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(img)
    return cl1

def bankGabor(ksize, sigma = 4):
    filters = []
    freqs = [1/5, 1/7, 1/9]
    for f in freqs:
        for theta in np.arange(0, np.pi, np.pi / 8):
            filters.append(np.real(gabor_kernel(frequency= f, theta=theta,
                                          sigma_x=sigma, sigma_y=sigma, n_stds=ksize)))

    return filters



def apply_filter_bank(img, filter_bank):
    filtered_images = []
    img_acc = np.zeros_like(img)
    for fb in filter_bank:
        img_p = cv2.filter2D(img, cv2.CV_8UC3, fb)
        filtered_images.append(img_p)
        np.maximum(img_acc, img_p, img_acc)

    return filtered_images, img_acc


def enhanceImage(img):
    eq = equalizeHistogram(img)
    filterBank = bankGabor(2)
    _, filtered = apply_filter_bank(eq, filterBank)
    inverted = invertImage(filtered)

    return inverted

