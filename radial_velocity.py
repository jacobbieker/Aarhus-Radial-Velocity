import os
import glob
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

def cross_correlation(extracted, before, after):
    """

    :param extracted: A list of arrays of extracted spectrum converted to km/s
    :param before: A list of arrays of spectrum taken right before the extracted ones in km/s
    :param after: A list of arrays of spectrum taken right before the extracted ones in km/s
    :return: Arrays with cross-correlated data
    """


# Read in the data
def read_files(directory):

    def convert_to_km(wavelength):
        wavelength = 1.0 - wavelength
        converted = np.array([])
        r = 0.5/2.997924e5  # <- For .5km/s resolution

        return converted

    def plot_wavelength(spectrum, wavelength):
        print(spectrum)
        for index, element in enumerate(spectrum):
            plt.plot(wavelength[index], element)
            plt.show()


    filenames = glob.glob(os.path.join(directory, "*.fits"))
    print(filenames)
    for data_file in filenames:
        table = fits.open(data_file)
        data = table[0].data
        header = table[0].header
        print(data)
        print(repr(header))
        print(data.shape)
        # Going through each of the 5 data sets
        '''
         1: the extracted spectrum (2048x51)
         2: the summed spectrum
         3: the blaze function (2048x51)
         4: the wavelength (2048x51), closest in time before the science exposure
         5: the wavelength (2048x51), closest in time after the science exposure.

         r = 0.5/2.997924d5  <- For .5km/s resolution
         w1 = 5187.0 * (1.d0+r)^dindgen(1024)

         Where r is the inverse spectroscopic resolution power R

        '''
        # extracted spectrum
        extracted_spectrum = data[0]
        before_spectrum = data[3]
        after_spectrum = data[4]
        plot_wavelength(extracted_spectrum, before_spectrum)
        plot_wavelength(extracted_spectrum, after_spectrum)
        converted_extracted = convert_to_km(extracted_spectrum)
        converted_before = convert_to_km(before_spectrum)
        converted_after = convert_to_km(after_spectrum)


read_files(os.path.join("data"))


