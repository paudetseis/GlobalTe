
import numpy as np
from math import floor
import inspect
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

class TeModel:
    """
    Top level model object to retreive information from the global Te model
    of Audet and Burgmann, 2011.

    Attributes
    ----------
    lons : ndarray
    Longitude grid

    lats : ndarray
    Latitude grid

    te_global : ndarray
    Elastic thickness grid

    """

    def __init__(self, data_path=os.path.dirname(inspect.stack()[0][1]) + '/../data/'):

        # Read in data files
        te_data = np.loadtxt(data_path+'te_global.xyz')

        # Reshape to a lon,lat,layer grid. The 0,0 index value
        # is at 90 south and 180 latitude.
        te_data = te_data.transpose()
        self.lons = te_data[0].reshape(90, 180)
        self.lats = te_data[1].reshape(90, 180)
        self.te_global = te_data[2].reshape(90, 180)

    def _get_index(self, lat, lon):
        """
        Returns in index values used to query the model for a given lat lon.

        Paramaters
        ----------
        lat : float
        Latitude of point

        lat : float
        Longitude of point

        Returns
        -------
        ilat : int
        Index for given latitude

        ilon : int
        Index for given longitude
        """

        # Make sure the longitude is between -180 and 180
        if lon > 180:
            lon -= 360
        if lon < -180:
            lon += 360

        # Find the index in the data for given lat and lon
        ilat = floor(90. - lat)
        ilon = floor(180 + lon)

        return int(ilat), int(ilon)

    def get_te_point(self, lat, lon):
        """
        Returns a Te value for a given latitude and longitude. 

        Parameters
        ----------
        lat : float
        Latitude of point

        lat : float
        Longitude of point

        Returns
        -------
        te : float
        Te value at point (km).
        """

        # Get index for arrays of data at this location
        ilat, ilon = self._get_index(lat, lon)

        # Calculate the thickness of the layers, add zero to the end
        # for the mantle since it's not defined
        self.te = self.te_global[ilat, ilon]

        return self.te

    def plot_global(self, proj='Robinson'):
        """
        Plots the Te model on a global map. 

        Parameters
        ----------
        proj : str
        String representing the global projection
        """

        # Specify projection
        if proj == 'Robinson':
            cc = ccrs.Robinson()
        elif proj == 'Mollweide':
            cc = ccrs.Mollweide()
        elif proj == 'IGH':
            cc = ccrs.InterruptedGoodeHomolosine()

        # Initialize figure
        fig = plt.figure(figsize=(10, 5))

        # Add one subplot
        ax = fig.add_subplot(1, 1, 1, projection=cc)

        # self.mask = np.isnan(te)
        # te = np.ma.array(te, mask=self.mask)
        ax.contourf(self.lons, self.lats, self.te_global,
            transform=ccrs.PlateCarree(),
            cmap='Spectral_r')
        ax.coastlines()
        ax.gridlines()
        ax.set_global()

        plt.show()

