from math import ceil
import numpy as np
from numba import cuda
import matplotlib.pyplot as plt


@cuda.jit
def grayscale(in_img, out_img):
    row, col = cuda.grid(2)
    if row < in_img.shape[0] and col < in_img.shape[1]:
        r, g, b, a = in_img[row, col]
        out_img[row, col] = 0.2989 * r + 0.5870 * g + 0.1140 * b


def main():
    # load image and create array for output
    img = plt.imread("imgs/img.png")
    img_gray = np.zeros((img.shape[0], img.shape[1]))

    # set tbp and bpg
    tpb = (32, 32)
    bpg = (ceil((img.shape[0]) / tpb[0]), ceil((img.shape[1]) / tpb[1]))

    # call kernel to greyscale img
    grayscale[bpg, tpb](img, img_gray)

    # save image into file
    plt.imsave("ygray.jpg", img_gray, format="jpg", cmap='gray')


if __name__ == "__main__":
    main()
