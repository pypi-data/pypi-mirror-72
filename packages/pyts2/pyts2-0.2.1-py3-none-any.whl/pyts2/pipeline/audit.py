# Copyright (c) 2018 Kevin Murray <kdmfoss@gmail.com>
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ..time import *
from ..utils import *
from ..timestream import *
from .base import *
from .imageio import *

import numpy as np
import zbarlight
import skimage as ski
from skimage.color import rgb2lab
import piexif
from math import log2


class ImageMeanColourException(Exception):
    pass


class ImageMeanColourStep(PipelineStep):

    def process_file(self, file):
        assert hasattr(file, "pixels")  # TODO proper check
        pix = file.pixels
        if len(pix.shape) == 2:  # Greyscale
            meancol = pix.mean()
            file.report.update({"ImageMean_Grey": meancol})
        elif len(pix.shape) == 3:  # Colour
            meanrgb = pix.mean(axis=(0, 1))
            file.report.update({"ImageMean_Red": meanrgb[0],
                                "ImageMean_Green": meanrgb[1],
                                "ImageMean_Blue": meanrgb[2]})

            # Hack: dont' calculate the whole L*a*b matrix, just Lab-ify the
            # precomputed mean value. I think this is the same???
            # meanlab = file.Lab.mean(axis=(0,1))  # this uses even more RAM
            meanimg = meanrgb[np.newaxis, np.newaxis, :]  # extra pretend axes for skimage
            meanlab = rgb2lab(meanimg).mean(axis=(0, 1))
            file.report.update({"ImageMean_L": meanlab[0],
                                "ImageMean_a": meanlab[1],
                                "ImageMean_b": meanlab[2]})
        else:
            raise ImageMeanColourException("Invalid pixel matrix shape")
        return file


class ScanQRCodesStep(PipelineStep):

    def process_file(self, file):
        assert hasattr(file, "pixels")  # TODO proper check
        codes = zbarlight.scan_codes('qrcode', file.pil)
        if codes is not None:
            codes = ';'.join(sorted(x.decode('utf8') for x in codes))
        file.report.update({"QRCodes": codes})
        return file

def rat2float(x):
    n, d = x
    return float(n)/float(d)

class CalculateEVStep(PipelineStep):

    def process_file(self, file):
        md = piexif.load(file.content)
        try:
            ss = md['Exif'][piexif.ExifIFD.ExposureTime]
            fs = md['Exif'][piexif.ExifIFD.FNumber]
            iso = md['Exif'][piexif.ExifIFD.ISOSpeedRatings]
            #print(ss, rat2float(ss), fs, rat2float(fs), iso)
            ev = log2((rat2float(fs) ** 2)/rat2float(ss)) - log2(float(iso)/100)
            file.report.update({"ExposureValue": ev})
        except KeyError:
            pass
        return file

