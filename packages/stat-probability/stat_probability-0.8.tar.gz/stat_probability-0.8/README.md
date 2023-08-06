stat-probability package:

The package calculates the gaussion distribution and Binomial distribution for a given
set of inputs. Calculate mean and standard deviation using Gaussian distribution and Binomial distribution.

Installation:

pip3 install stat_probablitiy

Usage:

>>> from stat_probability import Gaussian
>>> from stat_probability import Binomial
>>> Gaussian1 = Gaussian(23, 5)
>>> Gaussian2 = Gaussian(23, 3)
>>> total_gaussian = Gaussian1 + Gaussian2
>>> print(total_gaussian)
mean 46, standard deviation 5.830951894845301
>>> Binomial(0.8, 9)
mean 7.2, standard deviation 1.2, p 0.8, n 9