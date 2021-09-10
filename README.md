# WEUSEDTO
Water End USE Dataset and TOols (WEUSEDTO) is an open water end use consumption dataset and data analytics tools, it has been released to help researcher, water utilities and companies to test models and algorithms on real water consumption data. The dataset combines with some notebook python able to analyze high-resolution water data in order to provide several tools to manage raw data, compute statistical analysis, learn fixture usage and generate synthetic simulation models.  

* [The dataset](#dataset)
* [Data analysis](#analysis)
* [The API documentation](#api)
* [Requirements](#requirements)
* [Usage examples](#examples)

<a name="dataset"></a>
## The dataset
The software repository contains raw water end-use consumption time series collected in a single apartment used as case study. 
Water end-uses are monitored using different IoT systems set up for all the fixtures in the apartment, as reported in [[1]](#bib1)  and  [[2]](#bib2). Water consumption data at household level are gathered using an ultrasonic water meter based on LoRa wireless transmission technology.

The dataset refers to 1 year of monitoring between 2019 and 2020 (March to November 2019 and July to October 2020). The residential apartment monitored, sited in Naples (Italy), is made up of 7 water fixtures and is inhabited by 1 person. Data are gathered with 1s resolution at fixture level and 10s resolution at household level. Data at fixture level are collected for the entire period of monitoring while aggregate water consumption data are available for two months (September-October 2020).

The dataset contains:
* Water end use time series disaggregate for each fixture:
   * Washbasin
   * Bidet
   * Kitchen faucet
   * Shower
   * Washinmachine
   * Dishwasher (2 time series: cycle 30min and cycle 50eco)
   * Toilet
* Water end use time series aggregate for the whole apartment:
   * Whole house consumption
   
Since data collection is still on going, the DATASET is also available at this public repository: https://github.com/AnnaDiMauro/WEUSEDTO-Data where data stored will be periodically improved as more data become available.

<a name="analysis"></a>
## Data Analysis
Examples of analysis of water flow timeseries are shown in two notebook:
* [Shower Analysis](https://github.com/Water-End-Use-Dataset-Tools/WEUSEDTO/blob/main/src/notebooks/shower.ipynb)
* [Washbasin Analysis](https://github.com/Water-End-Use-Dataset-Tools/WEUSEDTO/blob/main/src/notebooks/washbasin.ipynb)

<a name="API"></a>
## API Documentation
The API allow for processing raw flow data and are organized according to four packages:
* *timeseries*: splits data into many short series, corresponding to different water usages. Provides methods to identify and filter overlays.
* *model*: support the statistical charactarization of water usages.
* *learning*: cluster and predict water consumption profile of usages.
* *simulation*: according to statistical properties and machine learning techniques simulates usages at larger scale.

API documentation can be found [here](https://water-end-use-dataset-tools.github.io/WEUSEDTO/docs/html).

<a name="requirements"></a>
## Requirements
Python 3.8 has been used as testing evironment.
To install requirements you can run:
```bash
$pip install -r requirements.txt
```
Alternatively you can directly run the software at codeocean! [![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/9225099).

<a name="examples"></a>
## Usage examples

Four python modules are provided to show how APIs can be used.
* split
* model
* learn
* simulate

### Split timeseries
This module uses the APIs to split a timeseries detecting several usages. It allows to filter overlays according to criteria embedded into the code. Two splitting algoritms can be chosen: "SimpleSplitter" and "Splitter". 

```bash
$python3 src/examples/split.py -h
usage: split.py [-h] [--nosplit] [--nofilter] [--alg SPLITALG] FIXTURE

complete example

positional arguments:
  FIXTURE         the basename of csv timeseries to be analyzed

optional arguments:
  -h, --help      show this help message and exit
  --nosplit       skip the split stage
  --nofilter      skip the filter stage
  --alg SPLITALG

```
### Generate models
This module compute statistics from splitted timeseries and generate three kinds (global, monthly, weekly) of statistical representation of user behaviour in terms of fixter usage. It also compute clusters of usage according to duration, consumed volume and maximum flow speed. It also compute, for each cluster an average water consumption profile using an spline approximation.
It starts from the splitting phase that can be skipped.

```bash
$ python3 src/examples/model.py 
usage: model.py [-h] [--nosplit] [--nofilter] [--nomodel] [--nocluster] [--nospline] [--splitalg {SimpleSplitter,Splitter}] FIXTURE
model.py: error: the following arguments are required: FIXTURE
```

### Learn
This module use machine learning techniques to learn the cluster of the water usage according to the datetime it starts.

```bash
$ python3 src/examples/learn.py 
usage: learn.py [-h] [--nocluster] [--nospline] FIXTURE
learn.py: error: the following arguments are required: FIXTURE
```

### Simulate
This module use simulate the water consumption of multiple users generating timeseries exploiting the statistical characterization of usages and the learned models

```bash
$ python3 src/examples/simulate.py 
usage: simulate.py [-h] [--smodel {global,monthly,weekly}] [--month {1,2,3,4,5,6,7,8,9,10,11,12}] [--weekday {0,1,2,3,4,5,6}] [--users USERS] FIXTURE
simulate.py: error: the following arguments are required: FIXTURE
```

### References
<a name="bib1">[1]</a>  [*Di Mauro, A., Di Nardo, A., Santonastaso, G. F., & Venticinque, S. (2019). An IoT system for monitoring and data collection of residential water end-use consumption. In Proc. - Int. Conf. Comput. Commun. Networks, ICCCN. Vol. 2019-July*](https://www.researchgate.net/publication/334957395_An_IoT_System_for_Monitoring_and_Data_Collection_of_Residential_Water_End-Use_Consumption) 

<a name="bib2">[2]</a> [*Di Mauro, A., Di Nardo, A., Santonastaso, G. F., & Venticinque, S. (2020). Development of an IoT System for the Generation of a Database of Residential Water End-Use Consumption Time Series. Environ. Sci. Proc. 2, 20.*](https://www.researchgate.net/publication/343637309_Development_of_an_IoT_System_for_the_Generation_of_a_Database_of_Residential_Water_End-Use_Consumption_Time_Series)

### Licences
This work is dual-licensed:

*SOFTWARE*: Released under the [GNU General Public License v3.0.](https://github.com/Water-End-Use-Dataset-Tools/WEUSEDTO/blob/main/LICENSE.txt) See the GNU General Public License for more details: http://www.gnu.org/licenses/licenses.en.html.

*DATASET*: Released under the [Creative Commons Attribution 4.0 International.](https://github.com/Water-End-Use-Dataset-Tools/WEUSEDTO/blob/main/data/LICENSE.txt) See theCreative Commons Attribution 4.0 International License for more details:https://creativecommons.org/licenses/by/4.0/legalcode
