# Copyright 2019 Pascal Audet
#
# This file is part of GlobalTe.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# -*- coding: utf-8 -*-
import numpy as np
from math import floor
import inspect
import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

class TeModel:
    """
    Top level object to retrieve information from the global Te model
    of Audet and Burgmann, 2011.

    Attributes
    ----------
    lons : ndarray
    Longitude grid

    lats : ndarray
    Latitude grid

    te_global : ndarray
    Elastic thickness grid

    nobias : bool
    If set to `True`, the grid will not include the points that are
    biased by 'gravitational noise' (set to NaN). Otherwise all calculated
    Te points are included [default].

    """

    def __init__(self, data_path=os.path.dirname(
        inspect.stack()[0][1]) + '/../data/', nobias=False):

        self.nobias = nobias
        if self.nobias:
            file = 'te_nobias.xyz'
        else:
            file = 'te_global.xyz'

        # Read in data files
        te_data = np.loadtxt(data_path+file)

        # Reshape to a lon,lat,layer grid. The 0,0 index value
        # is at 90 south and 180 latitude.
        te_data = te_data.transpose()
        self.lons = te_data[0].reshape(180, 360)
        self.lats = te_data[1].reshape(180, 360)
        self.te_global = te_data[2].reshape(180, 360)

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

    def plot_global(self, proj='Robinson', cmap='Spectral_r', 
        levels=20, save=False):
        """
        Plots the Te model on a global map. 

        Parameters
        ----------
        proj : str
        String representing the global projection. Available projections
        are 'Robinson' [default], 'Mollweide', and 'IGH' 
        (for InterruptedGoodeHomolosine()).

        cmap : str
        Name of colormap used in map.

        levels : int
        Number of contours in colorscale.

        save : bool
        Whether or not [default] to save the figure as a `.png` file

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
        cax = ax.contourf(self.lons, self.lats, self.te_global,
            transform=ccrs.PlateCarree(),
            cmap=cmap, levels=levels)
        ax.coastlines()
        ax.gridlines()
        ax.set_global()
        cbar = fig.colorbar(cax, orientation='horizontal',
            fraction=0.035, aspect=30, pad=0.035)
        cbar.set_label('Effective elastic thickness (km)', fontsize=10)

        if save:
            plt.savefig('Global_Te'+self.nobias*'.nobias'+'.'+proj+'.png')
        else:
            plt.show()

