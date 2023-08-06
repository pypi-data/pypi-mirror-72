from copy import deepcopy
import numpy as np

class Value(object):
    """A single value with uncertainties.

    :param nominal: nominal value
    :type nominal: ``float``
    :param uncorr_variations: dictionary of variations that are uncorrelated between different :py:class:`heppy.value` objects even when they have the same key
    :type uncorr_variations: ``dict`` of ``str`` and ``float``
    :param corr_variations: dictionary of variations that are fully correlated between different :py:class:`heppy.value` objects when they have the same key, and uncorrelated otherwise
    :type corr_variations: ``dict`` of ``str`` and ``float``
    :param attributes: dictionary of completely arbitrary attributes that the user can provide/change/access. E.g. information about the data sample that produced the value
    :type attributes: :code:`dict`
    """
    def __init__(self, nominal, uncorr_variations={}, corr_variations={}, attributes={}):
        super(Value, self).__init__()
        self.nominal = nominal
        self.uncorr_variations = deepcopy(uncorr_variations)
        self.corr_variations = deepcopy(corr_variations)
        self.attributes = deepcopy(attributes)



    def to_atlasiff(self, attributes={}, up_suffix='__1up', down_suffix='__1down'):
        """Returns string representation in ATLAS IFF format.

        This is the XML format used by the fake-lepton background tool of the
        ATLAS Isolation and Fakes Forum.

        :param attributes: dictionary of attributes to put in the bin-tag
        :type attributes: ``dict``
        :param up_suffix: suffix in variation keys to designate an up variation
        :type attributes: ``str``
        :param down_suffix: suffix in variation keys to designate an down variation
        :type attributes: ``str``

        Usage example:

        .. code-block:: python

            >>> import heppy as hp
            >>> nominal = 12.3
            >>> uncorr_variations = {
                    'stat__1up' : 12.4,
                    'stat__1down' : 12.1,
                    }
            >>> corr_variations={
                    'efficiency__1up' : 13.1,
                    'efficiency__1down' : 9.8,
                    'energy_scale__1up' : 10.5,
                    }
            >>> v = hp.Value(nominal, uncorr_variations=uncorr_variations, corr_variations=corr_variations)
            >>> v.to_atlasiff(attributes={'pt' : '[20,inf]', '|eta|' : '[0.0,0.6]'})
            '<bin pt="[20,inf]" |eta|="[0.0,0.6]"> 12.3 +0.1-0.2 (stat) -1.8+0.0 (energy_scale) +0.8-2.5 (efficiency) </bin>'

        """
        attribute_string = ' '.join([f'{key}="{val}"' for key, val in attributes.items()])
        stripped_uncorr_keys = set([key.replace(up_suffix, '').replace(down_suffix, '') for key in self.uncorr_variations.keys()])
        uncorr_string = ' '.join([f'{np.format_float_positional(self.uncorr_variations.get(stripped_key+up_suffix, self.nominal)-self.nominal, precision=7, sign=True)}{np.format_float_positional(self.uncorr_variations.get(stripped_key+down_suffix, self.nominal)-self.nominal, precision=7, sign=True)} ({stripped_key})' for stripped_key in stripped_uncorr_keys])
        stripped_corr_keys = set([key.replace(up_suffix, '').replace(down_suffix, '') for key in self.corr_variations.keys()])
        corr_string = ' '.join([f'{np.format_float_positional(self.corr_variations.get(stripped_key+up_suffix, self.nominal)-self.nominal, precision=7, sign=True)}{np.format_float_positional(self.corr_variations.get(stripped_key+down_suffix, self.nominal)-self.nominal, precision=7, sign=True)} ({stripped_key})' for stripped_key in stripped_corr_keys])
        return f'<bin {attribute_string}> {np.format_float_positional(self.nominal, precision=7)} {uncorr_string} {corr_string} </bin>'









