# UserSampling

The codes are for the experiments of the work "Privacy amplification by sampling under user differential privacy", which is submitted to SIGMOD 2024.

```
project
│   README.md
└───Code
└───Data
└───Query
└───Script
└───Result.zip
```

`./Code` includes the codes for SampleAndExplore, SimpleSample and other baselines.

`./Data` and `./Data` store the data for the graphs and TPCH datasets. Due to the size of the files, the TPCH datasets are not uploaded, and can be generated by following the [instructions](https://docs.deistercloud.com/content/Databases.30/TPCH%20Benchmark.90/Data%20generation%20tool.30.xml?embedded=true).

`./Query` stores the queries used in the experiments.

`./Script` stores the scripts used in the experiments.

`./Result.zip` stores the results of the experiments.

## Prerequisites
The framework is built on [PostgreSQL](https://www.postgresql.org/) and [Python3.7](https://www.python.org/downloads/release/python-3713/), and relies on the following dependencies.
* `getopt`
* `math`
* `matplotlib`
* `numpy`
* `os`
* `psycopg2`
* `random`
* `sys`
* `time`

## Demo - SampleAndExplore
Take edge counting on Amazon under node DP as example. We can run
```
python SampleAndExploreNode.py -G Amazon -S Edge -k 8 -T 1024 -C 13 -e 1 -d 0.00000001 -a 1851744
```
 - `-G`: the graph;
 - `-S`: the query;
 - `-k`: the maximum iteration number;
 - `-T`: the threshold \tau;
 - `-C`: the maximum clipping threshold used;
 - `-e`: the privacy budget \varepsilon;
 - `-d`: the failure probability \delta;
 - `-a`: the real answer;

## Demo - SimpleSample
For edge counting on Amazon under node DP, we can instead run
```
python SimpleSampleCountNode.py -G Amazon -S Edge -p 0.01 -T 1024 -a 1851744
```
 - `-G`: the graph;
 - `-S`: the query;
 - `-p`: the sample probability \eta;
 - `-T`: the threshold \tau;
 - `-a`: the real answer;
Note that \delta is fixed to 0.00000001 and various \varepsilon 's are used.
