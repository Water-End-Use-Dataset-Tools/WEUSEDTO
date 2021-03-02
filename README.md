# waterseries



##Examples

### split timeseries

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
### generate models
```bash
$ python3 src/examples/model.py 
usage: model.py [-h] [--nosplit] [--nofilter] [--nomodel] [--nocluster] [--nospline] [--splitalg {SimpleSplitter,Splitter}] FIXTURE
model.py: error: the following arguments are required: FIXTURE
```

### learn 

```bash
$ python3 src/examples/learn.py 
usage: learn.py [-h] [--nocluster] [--nospline] FIXTURE
learn.py: error: the following arguments are required: FIXTURE
```

### simulate
```bash
$ python3 src/examples/simulate.py 
usage: simulate.py [-h] [--smodel {global,monthly,weekly}] [--month {1,2,3,4,5,6,7,8,9,10,11,12}] [--weekday {0,1,2,3,4,5,6}] [--users USERS] FIXTURE
simulate.py: error: the following arguments are required: FIXTURE
```

##Documentation

* [API](https://github.io/25sal/waterseries/docs/html/)
