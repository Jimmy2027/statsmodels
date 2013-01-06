# -*- coding: utf-8 -*-
"""Examples of non-linear functions for non-parametric regression

Created on Sat Jan 05 20:21:22 2013

Author: Josef Perktold
"""

import numpy as np




def fg1(x):
    '''Fan and Gijbels example function 1

    '''
    return x + 2 * np.exp(-16 * x**2)

def fg1eu(x):
    '''Eubank similar to Fan and Gijbels example function 1

    '''
    return x + 0.5 * np.exp(-50 * (x - 0.5)**2)

def fg2(x):
    '''Fan and Gijbels example function 2

    '''
    return np.sin(2 * x) + 2 * np.exp(-16 * x**2)

doc = {'description':
'''Base Class for Univariate non-linear example

    Does not work on it's own.
    needs additional at least self.func
''',
'ref': ''}

class _UnivariateFanGijbels(object):
    __doc__ = '''%(description)s

    Parameters
    ----------
    nobs : int
        number of observations to simulate
    x : None or 1d array
        If x is given then it is used for the exogenous variable instead of
        creating a random sample
    distr_x : None or distribution instance
        Only used if x is None. The rvs method is used to create a random
        sample of the exogenous (explanatory) variable.
    distr_noise : None or distribution instance
        The rvs method is used to create a random sample of the errors.

    Attributes
    ----------
    x : ndarray, 1-D
        exogenous or explanatory variable. x is sorted.
    y : ndarray, 1-D
        endogenous or response variable
    y_true : ndarray, 1-D
        expected values of endogenous or response variable, i.e. values of y
        without noise
    func : callable
        underlying function (defined by subclass)

    %(ref)s
    ''' #% doc

    def __init__(self, nobs=200, x=None, distr_x=None, distr_noise=None):

        if x is None:
            if distr_x is None:
                x = np.random.normal(loc=0, scale=self.s_x, size=nobs)
            else:
                x = distr_x.rvs(size=nobs)
        self.x = x
        self.x.sort()
        if distr_noise is None:
            noise = np.random.normal(loc=0, scale=self.s_noise, size=nobs)
        else:
            noise = distr_noise.rvs(size=nobs)

        #self.func = fg1
        self.y_true = y_true = self.func(x)
        self.y = y_true + noise


    def plot(self, scatter=True, ax=None):
        '''plot the mean function and optionally the scatter of the sample

        Parameters
        ----------
        scatter: bool
            add scatterpoints of sample to plot
        ax : None or matplotlib axis instance
            If None, then a matplotlib.pyplot figure is created, otherwise
            the given axis, ax, is used.

        Returns
        -------
        fig : matplotlib figure
            This is either the created figure instance or the one associated
            with ax if ax is given.

        '''
        if ax is None:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)

        if scatter:
            ax.plot(self.x, self.y, 'o', alpha=0.5)

        xx = np.linspace(self.x.min(), self.x.max(), 100)
        ax.plot(xx, self.func(xx), lw=2, color='b', label='dgp mean')
        return ax.figure

doc = {'description':
'''Fan and Gijbels example function 1

linear trend plus a hump
''',
'ref':
'''
References
----------
Fan, Jianqing, and Irene Gijbels. 1992. "Variable Bandwidth and Local
Linear Regression Smoothers."
The Annals of Statistics 20 (4) (December): 2008-2036. doi:10.2307/2242378.

'''}

class UnivariateFanGijbels1(_UnivariateFanGijbels):
    __doc__ = _UnivariateFanGijbels.__doc__ % doc


    def __init__(self, nobs=200, x=None, distr_x=None, distr_noise=None):
        self.s_x = 1.
        self.s_noise = 0.7
        self.func = fg1
        super(self.__class__, self).__init__(nobs=nobs, x=x,
                                             distr_x=distr_x,
                                             distr_noise=distr_noise)

doc['description'] =\
'''Fan and Gijbels example function 2

sin plus a hump
'''

class UnivariateFanGijbels2(_UnivariateFanGijbels):
    __doc__ = _UnivariateFanGijbels.__doc__ % doc

    def __init__(self, nobs=200, x=None, distr_x=None, distr_noise=None):
        self.s_x = 1.
        self.s_noise = 0.5
        self.func = fg2
        super(self.__class__, self).__init__(nobs=nobs, x=x,
                                             distr_x=distr_x,
                                             distr_noise=distr_noise)

class UnivariateFanGijbels1EU(_UnivariateFanGijbels):
    '''

    Eubank p.179f
    '''

    def __init__(self, nobs=50, x=None, distr_x=None, distr_noise=None):
        from scipy import stats
        distr_x = stats.uniform
        self.s_noise = 0.15
        self.func = fg1eu
        super(self.__class__, self).__init__(nobs=nobs, x=x,
                                                   distr_x=distr_x,
                                                   distr_noise=distr_noise)
