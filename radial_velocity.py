import os
import glob
from astropy.table import Table, vstack
from astropy.io import fits


# Read in the data
def read_files(directory):
    filenames = glob.glob(os.path.join(directory, "*.fits"))
    print(filenames)
    finished_table = Table()
    for data_file in filenames:
        table = Table.read(data_file, format="fits")
        finished_table = vstack(finished_table, table)
    print(finished_table)

#read_files(os.path.join("data"))

hdulist = fits.open("/home/jacob/Development/Aarhus-Radial-Velocity/data/s1_2015-04-19T21-46-20_ext.fits")
print(hdulist.info())
data = hdulist[0].data
print(data)
