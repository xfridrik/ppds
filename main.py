import time
from math import ceil
import numpy as np
from numba import cuda
import matplotlib.pyplot as plt


@cuda.jit
def grayscale_kernel(in_img, out_img):
    row, col = cuda.grid(2)
    if row < in_img.shape[0] and col < in_img.shape[1]:
        r, g, b, a = in_img[row, col]
        out_img[row, col] = 0.2989 * r + 0.5870 * g + 0.1140 * b


def grayscale_cpu(in_img):
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
    img_gray = np.zeros((in_img.shape[0], in_img.shape[1]))

    # set tbp and bpg
    tpb = (32, 32)
    bpg = (ceil((in_img.shape[0]) / tpb[0]), ceil((in_img.shape[1]) / tpb[1]))

    # call kernel to greyscale img
    grayscale_kernel[bpg, tpb](in_img, img_gray)
    return img_gray


def main():
    # load image
    img = plt.imread("imgs/img.png")

    # run CUDA transformation
    start_time = time.time()
    gray_img = grayscale_cuda(img)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"CUDA - Elapsed time: {elapsed_time:.2f} seconds")

    # save image into file
    plt.imsave("ygray.jpg", gray_img, format="jpg", cmap='gray')

    # run CPU transformation
    start_time = time.time()
    gray_img = grayscale_cpu(img)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"CPU - Elapsed time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
