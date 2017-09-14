import os
import unittest

from effayoh.marchandmodel.builder import MarchandModelBuilder
from effayoh.marchandmodel.base.mungers import fbs
from effayoh.marchandmodel.base.mungers import psd
from effayoh.marchandmodel.base.mungers import dtm

from effayoh.mungers import FAOCountry
from effayoh.marchandmodel.base.mungers.dtm import BaseDTMMunger
from effayoh.resources.faostat import map as fao_map
from effayoh.marchandmodel.base.mungers.fbs import BaseFBSMunger
from effayoh.mungers.psd import PSDCountry, PSDCommodityGroup
from effayoh.marchandmodel.base.mungers.psd import (
    item_attribute_factor, ENDING_STOCKS, COMMODITIES
)
from effayoh.resources.usda import map as psd_map


TESTS_DIR, _ = os.path.split(__file__)
RESOURCES_DIR = os.path.join(TESTS_DIR, "resources")


class TestBaseDTMMunger(BaseDTMMunger):

    def __init__(self, political_rectifier):
        super().__init__(political_rectifier)

        data_path = os.path.join(RESOURCES_DIR,
                                 "fao",
                                 "dtm",
                                 "dtm_simple-4-network.csv")
        self.set_data_path(data_path)


class TestBaseFBSMunger(BaseFBSMunger):

    def __init__(self, political_rectifier):
        super().__init__(political_rectifier)

        data_path = os.path.join(RESOURCES_DIR,
                                 "fao",
                                 "fbs",
                                 "fbs_simple-4-network.csv")
        self.set_data_path(data_path)


item_attribute_factor = {
    key: value/1000.0 for key, value in item_attribute_factor.items()
}


class TestBasePSDMunger(psd.PSDMunger):

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

        data_path = os.path.join(RESOURCES_DIR,
                                 "usda",
                                 "psd",
                                 "psd_simple-4-network.csv")
        self.set_data_path(data_path)


def build_model():

    builder = MarchandModelBuilder()

    builder.set_years(list(range(2005, 2010)))
    # Base model parameters. Values taken from the paper
    # introducing the model.
    #
    # fc: fraction of residual shock absorbed by C if R is depleted
    # fr: fraction of actual reserves that are available to absorb
    #     shocks.
    # fp: magnitude of initial shock as a fraction of the affected
    #     country's P.
    # alpha: minimum threshold for a shock to be propagated.
    builder.add_static_param("fc", 0.01)
    builder.add_static_param("fr", 0.5)
    builder.add_static_param("fp", 0.2)
    builder.add_static_param("alpha", 0.001)

    # Register data sources.
    builder.register_data_source(TestBaseDTMMunger, FAOCountry, fao_map)
    builder.register_data_source(TestBaseFBSMunger, FAOCountry, fao_map)
    builder.register_data_source(TestBasePSDMunger, PSDCountry, psd_map)

    builder.add_network_initializer(MarchandModelBuilder.supply_initializer)
    builder.add_network_initializer(MarchandModelBuilder.shocked_initializer)
    builder.add_network_initializer(
        MarchandModelBuilder.consumption_initializer
    )
    builder.add_network_initializer(
        MarchandModelBuilder.reserves_initializer
    )

    model = builder.build()
    return model


class TestNetworkSetup(unittest.TestCase):

    def setUp(self):
        self.model = build_model()

    def test_consumption(self):
        """ Test the initial network values for consumption. """

        items_elements = {
            (item, element): fbs.item_element_conversions[(item, element)]
                             for item in fbs.ITEMS
                             for element in fbs.ELEMENTS[:-1]
        }
        expected = sum(items_elements.values())

        nodes = self.model.network.node
        usa_consumption = nodes["USA"]["consumption"]
        self.assertTrue(abs(usa_consumption - expected) < 0.001)

        china_consumption = nodes["CHINA"]["consumption"]
        self.assertTrue(abs(china_consumption - 2*expected) < 0.001)

        germany_consumption = nodes["GERMANY"]["consumption"]
        self.assertTrue(abs(germany_consumption - 3*expected) < 0.001)

        russia_consumption = nodes["RUSSIA"]["consumption"]
        self.assertTrue(abs(russia_consumption - 4*expected) < 0.001)

    def test_production(self):
        """ Test the initial network values for production. """

        items_elements = {
            (item, element): fbs.item_element_conversions[(item, element)]
                             for item in fbs.ITEMS
                             for element in fbs.ELEMENTS[-1:]
        }
        expected = sum(items_elements.values())

        nodes = self.model.network.node
        usa_production = nodes["USA"]["production"]
        self.assertTrue(abs(usa_production - expected) < 0.001)

        china_production = nodes["CHINA"]["production"]
        self.assertTrue(abs(china_production - 2*expected) < 0.001)

        germany_production = nodes["GERMANY"]["production"]
        self.assertTrue(abs(germany_production - 3*expected) < 0.001)

        russia_production = nodes["RUSSIA"]["production"]
        self.assertTrue(abs(russia_production - 4*expected) < 0.001)

    def test_reserves(self):
        """ Test the initial network values for reserves. """

        expected = sum(item_attribute_factor.values())
        nodes = self.model.network.node

        usa_production = nodes["USA"]["reserves"]
        self.assertTrue(abs(usa_production - expected) < 0.001)

        china_production = nodes["CHINA"]["reserves"]
        self.assertTrue(abs(china_production - 2*expected) < 0.001)

        germany_production = nodes["GERMANY"]["reserves"]
        self.assertTrue(abs(germany_production - 3*expected) < 0.001)

        russia_production = nodes["RUSSIA"]["reserves"]
        self.assertTrue(abs(russia_production - 4*expected) < 0.001)

    def test_exports(self):
        """ Test the initial network values of export edges. """

        expected = sum(dtm.calories_per_ton.values())
        network = self.model.network

        for usa, partner in network.out_edges("USA"):
            exports = network[usa][partner]["exports"]
            self.assertTrue(abs(0.1*expected - exports) < 0.001)

        for china, partner in network.out_edges("CHINA"):
            exports = network[china][partner]["exports"]
            self.assertTrue(abs(0.2*expected - exports) < 0.001)

        for germany, partner in network.out_edges("GERMANY"):
            exports = network[germany][partner]["exports"]
            self.assertTrue(abs(0.3*expected - exports) < 0.001)

        for russia, partner in network.out_edges("RUSSIA"):
            exports = network[russia][partner]["exports"]
            self.assertTrue(abs(0.4*expected - exports) < 0.001)


if __name__ == "__main__":
    unittest.main()
