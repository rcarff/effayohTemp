"""
Provide the munger for the USDA PSD data set, PSDMunger.

The only processing step in the Marchand model is to aggregate a
collection of commodities by an attribute.

"""

from __future__ import division, absolute_import, print_function
from builtins import super

import os
import csv

from effayoh.util import PSD_DIR


class PSDCommodity(tuple):

    __slots__ = []
    object_pool = {}

    def __new__(cls, code, desc):
        tup = (code, desc)
        if tup in PSDCommodity.object_pool:
            return PSDCommodity.object_pool[tup]
        else:
            psd_commodity = super().__new__(cls, tup)
            PSDCommodity.object_pool[psd_commodity] = psd_commodity
            return psd_commodity


class PSDCommodityGroup(frozenset):

    __slots__ = ["attr_name"]

    def __new__(cls, commodities, attr_name):
        return super().__new__(cls, commodities)

    def __init__(self, commodities, attr_name):
        self.attr_name = attr_name


class PSDCountry(tuple):

    __slots__ = []
    object_pool = {}

    def __new__(cls, code, name):
        tup = (code, name)
        if tup in PSDCountry.object_pool:
            return PSDCountry.object_pool[tup]
        else:
            obj = super().__new__(cls, tup)
            PSDCountry.object_pool[tup] = obj
            return obj


class PSDAttribute(tuple):

    __slots__ = []
    object_pool = {}

    def __new__(cls, attr_id, desc):
        tup = (attr_id, desc)
        if tup in PSDAttribute.object_pool:
            return PSDAttribute.object_pool[tup]
        else:
            obj = super().__new__(cls, tup)
            PSDAttribute.object_pool[tup] = obj
            return obj

class PSDMunger(object):
    """
    Data munger for the USDA PSD data set.

    """

    def __init__(self, political_rectifier):
        self.data_path = None
        self.years = None
        self.attributes = set()
        self.commodities = set()
        self.attribute_commodity_conversions = {}
        self.attribute_commodities_groups = set()
        self.attribute_commodities_group_conversions = {}
        self.political_rectifier = political_rectifier

    def set_data_path(self, data_path):
        self.data_path = data_path

    def set_years(self, years):
        self.years = years

    def set_attribute_commodity_conversion(self,
                                           attribute,
                                           commodity,
                                           conversion):
        if not isinstance(attribute, PSDAttribute):
            raise TypeError("attribute must be an instance of PSDAttribute")
        if not isinstance(commodity, PSDCommodity):
            raise TypeError("commodity must be an instance of PSDCommodity")
        if not callable(conversion):
            raise TypeError("conversion must be a callable")
        key = (attribute, commodity)
        self.attribute_commodity_conversions[key] = conversion

    def add_attribute_commodities_group(self, attribute, commodities_group):
        if not isinstance(attribute, PSDAttribute):
            raise TypeError("attribute must be a PSDAttribute")
        if not isinstance(commodities_group, PSDCommodityGroup):
            raise TypeError("commodities_group must be a PSDCommodityGroup")
        self.attribute_commodities_groups.add((attribute, commodities_group))
        self.commodities |= commodities_group
        self.attributes.add(attribute)

    def set_attribute_commodities_group_conversion(self,
                                                   attribute,
                                                   commodities_group,
                                                   conversion):
        if not isinstance(attribute, PSDAttribute):
            raise TypeError("attribute must be a PSDAttribute")
        if not isinstance(commodities_group, PSDCommodityGroup):
            raise TypeError("commodities_group must be a PSDCommodityGroup")
        if not callable(conversion):
            raise TypeError("conversion must be a callable")
        map_ = self.attribute_commodities_group_conversions
        map_[(attribute, commodities_group)] = conversion

    def munge(self):
        """
        Extract and process data in the USDA PSD data.
        """
        data = self.get_raw_data()

        # Apply the (attribute, commodity) conversions.
        for country, attributes in data.items():
            for attribute, commodities in attributes.items():
                for commodity, years in commodities.items():
                    mean = sum(years.values()) / len(years)
                    func = self.attribute_commodity_conversions.get(
                        (attribute, commodity),
                        lambda x: x
                    )
                    value = func(mean)
                    commodities[commodity] = value

        # Apply the (attribute, commodities-group) conversions.
        for attribute, cm_group in self.attribute_commodities_groups:
            for country, attributes in data.items():
                if not attribute in attributes:
                    continue
                commodities = attributes[attribute]
                args = {cm: commodities[cm]
                        for cm in commodities
                        if cm in cm_group}
                func = self.attribute_commodities_group_conversions.get(
                    (attribute, cm_group),
                    # If no (attribute, commodities-group) conversion
                    # is available, the default conversion unpacks the
                    # 2-key (commodity, year) dict and sums its values.
                    lambda x: sum(x.values())
                )
                value = func(args)
                self.set_network_node_attr(
                    country,
                    cm_group.attr_name,
                    value
                )

    def get_raw_data(self):
        """
        Return a dict of PSD data.

        The dict is four dimensional keyed on country, attribute,
        commodity and year.
        """
        if self.data_path:
            data_path = self.data_path
        else:
            data_path = os.path.join(PSD_DIR, "psd_alldata-2017-03-15.csv")

        data = {}
        years = {str(year): year for year in self.years}

        with open(data_path) as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                aid = row["Attribute_ID"]
                adesc = row["Attribute_Description"]
                attribute = PSDAttribute(aid, adesc)
                if not attribute in self.attributes:
                    continue

                commodity = PSDCommodity(
                    code=row["Commodity_Code"],
                    desc=row["Commodity_Description"]
                )
                if not commodity in self.commodities:
                    continue

                market_year = row["Market_Year"]
                if not market_year in years:
                    continue

                ccode, cname = row["Country_Code"], row["Country_Name"]
                country = PSDCountry(ccode, cname)

                value = float(row["Value"])

                attr_dict = data.setdefault(country, {})
                commodity_dict = attr_dict.setdefault(attribute, {})
                year_dict = commodity_dict.setdefault(commodity, {})

                year = years[market_year]
                year_dict[year] = value

        self.data = data

        return data

    def set_network_node_attr(self, country, name, value):
        self.political_rectifier.set_network_node_attr(
            country,
            name,
            value
        )
