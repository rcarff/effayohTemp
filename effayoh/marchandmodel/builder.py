"""
Provide the MarchandModelBuilder.

"""
from __future__ import division, absolute_import, print_function

import funcsigs



from effayoh.marchandmodel import MarchandModel, MarchandModelError
from effayoh.marchandmodel.base import policy as base_policy

from effayoh.marchandmodel.base.filters.population_filter import (FAOSTATPopulationFilter)

from effayoh.mungers import FAOCountry
from effayoh.marchandmodel.base.mungers.dtm import BaseDTMMunger
from effayoh.resources.faostat import map as fao_map
from effayoh.marchandmodel.base.mungers.fbs import BaseFBSMunger

from effayoh.mungers.psd import PSDCountry
from effayoh.marchandmodel.base.mungers.psd import BasePSDMunger
from effayoh.resources.usda import map as psd_map




class MarchandModelBuilder:

    """
    A class that manages the complex Marchand model build process.

    """

    def __init__(self):
        self.years = []
        self.munger_classes = []
        self.filter_classes = []
        self.recorder_classes = []
        self.politent_maps = {}
        self.model_component_groups = []
        self.model_compound_politents = []

        self.network_initializers = []
        self.static_params = {}
        self.dynamic_params = {}
        self.policy = base_policy

    def set_years(self, years):
        """
        Set the years on the model and data mungers.
        """
        self.years = years

    def register_data_source(self,
                             munger_class,
                             politent_class,
                             politent_map):
        self.munger_classes.append(munger_class)
        self.politent_maps[politent_class] = politent_map

    def add_model_component_group(self, group):
        """
        Add a model component group to register at build time.
        """
        self.model_component_groups.append(group)

    def add_model_compound_politent(self, compound):
        """
        Add a compound model to register at build time.
        """
        self.model_compound_politents.append(compound)

    def add_network_initializer(self, initializer):
        """
        Add initializer to the collection of initializers.

        Inititializers will be executed in the order in which they are
        added to the builder. If an initializer, f, depends on a
        previous initializer, g, then it is up to the client code to
        add g to the builder before adding f.

        """
        if not callable(initializer):
            msg = "initializer must be a function."
            raise MarchandModelError(msg)

        signature = funcsigs.signature(initializer)
        if len(signature.parameters) != 1:
            msg = "initializer must be a monadic function."
            raise MarchandModelError(msg)

        self.network_initializers.append(initializer)

    def add_static_param(self, name, val):
        """ Add a static parameter to the builder. """
        self.static_params[name] = val

    def add_dynamic_param(self, name, func):
        """ Add a dynamic parameter to the builder. """
        if not callable(func):
            msg = "func must be a function."
            raise MarchandModelError(msg)

        self.dynamic_params[name] = func

    def set_policy(self, policy):
        """ Set the iteration policy for the model. """
        if not callable(policy):
            msg = "policy must be a function."
            raise MarchandModelError(msg)

        self.policy = policy

    def add_filter(self, filter_class):
        self.filter_classes.append(filter_class)

    def add_recorder(self, recorder_class):
        self.recorder_classes.append(recorder_class)

    def setup_base_model(self):
        """
        Setup the base Marchand model.

        """
        # Check self.years so that we do not clobber a client's
        # specified years.
        if not self.years:
            self.years = list(range(2005, 2014))

        # Base model parameters. Values taken from the paper
        # introducing the model.
        #
        # fc: fraction of residual shock absorbed by C if R is depleted
        # fr: fraction of actual reserves that are available to absorb
        #     shocks.
        # fp: magnitude of initial shock as a fraction of the affected
        #     country's P.
        # alpha: minimum threshold for a shock to be propagated.
        self.add_static_param("fc", 0.01)
        self.add_static_param("fr", 0.5)
        self.add_static_param("fp", 0.2)
        self.add_static_param("alpha", 0.001)

        # Add the population filter.
        self.add_filter(FAOSTATPopulationFilter)

        # Register data sources.
        self.register_data_source(BaseDTMMunger, FAOCountry, fao_map)
        self.register_data_source(BaseFBSMunger, FAOCountry, fao_map)
        self.register_data_source(BasePSDMunger, PSDCountry, psd_map)

        self.add_network_initializer(MarchandModelBuilder.shocked_initializer)
        self.add_network_initializer(MarchandModelBuilder.reserves_initializer)
        self.add_network_initializer(
            MarchandModelBuilder.production_initializer
        )
        self.add_network_initializer(
            MarchandModelBuilder.consumption_initializer
        )
        self.add_network_initializer(MarchandModelBuilder.supply_initializer)

    def build(self):
        """
        Configure, build and return a Marchand model.
        """
        recorders = [recorder_class() for recorder_class in self.recorder_classes]

        model = MarchandModel(self.static_params,
                              self.dynamic_params,
                              self.policy,
                              recorders,
                              self.politent_maps,
                              builder=self)

        political_rectifier = model.get_political_rectifier()
        # Add filters to the political rectifier.
        for filter_class in self.filter_classes:
            filter = filter_class(self.years)
            political_rectifier.add_filter(filter)

        for group in self.model_component_groups:
            political_rectifier.register_model_component_group(group)

        for politent in self.model_compound_politents:
            political_rectifier.register_model_compound_politent(politent)

        # Instantiate the data mungers.
        for MungerClass in self.munger_classes:
            munger = MungerClass(political_rectifier)
            munger.set_years(self.years)
            munger.munge()

        # Apply the network intializers.
        for initializer in self.network_initializers:
            initializer(model.network)

        return model

    @staticmethod
    def supply_initializer(network):
        for node, data in network.node.items():
            if not "production" in data:
                continue
            data["supply"] = data["production"]

        for u, v, data in network.edges(data=True):
            if "supply" in network.node[u]:
                network.node[u]["supply"] -= data["exports"]
            else:
                network.node[u]["supply"] = -data["exports"]
            if "supply" in network.node[v]:
                network.node[v]["supply"] += data["exports"]
            else:
                network.node[v]["supply"] = data["exports"]

    @staticmethod
    def shocked_initializer(network):
        for node, data in network.node.items():
            data["shocked"] = False

    @staticmethod
    def consumption_initializer(network):
        for node, data in network.node.items():
            if not "consumption" in data:
                msg = "{node} has no consumption data"
                print(msg.format(node=node))
                data["consumption"] = 0.0

    @staticmethod
    def reserves_initializer(network):
        for node, data in network.node.items():
            if not "reserves" in data:
                data["reserves"] = 0.0

    @staticmethod
    def production_initializer(network):
        for node, data in network.node.items():
            if not "production" in data:
                data["production"] = 0.0
