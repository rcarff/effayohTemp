"""
Provides an FBSMunger configured in accordance with the base Marchand
model.

"""

from __future__ import division, absolute_import, print_function
from builtins import super

from effayoh.mungers.fbs import (
    FBSItem, FBSItemGroup, FBSElement, FBSElementGroup,
    FBSItemsElementsGroup, FBSMunger
)


# Define the items used in the base Marchand model. These are obtained
# by matching the composition of an item defined for the food balance
# sheet with the items used in the detailed trade matrix.
#
# Item - Code - Composition - Not in Table 2.
# Wheat and products - 2511 -
#   (15, Wheat), (16, Flour, wheat), (17, Bran), (18, Macaroni),
#   (19, Germ), (20, Bread), (21, Bulgur), (22, Pastry),
#   (23, Starch, wheat), (24, Gluten, wheat), (41, Cereals, breakfast),
#   (110, Wafers), (114, Mixes and doughs),
#   (115, Food preparations, flour, malt extract)
#   -
#   (17, Bran), (23, Starch, wheat), (24, Gluten, wheat)
# Rice (Milled Equivalent) - 2805 -
#   (27, Rice, paddy), (28, Rice, husked), (29, Rice, milled/husked),
#   (31, Rice, milled), (32, Rice, broken), (33, Gluten, rice),
#   (34, Starch, rice), (35, Bran, rice), (38, Flour, rice)
#   -
#   (33, Gluten, rice), (34, Starch, rice), (35, Bran, rice)
# Barley and products - 2513 -
#   (44, Barley), (45, Barley, pot), (46, Barley, pearled),
#   (47, Bran, barley), (48, Flour, barley and grits), (49, Malt),
#   (50, Malt extract)
#   -
#   (47, Bran, barley)
# Maize and products - 2514 -
#   (56, Maize), (57, Germ, maize), (58, Flour, maize),
#   (59, Bran, maize), (63, Gluten, maize), (64, Starch, maize)
#   (864, Feed and meal gluten)
#   -
#   (59, Bran, maize), (63, Gluten, maize), (64, Starch, maize),
#   (864, Feed and meal, gluten)
# Cereals, other - 2520 -
#   (68, Popcorn), (89, Buckwheat), (90, Flour, buckwheat),
#   (91, Bran, buckwheat), (92, Quinoa), (94, Fonio),
#   (95, Flour, fonio), (96, Bran, fonio), (97, Triticale),
#   (98, Flour, triticale), (99, Bran, triticale), (101, Canary seed),
#   (103, Grain, mixed), (104, Flour, mixed grain),
#   (105, Bran, mixed grains), (108, Cereals, nes),
#   (111, Flour, cereals), (112, Bran, cereals nes),
#   (113, Cereal preparations, nes)
#   -
#   (91, Bran, buckwheat), (96, Bran, fonio), (98, Flour, triticale),
#   (99, Bran, triticale), (105, Bran, mixed grains),
#   (112, Bran, cereals nes)
# Rye and products - 2515 -
#   (71, Rye), (72, Flour, rye), (73, Bran, rye)
#   -
#   (73, Bran, rye)
# Oats - 2516 -
#   (75, Oats), (76, Oats rolled), (77, Bran, oats)
#   -
#   (77, Bran, oats)
# Millet and products - 2517 -
#   (79, Millet), (80, Flour, millet), (81, Bran, millet)
#   -
#   (81, Bran, millet)
# Sorghum and products - 2518 -
#   (83, Sorghum), (84, Flour, sorghum), (85, Bran, sorghum)
#   -
#   (85, Bran, sorghum)
# Infant food - 2680 -
#   (109, Infant food)


# Abridged item list.
# Code - Item
# 2511 - Wheat and products
# 2805 - Rice (Milled Equivalent)
# 2513 - Barley and products
# 2514 - Maize and products
# 2520 - Cereals, other
# 2515 - Rye and products
# 2516 - Oats
# 2517 - Millet and products
# 2518 - Sorghum and products
# 2680 - Infant food

WHEAT = FBSItem(item="Wheat and products", code="2511")
RICE = FBSItem(item="Rice (Milled Equivalent)", code="2805")
BARLEY = FBSItem(item="Barley and products", code="2513")
MAIZE = FBSItem(item="Maize and products", code="2514")
CEREALS_OTHER = FBSItem(item="Cereals, other", code="2520")
RYE = FBSItem(item="Rye and products", code="2515")
OATS = FBSItem(item="Oats", code="2516")
MILLET = FBSItem(item="Millet and products", code="2517")
SORGHUM = FBSItem(item="Sorghum and products", code="2518")
INFANT_FOOD = FBSItem(item="Infant food", code="2680")

ITEMS = [
    WHEAT,
    RICE,
    BARLEY,
    MAIZE,
    CEREALS_OTHER,
    RYE,
    OATS,
    MILLET,
    SORGHUM,
    INFANT_FOOD
]

# Define the elements used in the base Marchand model. These are taken
# from Table 3 which shows total consumption to be composed of 6
# elements.
#
# Element - Code
# Food - 5142
# Feed - 5521
# Seed - 5527
# Processing - 5131
# Waste - 5123
# Other uses - 5154
# Production - 5511

FOOD = FBSElement(element="Food", code="5142")
FEED = FBSElement(element="Feed", code="5521")
SEED = FBSElement(element="Seed", code="5527")
PROCESSING = FBSElement(element="Processing", code="5131")
WASTE = FBSElement(element="Waste", code="5123")
OTHER = FBSElement(element="Other uses", code="5154")
PRODUCTION = FBSElement(element="Production", code="5511")

ELEMENTS = [
    FOOD,
    FEED,
    SEED,
    PROCESSING,
    WASTE,
    OTHER,
    PRODUCTION,
]

# Define (item, element) conversion factors.
# The unit of these elements is 1000 tonnes so we have to multiply the
# per ton conversion factor from Table 2 by 1000.

item_element_conversions = {
    (WHEAT, FOOD): 3.34*1000.0,
    (WHEAT, FEED): 3.34*1000.0,
    (WHEAT, SEED): 3.34*1000.0,
    (WHEAT, PROCESSING): 3.34*1000.0,
    (WHEAT, WASTE): 3.34*1000.0,
    (WHEAT, OTHER): 3.34*1000.0,
    (WHEAT, PRODUCTION): 3.34*1000.0,
    (RICE, FOOD): 3.6*1000.0,
    (RICE, FEED): 3.6*1000.0,
    (RICE, SEED): 3.6*1000.0,
    (RICE, PROCESSING): 3.6*1000.0,
    (RICE, WASTE): 3.6*1000.0,
    (RICE, OTHER): 3.6*1000.0,
    (RICE, PRODUCTION): 3.6*1000.0,
    (BARLEY, FOOD): 3.32*1000.0,
    (BARLEY, FEED): 3.32*1000.0,
    (BARLEY, SEED): 3.32*1000.0,
    (BARLEY, PROCESSING): 3.32*1000.0,
    (BARLEY, WASTE): 3.32*1000.0,
    (BARLEY, OTHER): 3.32*1000.0,
    (BARLEY, PRODUCTION): 3.32*1000.0,
    (MAIZE, FOOD): 3.56*1000.0,
    (MAIZE, FEED): 3.56*1000.0,
    (MAIZE, SEED): 3.56*1000.0,
    (MAIZE, PROCESSING): 3.56*1000.0,
    (MAIZE, WASTE): 3.56*1000.0,
    (MAIZE, OTHER): 3.56*1000.0,
    (MAIZE, PRODUCTION): 3.56*1000.0,
    (CEREALS_OTHER, FOOD): 3.3*1000.0,
    (CEREALS_OTHER, FEED): 3.3*1000.0,
    (CEREALS_OTHER, SEED): 3.3*1000.0,
    (CEREALS_OTHER, PROCESSING): 3.3*1000.0,
    (CEREALS_OTHER, WASTE): 3.3*1000.0,
    (CEREALS_OTHER, OTHER): 3.3*1000.0,
    (CEREALS_OTHER, PRODUCTION): 3.3*1000.0,
    (RYE, FOOD): 3.19*1000.0,
    (RYE, FEED): 3.19*1000.0,
    (RYE, SEED): 3.19*1000.0,
    (RYE, PROCESSING): 3.19*1000.0,
    (RYE, WASTE): 3.19*1000.0,
    (RYE, OTHER): 3.19*1000.0,
    (RYE, PRODUCTION): 3.19*1000.0,
    (OATS, FOOD): 3.85*1000.0,
    (OATS, FEED): 3.85*1000.0,
    (OATS, SEED): 3.85*1000.0,
    (OATS, PROCESSING): 3.85*1000.0,
    (OATS, WASTE): 3.85*1000.0,
    (OATS, OTHER): 3.85*1000.0,
    (OATS, PRODUCTION): 3.85*1000.0,
    (MILLET, FOOD): 3.4*1000.0,
    (MILLET, FEED): 3.4*1000.0,
    (MILLET, SEED): 3.4*1000.0,
    (MILLET, PROCESSING): 3.4*1000.0,
    (MILLET, WASTE): 3.4*1000.0,
    (MILLET, OTHER): 3.4*1000.0,
    (MILLET, PRODUCTION): 3.4*1000.0,
    (SORGHUM, FOOD): 3.43*1000.0,
    (SORGHUM, FEED): 3.43*1000.0,
    (SORGHUM, SEED): 3.43*1000.0,
    (SORGHUM, PROCESSING): 3.43*1000.0,
    (SORGHUM, WASTE): 3.43*1000.0,
    (SORGHUM, OTHER): 3.43*1000.0,
    (SORGHUM, PRODUCTION): 3.43*1000.0,
    (INFANT_FOOD, FOOD): 3.68*1000.0,
    (INFANT_FOOD, FEED): 3.68*1000.0,
    (INFANT_FOOD, SEED): 3.68*1000.0,
    (INFANT_FOOD, PROCESSING): 3.68*1000.0,
    (INFANT_FOOD, WASTE): 3.68*1000.0,
    (INFANT_FOOD, OTHER): 3.68*1000.0,
    (INFANT_FOOD, PRODUCTION): 3.68*1000.0
}


class BaseFBSMunger(FBSMunger):

    consumption = FBSItemsElementsGroup(
        attr_name="consumption",
        items_group=FBSItemGroup(ITEMS),
        elements_group=FBSElementGroup(ELEMENTS[:-1])  # Exclude Production
    )

    production = FBSItemsElementsGroup(
        attr_name="production",
        items_group=FBSItemGroup(ITEMS),
        elements_group=FBSElementGroup(ELEMENTS[-1:])  # Only Production
    )

    def __init__(self, political_rectifier):
        super().__init__(political_rectifier)

        self.add_items_elements_group(BaseFBSMunger.consumption)
        self.add_items_elements_group(BaseFBSMunger.production)
        for (item, element), factor in item_element_conversions.items():
            self.set_item_element_conversion(
                item,
                element,
                lambda x, factor=factor: x*factor
            )
