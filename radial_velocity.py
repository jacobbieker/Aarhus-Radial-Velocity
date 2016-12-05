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

    def convert_to_km(spectrum):
        ws = np.arange(0, 2048, 1)
        for index, element in enumerate(ws):
            ws[index] = 4383.0 + 0.022*element
        converted = np.array([])
        r = 1.0/2.997924e5  # <- For 1.0km/s resolution
        w1 = np.arange(0, 2048, 1)
        for index, element in enumerate(w1):
            w1[index] = 4385.0 * (1.0 + r)**element
        #print(len(w1))
        #print(len(ws))
        #print(len(wavelength))
        for index, spectra in enumerate(spectrum):
            np.append(converted, np.interp(w1, ws, spectra))
        return converted

    def plot_wavelength(spectrum, wavelength):
        """
        Plot the spectrum as function of wavelength
        :param spectrum:
        :param wavelength:
        :return:
        """
        for index, element in enumerate(wavelength):
            #print(len(wavelength))
            #print(len(element))
            plt.plot(element, spectrum)
        plt.show()

    def correlate_wavelength(spectrum1, spectrum2):
        lag = np.arange(-1023, 1024, 1)
        value = np.correlate(spectrum1, spectrum2, "same")
        velocity = lag * 1.0
        plt.plot(velocity, value)
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

        #plot_wavelength(extracted_spectrum, before_spectrum)
        #plot_wavelength(extracted_spectrum, after_spectrum)
        #print(extracted_spectrum[0])
        converted_extracted = convert_to_km(extracted_spectrum)
        plot_wavelength(converted_extracted, before_spectrum)
        converted_before = convert_to_km(before_spectrum)
        converted_after = convert_to_km(after_spectrum)


read_files(os.path.join("data"))


