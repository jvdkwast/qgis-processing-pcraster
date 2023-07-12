# PCRaster Tools Plugin

Processing provider for the PCRaster analysis tools for [QGIS](https://www.qgis.org/en/site/). The plugin allows execution of PCRaster operations directly from QGIS.

## Installation

The plugin is available in the QGIS Python Plugins Repository [here](https://plugins.qgis.org/plugins/pcraster_tools/). It can also be installed directly from QGIS via the **Plugins** tool. **Note that you have to install PCRaster too (instructions below)**.

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

Before you can use the plugin you need to install PCRaster. This can be done on Windows (OSGeo4W installer or conda), Linux (build from source or conda) or MacOS (conda).

### Windows (OSGeo4W)

PCRaster is available in the OSGeo4W installer. Alternatively you can install PCRaster and QGIS in conda (see conda section below).

1. Run the OSGeo4W setup
2. Choose *Advanced Install*, click *Next*
3. Choose *Install from Internet*, click *Next*
4. Select the root install directory or keep the defaults, click *Next*
5. Select local package directory or keep the defaults, click *Next*
6. Select your internet connection, click *Next*
7. Choose one of the download sites, click *Next*
8. In the *Select Packages window* search for pcraster
9. Click the arrows icon to change from skip to a PCRaster version to install. 
10. Click *Next* to complete the installation.

Watch this video:

[![Install PCRaster packages with the OSGeo4W Installer](https://user-images.githubusercontent.com/1172662/148247643-40c2d8ed-9823-43ac-ad9a-9f3d9a512fad.jpg)](https://youtu.be/pja_EX0tVZA "Install PCRaster packages with the OSGeo4W Installer")

### Windows (Standalone QGIS install)

The QGIS standalone install includes a bundled version of the OSGeo4W installer which will be listed in your start menu as *Setup*.

1. Run *Setup*.  You will probably need to right-click on it, choose *Run as administrator*, and confirm that you want to allow it to modify your computer.
2. Choose *Advanced Install*, click *Next*
3. Choose *Install from Internet*, click *Next*
4. Leave the root directory unchanged and click *Next*
5. Select local package directory or keep the defaults, click *Next*
6. Select your internet connection, click *Next*
7. Choose one of the download sites, click *Next*
8. Select the radio button to *Keep* existing packages at their currently installed version.
9. In the *Search* field search for *pcraster*.
10. Click the *+* to expand *Libs*.
11. Click the arrows icon to change from skip to a PCRaster version to install. 
12. Click *Next* to complete the installation.

Watch this video:
[Install QGIS with the Standalone Installer and Add Missing Packages](https://youtu.be/9rFL2VgbZ7Q)

### Linux, MacOS and Windows (conda)

PCRaster is available on [conda-forge](https://conda-forge.org/feedstock-outputs/index.html) and can be installed using conda. Supported platforms are Linux, MacOS and Windows. QGIS and PCRaster need to be installed in the same conda environment.

First thing you need to do is to install the Conda packaging system. Two distributions install Conda: Anaconda and Miniconda.

1. Download [Anaconda](https://www.anaconda.com/distribution/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installers for your system and follow the instructions to install it.
2. Create a new conda environment and install QGIS and PCRaster by typing the following command in the terminal (e.g. Anaconda prompt on Windows): <br>`conda create --name <name_of_the_environment> -c conda-forge qgis pcraster`
4. Enter the environment by typing `conda activate <name_of_the_environment>`
5. Type `qgis` to run QGIS
6. Install the plugin

Watch this video:

[![Install PCRaster and QGIS in conda](https://user-images.githubusercontent.com/1172662/148248750-d0f4adf0-67fb-4bcb-a524-b8ad518c0c30.png)](https://youtu.be/RaFrXzw7IvI "Install PCRaster and QGIS in conda")

Alternatively, you can use mamba, which is faster. Watch this video:

[![Install Mamba and create a Python environment with QGIS and PCRaster](https://github.com/jvdkwast/qgis-processing-pcraster/assets/1172662/29a7f31e-50dc-4b3f-9534-09fce8ee4ec7)](https://youtu.be/VgBYgk7VQWg "Install Mamba and create a Python environment with QGIS and PCRaster")

### Build PCRaster from source on Linux

In [this Gist](https://gist.github.com/timlinux/5824f0e3d75f2fc43267e5c058602cde#file-buildingpcrasteronfedora-md) by Tim Sutton you can read how to build PCRaster on Fedora from source.

For building PCRaster on Ubuntu you can type the following commands in the terminal window:

```
sudo apt install libboost-all-dev libqt5charts5-dev libxerces-c-dev libncurses-dev cmake-curses-gui libqt5opengl5-dev pybind11-dev
git clone --recursive https://github.com/pcraster/pcraster.git
cd pcraster && mkdir build && cd build
cmake -G"Unix Makefiles" -D CMAKE_BUILD_TYPE=Release -DPCRASTER_BUILD_TEST=OFF ..
make -j4
sudo make install
echo "export PYTHONPATH=$PYTHONPATH:/usr/local/python" >> ~/.bash_profile
```

Then reboot: 
`sudo reboot`

After rebooting you can test the installation with the following commands:
`python3`
```Python
import pcraster as pcr
pcr.__version__
```


## Other resources

[FOSS4G 2022 Workshop on Hydrological analysis with PCRaster in QGIS and Python](https://courses.gisopencourseware.org/course/view.php?id=53)

[YouTube playlist on PCRaster Tools in QGIS](https://youtube.com/playlist?list=PLeuKJkIxCDj2xbV45C45wz3N89FvmTuSu)

[More info about installing PCRaster](https://pcraster.geo.uu.nl/pcraster/latest/documentation/pcraster_project/install.html)

[More info about QGIS in conda](https://gisunchained.wordpress.com/2019/05/29/using-qgis-from-conda/)

[PCRaster documentation](https://pcraster.geo.uu.nl/pcraster/latest/documentation)

## Found bugs or need help?

The PCRaster community has a mailing list. The pcraster-info mailing list is a discussion platform for users of PCRaster and related software. The PCRaster Research&Development team also uses the list to announce new software releases. We recommend that every PCRaster user becomes a member of the list. [Subscribe here](https://pcraster.geo.uu.nl/support/questions/).

Issues related to the PCRaster package can be reported on the PCRaster GitHub repository [following these instructions](https://pcraster.geo.uu.nl/support/report-a-bug/).

Issues related to the PCRaster Tools plugin for QGIS can be reported in the [PCRaster Tools Github repository](https://github.com/jvdkwast/qgis-processing-pcraster/issues).





