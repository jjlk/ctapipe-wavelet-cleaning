#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on score files (stored in JSON files).
"""

import argparse
import json
import math
import os

import matplotlib.pyplot as plt
import numpy as np


def fetch_data(json_file_path):

    with open(json_file_path, "r") as fd:
        score_dict = json.load(fd)

    return score_dict


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on score files (JSON files).")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON file to process")

    args = parser.parse_args()
    json_file_path_list = args.fileargs

    # FETCH SCORE #############################################################

    result_list = []
    label_list = []

    for json_file_path in json_file_path_list:
        score_dict = fetch_data(json_file_path)
        execution_time_list = score_dict["execution_time_list"]

        execution_time_array = np.array(execution_time_list)
        result_list.append(execution_time_array)

        # METADATA

        algo_path = score_dict["algo"]
        label_list.append(os.path.splitext(os.path.basename(algo_path))[0])

    # PLOT STATISTICS #########################################################

    fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))

    meanpointprops = dict(marker='*', markeredgecolor='black', markerfacecolor='firebrick')
    whiskerprops = dict(color='k', linestyle='-')

    bp = ax1.boxplot(result_list,
                     labels=label_list,
                     meanprops=meanpointprops,
                     whiskerprops=whiskerprops,
                     #notch=True,
                     meanline=False,
                     showmeans=True)

    ax1.axhline(y=0.00003, linewidth=1, color='gray', linestyle='dashed', label=r'$30 \mu s$')  # The maximum time allowed per event on CTA

    ax1.set_yscale('log')

    ax1.legend(prop={'size': 18}, loc='upper left')

    ax1.set_title("Execution time", fontsize=20)
    ax1.set_ylabel("Execution time (seconds)", fontsize=20)

    #plt.setp(ax1.get_xticklabels(), rotation='vertical', fontsize=18)
    plt.setp(ax1.get_xticklabels(), fontsize=16)

    # Save file and plot ########

    output_file = "execution_time.pdf"

    plt.savefig(output_file, bbox_inches='tight')
    plt.show()

