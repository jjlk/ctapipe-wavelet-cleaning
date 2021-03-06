#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Denoise FITS and PNG images with the tailcut algorithm.

Example usages:
  ./denoising_with_tailcut.py -h
  ./denoising_with_tailcut.py -T 0.5 -t 0.1 ./test.fits
  ./denoising_with_tailcut.py -T 0.5 -t 0.1 ./test.fits
  ipython3 -- ./denoising_with_tailcut.py -t 0.0001 -s ./test.fits

This snippet requires Numpy, Matplotlib and PIL/Pillow Python libraries.
"""

import argparse
import datetime
import json
import os
import numpy as np
import time

import datapipe.denoising
from datapipe.denoising.abstract_cleaning_algorithm import AbstractCleaningAlgorithm
from datapipe.benchmark import assess
from datapipe.io import images


import matplotlib.pyplot as plt
from matplotlib import cm

# DEBUG PLOT FUNCTION #########################################################

def debug_plot(img, high_mask, final_mask, title=""):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title("Original image")

    im1 = ax.imshow(img,
                   origin='lower',
                   interpolation='nearest',
                   vmin=min(img.min(), 0),
                   cmap="gray")

    plt.colorbar(im1) # draw the colorbar

    #plt.show()
    plt.savefig("tailcut_original.pdf", bbox_inches='tight')
    plt.close('all')

    ###########################################################################
    
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title("First threshold")

    im1 = ax.imshow(img,
                   origin='lower',
                   interpolation='nearest',
                   vmin=min(img.min(), 0),
                   cmap="gray",
                   alpha=0.5)

    # http://stackoverflow.com/questions/17170229/setting-transparency-based-on-pixel-values-in-matplotlib
    mask = np.ma.masked_where(high_mask < 0.9, high_mask) # TODO

    im = ax.imshow(mask,
                   origin='lower',
                   interpolation='nearest',
                   vmin=0,
                   cmap="Reds",
                   alpha=0.8)

    plt.colorbar(im1) # draw the colorbar

    #plt.show()
    plt.savefig("tailcut_1st_threshold.pdf", bbox_inches='tight')
    plt.close('all')

    #########################################################################
    
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.set_title("Second threshold")

    im1 = ax.imshow(img,
                   origin='lower',
                   interpolation='nearest',
                   vmin=min(img.min(), 0),
                   cmap="gray",
                   alpha=0.5)

    mask = np.ma.masked_where(high_mask < 0.9, high_mask) # TODO

    im = ax.imshow(mask,
                   origin='lower',
                   interpolation='nearest',
                   vmin=0,
                   cmap="Reds",
                   alpha=0.5)

    neighbors_mask = final_mask - high_mask

    mask = np.ma.masked_where(neighbors_mask < 0.9, neighbors_mask) # TODO

    im = ax.imshow(mask,
                   origin='lower',
                   interpolation='nearest',
                   vmin=0,
                   cmap="Greens",
                   alpha=0.8)

    plt.colorbar(im1) # draw the colorbar

    #plt.show()
    plt.savefig("tailcut_2nd_threshold.pdf", bbox_inches='tight')
    plt.close('all')


# TAILCUT #####################################################################

class Tailcut(AbstractCleaningAlgorithm):

    def __init__(self):
        super(Tailcut, self).__init__()
        self.label = "Tailcut (JD)"  # Name to show in plots

    def clean_image(self, img, high_threshold=10., low_threshold=5.,
                    base_file_path="tailcut_jd", output_data_dict=None):

        # COMPUTE MASKS #######################################

        high_mask = (img >= high_threshold)
        low_mask =  (img >= low_threshold)

    #    images.plot(high_mask, title="High mask")
    #    images.plot(low_mask, title="Low mask")

        # MERGE MASKS #########################################

        # Dilate the high_mask to create a mask of neighbors.
        # For instance, if high_mask is equals to:
        #    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 1, 0, 0, 0, 1, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        # the dilated version of high_mask is equals to:
        #    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        #     [0, 1, 1, 1, 0, 1, 1, 1, 0],
        #     [0, 1, 1, 1, 0, 1, 1, 1, 0],
        #     [0, 1, 1, 1, 0, 1, 1, 1, 0],
        #     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        high_mask_dilated = np.zeros(high_mask.shape, dtype=np.bool)
        high_mask_dilated[:] = high_mask

        high_mask_dilated[:-1,:] |= high_mask[1:,:]    # shift up
        high_mask_dilated[1:,:]  |= high_mask[:-1,:]   # shift down

        high_mask_dilated[:,:-1] |= high_mask_dilated[:,1:]   # shift left
        high_mask_dilated[:,1:]  |= high_mask_dilated[:,:-1]  # shift right

        # Merge high_mask_dilated and low_mask (using a logical AND)

        final_mask = high_mask_dilated & low_mask

        # PLOT MASK ###########################################

        if self.verbose:
            images.plot(final_mask, title="Tailcut mask")
            images.mpl_save(final_mask,
                            "{}_tailcut_mask.pdf".format(base_file_path),
                            title="Tailcut mask")

        #debug_plot(img, high_mask, final_mask, title="Tailcut mask")

        # APPLY MASK ##########################################

        cleaned_img = img * final_mask

        return cleaned_img


def main():

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Denoise FITS images with the tailcut algorithm.")

    parser.add_argument("--benchmark", "-b", metavar="STRING", 
                        help="The benchmark method to use to assess the algorithm for the"
                             "given images")

    parser.add_argument("--high_threshold", "-T", type=float, default=0, metavar="FLOAT", 
                        help="The 'high' threshold value (between 0 and 1)")

    parser.add_argument("--low_threshold", "-t", type=float, default=0, metavar="FLOAT", 
                        help="The 'low' threshold value (between 0 and 1)")

    parser.add_argument("--plot", action="store_true",
                        help="Plot images")

    parser.add_argument("--saveplot", default=None, metavar="FILE",
                        help="The output file where to save plotted images")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path (JSON)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The files image to process (FITS)."
                             "If fileargs is a directory,"
                             "all FITS files it contains are processed.")

    args = parser.parse_args()

    benchmark_method = args.benchmark
    high_threshold = args.high_threshold
    low_threshold = args.low_threshold
    plot = args.plot
    saveplot = args.saveplot
    input_file_or_dir_path_list = args.fileargs

    if args.output is None:
        output_file_path = "score_tailcut_jd_benchmark_{}.json".format(benchmark_method)
    else:
        output_file_path = args.output

    cleaning_function_params = {"high_threshold": high_threshold, "low_threshold": low_threshold}

    cleaning_algorithm = Tailcut()
    cleaning_algorithm.run(cleaning_function_params,
                           input_file_or_dir_path_list,
                           benchmark_method,
                           output_file_path,
                           plot,
                           saveplot)


if __name__ == "__main__":
    main()

