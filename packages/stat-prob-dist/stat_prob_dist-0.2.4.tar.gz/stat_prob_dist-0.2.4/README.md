# stat_prob_dist
A python package to calculate Statistics and Probability Distributions. Currently provides Gaussian and Binomial distribution support. Please note that this is very early stage and is certainly not ready for production use.


## Prerequisites
* Python3
* Matplotlib


## Installation
Package can be installed using pip
```python
 pip install stat_prob_dist
 ```


## Usage
```python
>>> from stat_prob_dist import Gaussian, Binomial
>>> Binomial(.4, 25)
mean 10.0, standard deviation 2.449489742783178, p 0.4, n 25
>>>
>>> Gaussian(10, 7)
mean 10, standard deviation 7
>>>
```

## Author(s)
* [Amanpreet Singh](http://amanpreetsingh459.github.io/)

## License
This project is licensed under the MIT License - see the LICENSE.txt file for details
