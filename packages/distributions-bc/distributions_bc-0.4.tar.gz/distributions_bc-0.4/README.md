# distributions_bc package


## Prerequisites

Python 3.7.4+
matplotlib package


### Files

Contains 3 files:

* generaldistribution.py
* binomialdistribution.py
* gaussiandistribution.py


### Description

* generaldistribution.py contains a Distribution class



* binomialdistribution.py creates a Binomial class that inherits from the Distribution class. This Binomial class has attributes typically associated with a Binomial Distribution (n, p, k, mean, stdev etc.) that can be either specified or determined from a file read in. The Binomial class also has methods that allow the computation of the probability distribution function and its plotting. A magic method that allows the addition of 2 Binomial Objects with the same p is also present



* gaussiandistribution.py creates a Gaussian class that inherits from the Distribution class. This Gaussian class has attributes typically associated with a Gaussian Distribution (mean, stdev) that can be either specified or determined from a file read in. The Binomial class also has methods that allow the computation of the probability distribution function and its the plotting. A magic method that allows the addition of 2 Gaussian Objects is also present


### Installation

```bash
pip install distributions_bc
```

### Usage

```bash
from distributions_bc import Gaussian

g1 = Gaussian(mu = 23, sigma = 2)
g1.mean # 23
g1.stdev # 2
g1.pdf(x = 22) # 0.2787008074875851


g1.read_data_file('numbers.txt')  # Reads file and updates attributes and parameters
```



#### Authors

Charles Gauthey


#### License

distributions_bc is offered under the MIT license
