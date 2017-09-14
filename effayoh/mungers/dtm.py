"""
Provide the DTMMunger class for munging the Detailed Trade Matrix.

A typical processing step in the detailed trade matrix is to extract
the export trade links between all countries for a particular item. In
which case the Item and Element are fixed. Often we will want to
convert the value associated with each (item, element) coordinate. The
DTMMunger class exposes a dict item_element_conversions for associating
a function with an (item, element) coordinate for conversion.

Another typical processing step will be to combine the export trade
links for some collection of items, in which case the item is fixed for
a group of elements. Often we will want to combine the values of each
(item, element) coordinate to obtain one value for the (element, items)
coordinate. The DTMMunger class exposes a dict item_group_conversions
for this purpose.

"""
from __future__ import division, absolute_import, print_function
from builtins import super

import os
import csv
import io

from effayoh.util import FAOSTAT_DIR
from effayoh.mungers import FAOCountry
from effayoh.resources.faostat import map as map_


class DTMItem(tuple):

    __slots__ = []
    object_pool = {}

    def __new__(cls, item, code):
        tup = (item, code)
        if tup in DTMItem.object_pool:
            return DTMItem.object_pool[tup]
        else:
            obj = super().__new__(cls, tup)
            DTMItem.object_pool[obj] = obj
            return obj


class DTMItemGroup(frozenset):

    __slots__ = ["attr_name"]

    def __new__(cls, attr_name, items):
        return super().__new__(cls, items)

    def __init__(self, attr_name, items):
        self.attr_name = attr_name


class DTMElement(tuple):

    __slots__ = []
    object_pool = {}

    def __new__(cls, element, code):
        tup = (element, code)
        if tup in DTMElement.object_pool:
            return DTMElement.object_pool[tup]
        else:
            obj = super().__new__(cls, tup)
            DTMElement.object_pool[obj] = obj
            return obj


class DTMMunger(object):
    """
    Data munger for the FAO Detailed Trade Matrix data.

    """

    def __init__(self, political_rectifier):
        self.data_path = None
        self.years = None
        self.items = set()
        self.elements = set()
        self.item_elem_edges = set()
        self.item_element_conversions = {}
        self.element_items_groups = set()
        self.element_items_group_conversions = {}
        self.political_rectifier = political_rectifier

    def set_data_path(self, data_path):
        self.data_path = data_path

    def set_years(self, years):
        self.years = years

    def add_item(self, item):
        self.items.add(item)

    def add_items(self, items):
        for item in items:
            self.items.add(item)

    def add_item_elem_edge(self, item, element):
        self.item_elem_edges.add((item, element))

    def set_item_element_conversion(self, item, element, conversion):
        if not isinstance(item, DTMItem):
            raise TypeError("item must be a DTMItem")
        if not isinstance(element, DTMElement):
            raise TypeError("element must be a DTMElement")
        if not callable(conversion):
            raise TypeError("conversion must be a callable")
        self.item_element_conversions[(item, element)] = conversion

    def add_element(self, element):
        self.elements.add(element)

    def add_element_items_group(self, element, items_group):
        if not isinstance(element, DTMElement):
            raise TypeError("element must be a DTMElement")
        if not isinstance(items_group, DTMItemGroup):
            raise TypeError("items_group must be a DTMItemGroup")
        self.add_element(element)
        self.add_items(items_group)
        self.element_items_groups.add((element, items_group))

    def set_element_items_group_conversion(self,
                                           element,
                                           items_group,
                                           conversion):
        """
        Store an element-items group conversion function.

        This function is used to customize how the values for each item
        in the group are combined.

        Parameters:
        -----------
        element : DTMElement
            The DTMElement that is used to group the items in
            items_group. Data will be extracted from rows in the
            detailed trade matrix that match this element and any item
            in items_group.
        items_group: DTMItemGroup
            The DTMItemGroup that contains the items being grouped.
        conversion: callable
            A callable that takes as argument a dict mapping each item
            in items_group to its value in the detailed trade matrix
            and returns the value resulting from the custom combination
            behavior, e.g. converting different cereals tonnes to
            calories and summing.

        Raises:
        -------
        TypeError
            If element is not a DTMElement.
            If items_group is not a DTMItemGroup.
            If conversion is not callable.

        """
        if not isinstance(element, DTMElement):
            raise TypeError("element must be a DTMElement")
        if not isinstance(items_group, DTMItemGroup):
            raise TypeError("items_group must be a DTMItemGroup")
        if not callable(conversion):
            raise TypeError("conversion must be a callable")
        key = (element, items_group)
        self.element_items_group_conversions[key] = conversion

    def munge(self):
        """
        Extract and process data in the FAO Detailed Trade Matrix.
        """
        data = self.get_raw_data()

        # Apply the (item, element)-wise conversions.
        for reporter_country, partners in data.items():
            for partner_country, elements in partners.items():
                for element, items in elements.items():
                    for item, years in items.items():
                        # Items in element-items groups will also be
                        # processed to obtain value here.
                        mean = sum(years.values()) / len(years)
                        func = self.item_element_conversions.get(
                            (item, element),
                            lambda x: x
                        )
                        value = func(mean)
                        items[item] = value

                        if (item, element) in self.item_elem_edges:
                            self.set_network_item_element_edge(
                                reporter_country,
                                partner_country,
                                item,
                                element,
                                value
                            )

        # Apply the element-items-group conversions.
        for element, items_group in self.element_items_groups:
            for reporter_country, partners in data.items():
                for partner_country, elements in partners.items():
                    if not element in elements:
                        continue
                    items = elements[element]
                    args = {item: items[item]
                            for item in items
                            if item in items_group}
                    func = self.element_items_group_conversions.get(
                        (element, items_group),
                        lambda x: sum(x.values())
                    )
                    value = func(args)
                    self.set_element_items_group_network_edge(
                        reporter_country,
                        partner_country,
                        element,
                        items_group,
                        value
                    )

    def get_raw_data(self):
        """
        Return a dict of trade matrix data.

        The dict is five dimensional keyed on: Reporter Country, Partner
        Country, Element, Item and Year.
        """
        if self.data_path:
            data_path = self.data_path
        else:
            data_path = os.path.join(
                FAOSTAT_DIR,
                "detailed-trade-matrix",
                "Trade_DetailedTradeMatrix_E_All_Data.csv"
            )

        data = {}
        years_fields = [(year, "Y" + str(year)) for year in self.years]

        with io.open(data_path, mode='rb') as csv_file:

            reader = csv.DictReader(csv_file)

            for row in reader:

                item = DTMItem(row["Item"], row["Item Code"])
                if not item in self.items:
                    continue

                element = DTMElement(row["Element"], row["Element Code"])
                if not element in self.elements:
                    continue

                # The row has one of the target item codes and one of
                # the target element codes but it might not have a value
                # for any of the years. We do the check here to avoid
                # creating chains of dicts in the data that ultimately
                # have no values.
                years_values = []
                for year, field in years_fields:
                    try:
                        value = float(row[field])
                        if value > 0.0:
                            years_values.append((year, value))
                    except ValueError as ve:
                        pass

                if not years_values:
                    continue

                reporter_country = FAOCountry(
                    row["Reporter Countries"],
                    row["Reporter Country Code"]
                )

                partner_country = FAOCountry(
                    row["Partner Countries"],
                    row["Partner Country Code"]
                )

                if not (reporter_country in map_ and partner_country in map_):
                    continue

                partners_dict = data.setdefault(reporter_country, {})
                element_dict = partners_dict.setdefault(partner_country, {})
                item_dict = element_dict.setdefault(element, {})
                years_dict = item_dict.setdefault(item, {})

                for year, value in years_values:
                    years_dict[year] = value

        self.data = data

        return data

    def set_network_item_element_edge(self,
                                      reporter_country,
                                      partner_country,
                                      item,
                                      element,
                                      value):
        name = "_".join([item[0], element[0]])
        self.political_rectifier.set_network_edge(
            reporter_country,
            partner_country,
            name,
            value
        )

    def set_element_items_group_network_edge(self,
                                             reporter_country,
                                             partner_country,
                                             element,
                                             items_group,
                                             value):
        self.political_rectifier.set_network_edge(
            reporter_country,
            partner_country,
            items_group.attr_name,
            value
        )
