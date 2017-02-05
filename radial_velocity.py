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
        '''
        del(v) and velocity is the change that I am going for i.e. 1 km/s
        Steps: Change the different wavelengths to the same lambda through lambda0 *(1+del(v)/c)^n - lambdaN = 5438 or something
        n is the step for it all, from o to nmax, where nmax gives 5438 Angstroms
        Then interpolate the original spectrum on the new n value, so that the new flux corresponds to the same wavelength
        Resample, and then cross-correlate to the template, after converting the solar template to teh same lambda
        Use Walalce Hinkle for the solar spectrum
        '''
        c = 2.997924e5
        n_max = np.log(finish/start)/np.log(1 + velocity/c)
        print(n_max)
        n_max = int(n_max)
        new_lambda = []
        for n in range(0, n_max):
            new_lambda.append(start * (1 + (velocity/c))**n)
        return new_lambda

    def interpolate_to_lambda(old_lambda, new_lambda, spectrum):
        '''
        :param old_lambda: Set of x-coordinates of the original spectrum, usually based off wavelength[index]?
        :param new_lambda: Set of new x-coordinates to interpolate data on
        :param spectrum: Set of y-coordinate data, the spectrum flux
        :return: Converted set of spectrum moved to the new lambda
        '''
        converted = []
        new_spectrum = []
        for index, spectra in enumerate(spectrum):
            converted.append(np.interp(new_lambda[index], old_lambda[index], spectra))
        for index, new_spectra in enumerate(converted):
            new_spectrum.append((new_lambda[index], new_spectra))
        return new_spectrum

    def convert_and_interpolate(spectrum, wavelength, vel_resolution, start_ang, end_ang):
        '''
        Completely converts a given source spectrum into a specified start and end lambda for the given resolution from source spectra
        :param spectrum: Source spectra
        :param vel_resolution: Velocity resolution in km/s
        :param start_ang: Start Angstrom value (i.e. 5400) used for new lambda for the start
        :param end_ang: End Angstrom value (i.e. 5438) used for new lambda for the finish
        :return: Converted spectra based on the start and end Angstrom values with the specified resolution in a list of tuples
        '''
        converted_spectrum = []
        calculated_lambda = lambda_n(vel_resolution, start=start_ang, finish=end_ang)
        for index, spectra in enumerate(spectrum):
            converted_spectrum.append(interpolate_to_lambda(wavelength[index], calculated_lambda, spectrum))
        return converted_spectrum

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

        converted_extracted = interpolate_to_lambda(5400, 5438, extracted_spectrum)

        #plot_wavelength(extracted_spectrum, before_wavelength)
        plot_wavelength(extracted_spectrum, after_wavelength)
        plot_wavelength(converted_extracted, after_wavelength)
        #print(len(converted_extracted))
        for index in range(0, len(converted_extracted) - 1):
            correlate_wavelengths(converted_extracted[index], converted_extracted[index + 1])
        plt.show()

read_files(os.path.join("data"))


