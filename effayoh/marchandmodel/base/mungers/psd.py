"""
Provides a PSDMunger configured in accordance with the base Marchand
model.

"""
from __future__ import division, absolute_import, print_function
from builtins import super

from effayoh.mungers.psd import (
    PSDCommodity, PSDCommodityGroup, PSDCountry, PSDAttribute, PSDMunger
)

# Define the attribute used in the base Marchand model.

ENDING_STOCKS = PSDAttribute(attr_id="176", desc="Ending Stocks")


# Define the commodities used in the base Marchand model. These can be
# found in the Data section of the Marchand paper.

BARLEY = PSDCommodity(code="0430000", desc="Barley")
CORN = PSDCommodity(code="0440000", desc="Corn")
MILLET = PSDCommodity(code="0459100", desc="Millet")
MIXED_GRAIN = PSDCommodity(code="0459900", desc="Mixed Grain")
OATS = PSDCommodity(code="0452000", desc="Oats")
RICE_MILLED = PSDCommodity(code="0422110", desc="Rice, Milled")
RYE = PSDCommodity(code="0451000", desc="Rye")
SORGHUM = PSDCommodity(code="0459200", desc="Sorghum")
WHEAT = PSDCommodity(code="0410000", desc="Wheat")

COMMODITIES = [
    BARLEY,
    CORN,
    MILLET,
    MIXED_GRAIN,
    OATS,
    RICE_MILLED,
    RYE,
    SORGHUM,
    WHEAT
]

# Define (commodity, attribute) conversion factors.
# The unit of these attributes is 1000 MT so we
# also multiply by 1000.0.

item_attribute_factor = {
    (BARLEY, ENDING_STOCKS): 3.32*1000.0,
    (CORN, ENDING_STOCKS): 3.56*1000.0,
    (MILLET, ENDING_STOCKS): 3.4*1000.0,
    (MIXED_GRAIN, ENDING_STOCKS): 3.4*1000.0,
    (OATS, ENDING_STOCKS): 3.85*1000.0,
    (RICE_MILLED, ENDING_STOCKS): 3.6*1000.0,
    (RYE, ENDING_STOCKS): 3.19*1000.0,
    (SORGHUM, ENDING_STOCKS): 3.43*1000.0,
    (WHEAT, ENDING_STOCKS): 3.34*1000.0
}


class BasePSDMunger(PSDMunger):

    def __init__(self, political_rectifier):
        super().__init__(political_rectifier)

        # Add attribute element conversions.
        for (commodity, attribute), factor in item_attribute_factor.items():
            self.set_attribute_commodity_conversion(
                attribute,
                commodity,
                lambda x, factor=factor: x*factor
            )

        # Add attribute commodities group.
        self.add_attribute_commodities_group(
            ENDING_STOCKS,
            PSDCommodityGroup(COMMODITIES, "reserves")
        )
