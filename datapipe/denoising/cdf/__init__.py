#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Jérémie DECOCK (http://www.jdhp.org)

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

import os

PACKAGE_PATH = os.path.split(__file__)[0]

ASTRI_GAMMA_CDF_FILE = os.path.join(PACKAGE_PATH, 'astri_inaf_cdf_gamma.json')
GCT_GAMMA_CDF_FILE = os.path.join(PACKAGE_PATH, 'gct_konrad_cdf_gamma.json')
DIGICAM_GAMMA_CDF_FILE = os.path.join(PACKAGE_PATH, 'digicam_konrad_cdf_gamma.json')
FLASHCAM_GAMMA_CDF_FILE = os.path.join(PACKAGE_PATH, 'flashcam_grid_prod3b_north_cdf_gamma.json')
NECTARCAM_GAMMA_CDF_FILE = os.path.join(PACKAGE_PATH, 'nectarcam_grid_prod3b_north_cdf_gamma.json')
LSTCAM_GAMMA_CDF_FILE = os.path.join(PACKAGE_PATH, 'lstcam_grid_prod3b_north_cdf_gamma.json')

ASTRI_PROTON_CDF_FILE = os.path.join(PACKAGE_PATH, 'astri_inaf_cdf_proton.json')
GCT_PROTON_CDF_FILE = os.path.join(PACKAGE_PATH, 'gct_konrad_cdf_proton.json')
DIGICAM_PROTON_CDF_FILE = os.path.join(PACKAGE_PATH, 'digicam_konrad_cdf_proton.json')
FLASHCAM_PROTON_CDF_FILE = os.path.join(PACKAGE_PATH, 'flashcam_grid_prod3b_north_cdf_proton.json')
NECTARCAM_PROTON_CDF_FILE = os.path.join(PACKAGE_PATH, 'nectarcam_grid_prod3b_north_cdf_proton.json')
LSTCAM_PROTON_CDF_FILE = os.path.join(PACKAGE_PATH, 'lstcam_grid_prod3b_north_cdf_proton.json')

ASTRI_CDF_FILE = ASTRI_GAMMA_CDF_FILE
GCT_CDF_FILE = GCT_GAMMA_CDF_FILE
DIGICAM_CDF_FILE = DIGICAM_GAMMA_CDF_FILE
FLASHCAM_CDF_FILE = FLASHCAM_GAMMA_CDF_FILE
NECTARCAM_CDF_FILE = NECTARCAM_GAMMA_CDF_FILE
LSTCAM_CDF_FILE = LSTCAM_GAMMA_CDF_FILE

__all__ = ['ASTRI_CDF_FILE',
           'GCT_CDF_FILE',
           'DIGICAM_CDF_FILE',
           'FLASHCAM_CDF_FILE',
           'NECTARCAM_CDF_FILE',
           'LSTCAM_CDF_FILE']
