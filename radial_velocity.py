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

    def lambda_n(velocity, start, finish):
        c = 2.997924e5
        n_max = np.log(finish/start)/np.log(1 + velocity/c)
        print(n_max)
        n_max = int(n_max)
        new_lambda = []
        for n in range(0, n_max):
            new_lambda.append(start * (1 + (velocity/c))**n)

    def interpolate_to_lambda(old_lambda, new_lambda, spectrum):
        converted = []
        for index, spectra in enumerate(spectrum):
            converted.append(np.interp(new_lambda[index], old_lambda[index], spectra))
        return converted

    def plot_wavelength(spectrum, wavelength):
        """
        Plot the spectrum as function of wavelength
        :param spectrum:
        :param wavelength:
        :return:
        """
        #print(len(spectrum))
        #print(len(wavelength))
        for index, element in enumerate(spectrum):
            plt.plot(wavelength[index], element)
        plt.xlabel("Angstroms")
        plt.ylabel("Count")
        plt.show()

    def correlate_wavelengths(spectrum1, spectrum2):
        lag = np.arange(-1024, 1024, 1)
        print(len(spectrum1))
        print(len(lag))
        value = np.correlate(spectrum1, spectrum2, "same")
        velocity = lag * 1.0
        print(len(value))
        plt.plot(velocity, value)

    filenames = glob.glob(os.path.join(directory, "*.fits"))
    print(filenames)
    for data_file in filenames:
        table = fits.open(data_file)
        data = table[0].data
        header = table[0].header
        #print(data)
        #print(repr(header))
        #print(data.shape)
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
        before_wavelength = data[3]
        after_wavelength = data[4]

        #plot_wavelength(extracted_spectrum, before_wavelength)
        plot_wavelength(extracted_spectrum, after_wavelength)
        converted_extracted = convert_to_km(extracted_spectrum)
        plot_wavelength(converted_extracted, after_wavelength)
        #print(len(converted_extracted))
        for index in range(0, len(converted_extracted) - 1):
            correlate_wavelengths(converted_extracted[index], converted_extracted[index + 1])
        plt.show()
        converted_before = convert_to_km(before_wavelength)
        converted_after = convert_to_km(after_wavelength)


read_files(os.path.join("data"))


