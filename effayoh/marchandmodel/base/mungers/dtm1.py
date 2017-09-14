"""
Provides a DTMMunger configured in accordance with the base Marchand
model.

Several of the items listed in the Marchand paper do not appear in the
data used in development.

"""
from __future__ import division, absolute_import, print_function
from builtins import super

from effayoh.mungers.dtm import (
    DTMItem, DTMItemGroup, DTMElement, DTMMunger
)

EXPORT_TONNES = DTMElement(element="Export Quantity", code="5910")

# Define the items used in the base Marchand model which are enumerated
# in Table 2 of the Supplementary Data. Several of the items listed in
# the table do not occur in the definitions and standards associated
# with the detailed trade matrix, they are:
#
# Crop name - item code
# Rice, paddy - 27
# Rice Husked - 28
# Milled/Husked Rice - 29
# Rice Milled - 31
# Rice Broken - 32
# Rice Flour - 38
# Pot Barlety - 45
# Barley Flour and Grits - 48
# Malt Extract - 50
# Flour of Rye - 72
# Flour of Millet - 80
# Flour of Sorghum - 84
# Flour of Buckwheat - 89
# Quinoa - 92
# Cereals, nes - 108
WHEAT = DTMItem(item="Wheat", code="15")
FLOUR_OF_WHEAT = DTMItem(item="Flour, wheat", code="16")
MACARONI = DTMItem(item="Macaroni", code="18")
GERM_OF_WHEAT = None
BREAD = DTMItem(item="Bread", code="20")
BULGUR = DTMItem(item="Bulgur", code="21")
PASTRY = DTMItem(item="Pastry", code="22")
RICE = DTMItem(item="Rice - total  (Rice milled equivalent)", code="30")
BREAKFAST_CEREALS = DTMItem(item="Cereals, breakfast", code="41")
BARLEY = DTMItem(item="Barley", code="44")
BARLEY_PEARLED = DTMItem(item="Barley, pearled", code="46")
MALT = DTMItem(item="Malt", code="49")
MAIZE = DTMItem(item="Maize", code="56")
GERM_OF_MAIZE = DTMItem(item="Germ, maize", code="57")
FLOUR_OF_MAIZE = DTMItem(item="Flour, maize", code="58")
POPCORN = DTMItem(item="Popcorn", code="68")
RYE = DTMItem(item="Rye", code="71")
OATS = DTMItem(item="Oats", code="75")
OATS_ROLLED = DTMItem(item="Oats rolled", code="76")
MILLET = DTMItem(item="Millet", code="79")
SORGHUM = DTMItem(item="Sorghum", code="83")
BUCKWHEAT = DTMItem(item="Buckwheat", code="89")
FONIO = DTMItem(item="Fonio", code="94")
FLOUR_OF_FONIO = DTMItem(item="Flour, fonio", code="95")
TRITICALE = DTMItem(item="Triticale", code="97")
CANARY_SEED = DTMItem(item="Canary seed", code="101")
MIXED_GRAIN = DTMItem(item="Grain, mixed", code="103")
FLOUR_OF_MIXED_GRAIN = DTMItem(item="Flour, mixed grain", code="104")
INFANT_FOOD = DTMItem(item="Infant food", code="109")
WAFERS = DTMItem(item="Infant food", code="110")
FLOUR_OF_CEREALS = DTMItem(item="Flour, cereals", code="111")
CEREAL_PREPARATIONS_NES = DTMItem(item="Cereal preparations, nes", code="113")
MIXES_AND_DOUGHS = DTMItem(item="Mixes and doughs", code="114")
FOOD_PREP_FLOUR_MALT_EXTRACT = DTMItem(item="Food preparations, flour, malt extract", code="115")


# Conversion factors (10^6 kcal / ton)
# Obtained from Table 2 of Supplementary Data for the Marchand
# et al paper.
calories_per_ton = {
    WHEAT: 3.34,
    FLOUR_OF_WHEAT: 3.64,
    MACARONI: 3.67,
    BREAD: 2.49,
    BULGUR: 3.45,
    PASTRY: 3.69,
    RICE:3.6,
    BREAKFAST_CEREALS: 3.89,
    BARLEY:3.32,
    BARLEY_PEARLED: 3.46,
    MALT: 3.68,
    MAIZE: 3.56,
    GERM_OF_MAIZE:3.73,
    FLOUR_OF_MAIZE: 3.63,
    POPCORN: 3.56,
    RYE:3.19,
    OATS: 3.85,
    OATS_ROLLED: 3.84,
    MILLET: 3.40,
    SORGHUM: 3.43,
    BUCKWHEAT: 3.30,
    FONIO: 3.38,
    FLOUR_OF_FONIO: 3.55,
    TRITICALE: 3.27,
    CANARY_SEED: 3.88,
    MIXED_GRAIN: 3.40,
    FLOUR_OF_MIXED_GRAIN: 3.64,
    INFANT_FOOD: 3.68,
    WAFERS: 4.39,
    FLOUR_OF_CEREALS: 3.64,
    CEREAL_PREPARATIONS_NES: 3.64,
    MIXES_AND_DOUGHS: 3.93,
    FOOD_PREP_FLOUR_MALT_EXTRACT: 3.77
}


def calorie_cereals_exports_converter(item_tons):
    """
    Return the sum of the items kilocalories.
    """
    item_calories = {
        item: item_tons[item]
              for item in item_tons
    }
    return sum(item_calories.values())

ITEMS = (
    WHEAT, FLOUR_OF_WHEAT, MACARONI, BREAD, BULGUR,
    PASTRY, RICE, BREAKFAST_CEREALS, BARLEY, BARLEY_PEARLED,
    MALT, MAIZE, GERM_OF_MAIZE, FLOUR_OF_MAIZE, POPCORN,
    RYE, OATS, OATS_ROLLED, MILLET, SORGHUM, BUCKWHEAT,
    FONIO, FLOUR_OF_FONIO, TRITICALE, CANARY_SEED,
    MIXED_GRAIN, FLOUR_OF_MIXED_GRAIN, INFANT_FOOD, WAFERS,
    FLOUR_OF_CEREALS, CEREAL_PREPARATIONS_NES, MIXES_AND_DOUGHS,
    FOOD_PREP_FLOUR_MALT_EXTRACT
)

# Base element-items group of the model.
calorie_cereals_exports = (
    EXPORT_TONNES,  # element
    "exports",  # attribute name
    ITEMS,
    calorie_cereals_exports_converter  # conversion function
)


class BaseDTMMunger1(DTMMunger):

    def __init__(self, political_rectifier):
        super().__init__(political_rectifier)

        element, attr_name, items, conversion = calorie_cereals_exports
        items_group = DTMItemGroup(attr_name, items)
        self.add_element_items_group(element, items_group)
        self.set_element_items_group_conversion(
            element,
            items_group,
            conversion
        )
