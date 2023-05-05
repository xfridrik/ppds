"""
This module implements transforming images to grayscale
using GPU (CUDA) and CPU and comparing the two methods.
"""

__author__ = "Martin Fridrik, Tomáš Vavro"
__licence__ = "MIT"


import os
import time
from math import ceil
import numpy as np
from numba import cuda
import matplotlib.pyplot as plt


@cuda.jit
def grayscale_kernel(in_img, out_img):
    """
    Transform RGB into greyscale with CUDA, using grid() for position computation.
    Transformation formula source: https://stackoverflow.com/questions/12201577/how-can-i-convert-an-rgb-image-into-grayscale-in-python
    Arguments:
        in_img  -- 2D image pixels (in RGB)
        out_data -- output array for greyscale pixels
    """
    row, col = cuda.grid(2)
    if row < in_img.shape[0] and col < in_img.shape[1]:
        if len(in_img[row, col]) == 3:
            r, g, b = in_img[row, col]
        else:
            r, g, b, a = in_img[row, col]
        out_img[row, col] = 0.2989 * r + 0.5870 * g + 0.1140 * b


def grayscale_cpu(in_img):
    """
    Transform RGB into greyscale using CPU.
    Arguments:
        in_img  -- 2D image pixels (in RGB)
    Returns:
        img_gray -- image in grayscale matrix
    """
    img_gray = np.zeros((in_img.shape[0], in_img.shape[1]))
    for row in range(len(in_img)):
        for col in range(len(in_img[row])):
            if len(in_img[row, col]) == 3:
                r, g, b = in_img[row, col]
            else:
                r, g, b, a = in_img[row, col]
            img_gray[row, col] = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return img_gray


def grayscale_cuda(in_img):
    """
    Prepare params and run kernel for CUDA.
    """
    img_gray = np.zeros((in_img.shape[0], in_img.shape[1]))
    # set tbp and bpg
    tpb = (32, 32)
    bpg = (ceil((in_img.shape[0]) / tpb[0]), ceil((in_img.shape[1]) / tpb[1]))
    # call kernel to greyscale img
    grayscale_kernel[bpg, tpb](in_img, img_gray)
    return img_gray


def main():
    for image in os.listdir("imgs"):
        # load image
        img = np.array(plt.imread("imgs/"+image))
        print("--------------")
        print(f"image: {image}")

        # run CUDA grayscale transformation
        start_time = time.time()
        gray_img = grayscale_cuda(img)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"CUDA - Elapsed time: {elapsed_time:.2f} seconds")

        # save image into file
        plt.imsave("gray_imgs/gpu/"+image, gray_img, format="jpg", cmap='gray')

        # run CPU grayscale transformation
        start_time = time.time()
        gray_img = grayscale_cpu(img)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"CPU - Elapsed time: {elapsed_time:.2f} seconds")

        plt.imsave("gray_imgs/cpu/"+image, gray_img, format="jpg", cmap='gray')


if __name__ == "__main__":
    main()
