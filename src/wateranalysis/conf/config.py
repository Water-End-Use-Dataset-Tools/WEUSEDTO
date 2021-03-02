'''
Conf
=================================
This module include global configuration parameters for the software
'''
class Configuration:
    """
    This class define a correspondence between the name of the fixture and the filename of its time-series
    """
    facets_files = {
        'shower': 'feed_Shower.MYD.csv',
        "bidet": 'feed_Bidet.MYD.csv',
        "kitchen": 'feed_Kitchenfaucet.MYD.csv',
        "washbasin": 'feed_Washbasin.MYD.csv'
        }
