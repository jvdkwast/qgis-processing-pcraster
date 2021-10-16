# Processing PCRaster Provider

Processing provider for the PCRaster analysis tools for [QGIS](https://www.qgis.org/en/site/). The plugin allows execution of PCRaster operations directly from QGIS.

## Installation

The plugin is available QGIS Python Plugins Repository [here](https://plugins.qgis.org/plugins/processing_pcraster/). It can also be installed directly from QGIS via the **Plugins** tool.

Building from source for offline install can be done by downloading the [source code](https://github.com/jvdkwast/qgis-processing-pcraster) and running command:
```
make zip
```
in the main directory. The produced zip file can then be installed in QGIS from **Plugins** tool in the **Install from zip** window.

## Contributors

[List of project contributors on GitHub.](https://github.com/jvdkwast/qgis-processing-pcraster/graphs/contributors)

## PCRaster

[PCRaster](https://pcraster.geo.uu.nl/) is a powerful package of software for map algebra and environmental dynamic modelling. The main applications of PCRaster are found in environmental modelling: geography, hydrology, ecology to name a few. An extensive set of raster [operations](https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_manual/sphinx/index.html#operations-python-and-pcrcalc) is available: several point operations (analytical and arithmetical functions, Boolean operators, operators for relations, comparison, rounding, field generation etc.), neighbourhood operations for calculations in moving windows (highpass filtering, edge filtering, moving averages, etc.), area operations for calculations within specified areas (for instance soil groups), operations for the calculation of cost paths. In the PCRaster package a rich suite of geomorphological and hydrological functions is available. These include functions for visibility analysis, catchment analysis and routing of transport (drainage) of material in a catchment using interactively generated local drain direction maps and transport (routing) operations. These operations are made available in the QGIS Processing Toolbox through this plugin.

## Settings for the plugin

Before you can use the plugin you need to install PCRaster.

### Windows (OSGeo4W)

On Windows you can install PCRaster with the OSGeo4W installer. Alternatively you can install PCRaster and QGIS in conda (see next section).

1. Run the OSGeo4W setup
2. Choose Advanced Install, click Next
3. Choose Install from Internet, click Next
4. Select the root install directory or keep the defaults, click Next
5. Select local package directory or keep the defaults, click Next
6. Select your internet connection, click Next
7. Choose one of the download sites, click Next
8. In the Select Packages window search for pcraster
9. Click the arrows icon to change from skip to a PCRaster version to install and click Next to install.

![image](https://user-images.githubusercontent.com/1172662/132013736-b88639df-eb71-4fc1-860e-681063f428f1.png)

This video shows the steps: [Install PCRaster, SAGA and GRASS tools for QGIS with the OSGeo4W installer](https://youtu.be/pja_EX0tVZA)

### Linux, MacOS and Windows (conda)

PCRaster is available on [conda-forge](https://conda-forge.org/feedstock-outputs/index.html) and can be installed using conda. Supported platforms are Linux, MacOS and Windows. QGIS and PCRaster need to be installed in the same conda environment.

First thing you need to do is to install the Conda packaging system. Two distributions install Conda: Anaconda and Miniconda.

1. Download [Anaconda](https://www.anaconda.com/distribution/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installers for your system and follow the instructions to install it.
2. Create a new conda environment and install QGIS and PCRaster by typing the following command in the terminal (e.g. Anaconda prompt on Windows): `conda create --name <name_of_the_environment> -c conda-forge qgis pcraster`
3. Enter the environment by typing `conda activate <name_of_the_environment>`
4. Type `qgis` to run QGIS
5. Install the plugin

This video shows the steps: [Installing the PCRaster Tools plugin for QGIS using conda (MacOS, Linux, Windows)](https://youtu.be/RaFrXzw7IvI)

[More info about installing PCRaster](https://pcraster.geo.uu.nl/pcraster/4.3.1/documentation/pcraster_project/install.html)

[More info about QGIS in conda](https://gisunchained.wordpress.com/2019/05/29/using-qgis-from-conda/)

## Other resources
[YouTube playlist on PCRaster Tools in QGIS](https://youtube.com/playlist?list=PLeuKJkIxCDj2xbV45C45wz3N89FvmTuSu)


