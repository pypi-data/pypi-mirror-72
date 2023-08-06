Histogram
=========

.. automodule histogram
..	:members:



Base histogram
--------------

The base histogram class from which histograms of a specific dimension inherit.

.. autoclass:: heppy.basehistogram
    :members:
    :special-members: __add__,__mul__,__truediv__,__sub__



One-dimensional histogram
-------------------------

A histogram class with bins along one axis.

.. autoclass:: heppy.histogram1d
	:members:
	:inherited-members:
	:special-members: __add__,__mul__,__truediv__,__sub__

Convenience alias for one-dimensional histograms, since these are the most commonly encountered type in high-energy physics.

.. autoclass:: heppy.histogram



Two-dimensional histogram
-------------------------

A histogram class with bins along two axes.

.. autoclass:: heppy.histogram2d
	:members:
	:inherited-members:
	:special-members: __add__,__mul__,__truediv__,__sub__



Free functions
--------------

Free functions related to histograms.

.. autofunction:: heppy.histdiv

.. autofunction:: heppy.from_file
