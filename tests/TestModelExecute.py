import os
import unittest

from effayoh.marchandmodel.builder import MarchandModelBuilder
from effayoh.mungers.psd import PSDCountry
from effayoh.resources.usda import map as psd_map
from effayoh.mungers import FAOCountry
from effayoh.resources.faostat import map as fao_map

from TestNetworkSetup import (
    TestBaseDTMMunger, TestBaseFBSMunger, TestBasePSDMunger
)


def russian_exports_initializer(network):
    """ Initialize Russian exports to test cascade behavior. """
    network["RUSSIA"]["CHINA"]["exports"] = 0.0
    network["RUSSIA"]["GERMANY"]["exports"] = 0.0
    network["RUSSIA"]["USA"]["exports"] = 3000.0


def build_model(cascade_version=False, volumes_version=False):

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
    if volumes_version:
        fp = 6381.547 / 104010.0
    else:
        fp = 0.2
    builder.add_static_param("fr", 0.5)
    builder.add_static_param("fp", fp)
    builder.add_static_param("alpha", 0.0001)

    # Register data sources.
    builder.register_data_source(TestBaseDTMMunger, FAOCountry, fao_map)
    builder.register_data_source(TestBaseFBSMunger, FAOCountry, fao_map)
    builder.register_data_source(TestBasePSDMunger, PSDCountry, psd_map)

    if cascade_version:
        builder.add_network_initializer(russian_exports_initializer)

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


class TestModelExecute(unittest.TestCase):

    def test_execute(self):
        model = build_model()
        model.set_epicenter("USA")
        model.execute()
        network = model.network

        # Verify the state of USA.
        expected_reserves = 15.545
        expected_consumption = 201243.013
        expected_supply = 27948.202

        usa_data = network.node["USA"]
        actual_reserves = usa_data["reserves"]
        actual_consumption = usa_data["consumption"]
        actual_supply = usa_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of CHINA.
        expected_reserves = 31.09
        expected_consumption = 416035.723
        expected_supply = 69328.211

        china_data = network.node["CHINA"]
        actual_reserves = china_data["reserves"]
        actual_consumption = china_data["consumption"]
        actual_supply = china_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of GERMANY.
        expected_reserves = 46.635
        expected_consumption = 624059.479
        expected_supply = 103939.266

        germany_data = network.node["GERMANY"]
        actual_reserves = germany_data["reserves"]
        actual_consumption = germany_data["consumption"]
        actual_supply = germany_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of RUSSIA.
        expected_reserves = 65.415
        expected_consumption = 832080
        expected_supply = 138550.321

        russia_data = network.node["RUSSIA"]
        actual_reserves = russia_data["reserves"]
        actual_consumption = russia_data["consumption"]
        actual_supply = russia_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

    def test_cascade_execute(self):
        model = build_model(cascade_version=True)
        model.set_epicenter("RUSSIA")
        model.execute()
        network = model.network

        # Verify the state of USA.
        expected_reserves = 15.545
        expected_consumption = 205129.857
        expected_supply = 34787.89

        usa_data = network.node["USA"]
        actual_reserves = usa_data["reserves"]
        actual_consumption = usa_data["consumption"]
        actual_supply = usa_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of CHINA.
        expected_reserves = 19.301
        expected_consumption = 416023.934
        expected_supply = 69257.477

        china_data = network.node["CHINA"]
        actual_reserves = china_data["reserves"]
        actual_consumption = china_data["consumption"]
        actual_supply = china_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of GERMANY.
        expected_reserves = 28.9515
        expected_consumption = 624041.7955
        expected_supply = 103856.743

        germany_data = network.node["GERMANY"]
        actual_reserves = germany_data["reserves"]
        actual_consumption = germany_data["consumption"]
        actual_supply = germany_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of RUSSIA.
        expected_reserves = 38.602
        expected_consumption = 807476.914
        expected_supply = 111061.89

        russia_data = network.node["RUSSIA"]
        actual_reserves = russia_data["reserves"]
        actual_consumption = russia_data["consumption"]
        actual_supply = russia_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

    def test_volumes(self):
        model = build_model(volumes_version=True)
        model.set_epicenter("GERMANY")
        model.execute()
        network = model.network

        # Verify the state of USA.
        expected_reserves = 15.545
        expected_consumption = 208011.967
        expected_supply = 34717.156

        usa_data = network.node["USA"]
        actual_reserves = usa_data["reserves"]
        actual_consumption = usa_data["consumption"]
        actual_supply = usa_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of CHINA.
        expected_reserves = 32.7075
        expected_consumption = 416040.
        expected_supply = 69334.1055

        china_data = network.node["CHINA"]
        actual_reserves = china_data["reserves"]
        actual_consumption = china_data["consumption"]
        actual_supply = china_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of GERMANY.
        expected_reserves = 46.635
        expected_consumption = 617819.4
        expected_supply = 97699.187

        germany_data = network.node["GERMANY"]
        actual_reserves = germany_data["reserves"]
        actual_consumption = germany_data["consumption"]
        actual_supply = germany_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)

        # Verify the state of RUSSIA.
        expected_reserves = 83.0985
        expected_consumption = 832080.
        expected_supply = 138568.0045

        russia_data = network.node["RUSSIA"]
        actual_reserves = russia_data["reserves"]
        actual_consumption = russia_data["consumption"]
        actual_supply = russia_data["supply"]

        delta_reserves = abs(expected_reserves - actual_reserves)
        delta_consumption = abs(expected_consumption - actual_consumption)
        delta_supply = abs(expected_supply - actual_supply)

        self.assertTrue(delta_reserves < 0.001)
        self.assertTrue(delta_consumption < 0.001)
        self.assertTrue(delta_supply < 0.001)


if __name__ == "__main__":
    unittest.main()
