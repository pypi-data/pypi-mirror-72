"""
Module provides functionality for creating alloy
feature representations for alloy recipes by
considering them as descriptions of atom populations.

>>> prop_value('Al', 'Speed of Sound')
5100.0
>>> prop_value('Cu', 'Speed of Sound')
3570.0

"""

import pandas as pd
import math

import alloyml.datasets as datasets

from os import path

_dirname = path.dirname(__file__)
_tab_filename = path.join(_dirname, 'data', 'atomic_features.csv')
_meta_tab_filename = path.join(_dirname, 'data', 'atomic_features_metadata.csv')
table = pd.read_csv(_tab_filename, index_col=0)
properties = pd.read_csv(_meta_tab_filename, index_col=0) #table.columns
elements = table.index
verbose = True


def property_id(property):
    """ Finds canonical id of property.

    :param property: id, full name, or short name of property
    :return: id of property or None if no such property

    >>> property_id('Speed of Sound')
    'sos'

    >>> property_id('Speed Snd.')
    'sos'

    >>> property_id('Sp')
    'sos'

    >>> property_id('sos')
    'sos'
    """
    if property in properties.index:
        return property

    byfull = properties[properties.full == property].index
    if not byfull.empty:
        return byfull[0]

    byshort = properties[properties.short == property].index
    if not byshort.empty:
        return byshort[0]

    bysymb2 = properties[properties.symbol_2char == property].index
    if not bysymb2.empty:
        return bysymb2[0]

    return None


def prop_value(el, prop, warn=verbose):
    """ Provides access to atomic properties.

    :param el: the element for which property value is required, using usual chemical symbol, e.g., 'H', 'Cu', ...
    :param prop: the name of the property, e.g., 'Atomic radius'
    :param warn: whether to print warning if property not available (result will be nan)
    :return: the property value (or nan if unavailable)

    For example:
    >>> prop_value('H', 'Calculated Atomic Radius')
    53.0
    >>> prop_value('Th', 'Calculated Atomic Radius')
    0.18
    >>> prop_value('Th', 'Mean Lattice Constant')
    508.42
    """
    id = property_id(prop)
    if not id:
        if warn:
            print("WARNING: no such property: '{}'".format(prop))
        return None

    res = table.loc[el, id]
    if warn and math.isnan(res):
        print("WARNING: '{}' not available for element '{}'".format(prop, el))
    return res


def base_metal(alloy):
    """
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[50]
    >>> base_metal(alloy)
    'Al'
    """
    return max(elements_in(alloy), key=alloy.get)


def elements_in(alloy):
    """
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[24]
    >>> list(elements_in(alloy))
    ['Al', 'Cu', 'Mg', 'Mn', 'Pb']
    """
    return (key for key in alloy.keys() if key in elements and alloy[key] > 0.0)


def element_dist(alloy):
    """
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[24]
    >>> list(elements_in(alloy))
    ['Al', 'Cu', 'Mg', 'Mn', 'Pb']
    >>> element_dist(alloy)
    {'Al': 0.9344999999999999, 'Cu': 0.03899999999999999, 'Mg': 0.009, 'Mn': 0.005999999999999999, 'Pb': 0.011499999999999998}
    """
    els = list(elements_in(alloy))
    s = sum(alloy[el] for el in els)
    return {el: alloy[el]/s for el in els}


def property_dist(alloy, prop):
    dist = element_dist(alloy)
    return [(prop_value(el, prop), p) for el, p in dist.items()]


class Mean:
    """

    For example:
    >>> mean_sos = Mean('Speed of Sound')
    >>> mean_sos
    mean(Sp)
    >>> alloys = datasets.Al_maxUTS_MIF() #pd.read_csv(path.join(dirname, '..', 'data', 'AAl_maxUTS_MIF.csv'), index_col=0)
    >>> alloy = alloys.iloc[24]
    >>> from math import isclose
    >>> isclose(mean_sos(alloy), 4991.988)
    True
    """

    def __init__(self, prop):
        self.prop = property_id(prop)
        self.string = 'mean({})'.format(properties.symbol_2char[self.prop])

    def __call__(self, alloy):
        """
        :param alloy: data series with elements representing mixture coefficients of elements
            with names matching the chemical element names: 'H', 'He', 'Li', 'Be', etc.
        :return: mean value of property in atomic population described by alloy
        """
        dist = element_dist(alloy)
        s = sum(p * prop_value(el, self.prop) for el, p in dist.items())
        return s

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class StdDev:
    """

    For example:
    >>> std_sos = StdDev('Speed of Sound')
    >>> std_sos
    std(Sp)
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[24]
    >>> std_sos(alloy)
    501.4478475933464
    """

    def __init__(self, prop):
        self.prop = property_id(prop)
        self.string = 'std({})'.format(properties.symbol_2char[self.prop])

    def __call__(self, alloy):
        """
        :param alloy: data series with elements representing mixture coefficients of elements
            with names matching the chemical element names: 'H', 'He', 'Li', 'Be', etc.
        :return: standard deviation value of property in atomic population described by alloy
        """
        dist = element_dist(alloy)
        m = sum(p*prop_value(el, self.prop) for el, p in dist.items())
        return sum(p*(prop_value(el, self.prop) - m)**2 for el, p in dist.items())**0.5

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class Skew:
    """

    For example:
    >>> skew_sos = Skew('Speed of Sound')
    >>> skew_sos
    skew(Sp)
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> alloy = alloys.iloc[24]
    >>> skew_sos(alloy)
    -5.624748000662498
    """

    def __init__(self, prop):
        self.prop = property_id(prop)
        self.string = 'skew({})'.format(properties.symbol_2char[self.prop])

    def __call__(self, alloy):
        """
        :param alloy: data series with elements representing mixture coefficients of elements
            with names matching the chemical element names: 'H', 'He', 'Li', 'Be', etc.
        :return: standard deviation value of property in atomic population described by alloy
        """
        dist = element_dist(alloy)
        m = sum(p*prop_value(el, self.prop) for el, p in dist.items())
        var = sum(p * (prop_value(el, self.prop) - m) ** 2 for el, p in dist.items())
        if var == 0:
            return 0.0

        m3 = sum(p*(prop_value(el, self.prop) - m)**3 for el, p in dist.items())

        return m3/(var**(3/2))

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.string


class FeatureMap:
    """
    Feature map that maps alloys into representation space of atomic
    population features.

    >>> feat_map = FeatureMap(['Speed of Sound', 'Mean Lattice Constant'], feat_types=[Mean, StdDev, Skew])
    >>> feat_map
    AtomicFeatureMap(mean(Sp), std(Sp), skew(Sp), mean(LC), std(LC), skew(LC))
    >>> alloys = datasets.Al_maxUTS_MIF()
    >>> a = alloys.iloc[24]
    >>> a.name
    '2030-T3510'
    >>> b = feat_map(a)
    >>> b.name
    '2030-T3510'
    >>> b.values
    array([4991.988     ,  501.44784759,   -5.624748  ,  407.0536847 ,
             39.80294738,   10.86585838])
    >>> alloys_trans = alloys.apply(feat_map, axis=1)
    >>> alloys_trans.columns
    Index(['mean(Sp)', 'std(Sp)', 'skew(Sp)', 'mean(LC)', 'std(LC)', 'skew(LC)'], dtype='object')
    """

    def __init__(self, props, feat_types=[Mean]):
        """
        :param props: iterable collection of atomic properties used for feature representation
        :param feat_types: parameters of property distribution to compute the final features
        """
        self.features = [ft(prop) for prop in props for ft in feat_types]
        self.index = pd.Index(str(f) for f in self.features)
        self.string = 'AtomicFeatureMap({})'.format(', '.join(map(str, self.features)))

    def __call__(self, alloy):
        return pd.Series((f(alloy) for f in self.features), index=self.index, name=alloy.name)

    def __repr__(self):
        return self.string


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
