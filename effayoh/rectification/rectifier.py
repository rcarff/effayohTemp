"""
Provides the PoliticalRectifier class.

"""

import logging

from effayoh.rectification.political_entities import FAOPolitEnt


class RectificationError(Exception): pass


class ModelPolitent: pass


class WholePoliticalEntity(ModelPolitent):
    """
    An effayoh political entity that is in itself a network node.

    """

    def __init__(self, effpent):
        self.name = effpent.name
        self.value = effpent.value


class CompoundPoliticalEntity(ModelPolitent):
    """
    An effayoh political entity that comprises two or more network
    nodes.

    The CompoundPoliticalEntity must be split into its comprising
    nodes and its data must be apportioned between them.

    """

    def __init__(self, effpent, constituent_names, distribution):
        self.effpent = effpent
        self.constituent_names = constituent_names
        self.distribution = distribution
        # The constituents dict attribute is populated when the
        # CompoundPoliticalEntity instance is registered with a
        # PoliticalRectifier.
        self.constituents = {}

    def scale(self, constituent_name, value):
        """
        Return value scaled by the portion assigned to constituent_name.
        """
        numerator = self.distribution[constituent_name]
        denominator = sum(self.distribution.values())
        return value*numerator / denominator

    def distribute_node_attr(self, name, value):
        """
        Distribute value among the nodes that comprise this political
        entity.
        """
        for cname, node in self.constituents.items():
            scale = self.scale(cname, value)
            node[name] = node.get(name, 0.0) + scale


class ComponentPoliticalEntityGroup(list, ModelPolitent):
    """
    A group of effayoh political entities that comprise a network node.
    """

    def __init__(self, name, elements):
        self.name = name
        super().__init__(elements)

    def __hash__(self):
        return hash(self.name)


class PoliticalRectifier:

    def __init__(self, network, politent_maps):
        """
        Parameters
        ----------
        network:
            The NetworkX graph instance that is the network of the
            Marchand Model.

        politent_maps:
            A dict that maps a data source political entity to its
            effpent mapping.

        component_political_entities:
            A dict that maps component effpents to their groups.

        """
        self.network = network
        self.politent_maps = politent_maps
        self.component_political_entities = {}
        self.compound_politents = []
        self.mpent_to_node = {}
        self.effpent_to_mpent = {}
        self.filters = []
        self.intragroup_resolvers = {}

    def get_effayoh_politent(self, data_politent):
        """
        Return the associated FAOPolitEnt of data_politent.
        """
        if isinstance(data_politent, FAOPolitEnt):
            return data_politent
        for politent_type in self.politent_maps:
            if type(data_politent) is politent_type:
                map_ = self.politent_maps[politent_type]
                break
        else:
            msg = "Received an undefined Political Entity Type."
            raise RectificationError(msg)
        return map_[data_politent]

    def get_model_politent(self, data_politent):
        """
        Return the ModelPolitent associated to data_politent.
        """
        effpent = self.get_effayoh_politent(data_politent)
        if effpent in self.component_political_entities:
            return self.component_political_entities[effpent]
        elif effpent in self.effpent_to_mpent:
            return self.effpent_to_mpent[effpent]
        else:
            mpent = WholePoliticalEntity(effpent)
            self.effpent_to_mpent[effpent] = mpent
            return mpent

    def rectify(self, politent):
        """
        Return the network node that represents this effpent.

        """
        if isinstance(politent, FAOPolitEnt):
            mpent = self.get_model_politent(politent)
        else:
            mpent = politent
        if not isinstance(mpent, ModelPolitent):
            raise RectificationError("Cannot rectify non ModelPolitent instance.")
        elif isinstance(mpent, CompoundPoliticalEntity):
            raise RectificationError("Cannot rectify CompoundPoliticalEntity")
        elif isinstance(mpent, ComponentPoliticalEntityGroup):
            return self.mpent_to_node[mpent]
        elif mpent in self.mpent_to_node:
            return self.mpent_to_node[mpent]
        else:
            name = mpent.name
            self.network.add_node(name)
            node = self.network.node[name]
            self.mpent_to_node[name] = node
            return self.mpent_to_node[name]

    def set_network_edge(self, data_source, data_dest, name, value):
        """
        Rectify and add the edge name with value to the network.
        """
        if self.filters_exclude(data_source) or\
           self.filters_exclude(data_dest):
                return

        mpent_source = self.get_model_politent(data_source)
        mpent_dest = self.get_model_politent(data_dest)

        if isinstance(mpent_source, CompoundPoliticalEntity) and\
           isinstance(mpent_dest, CompoundPoliticalEntity):
            self._set_network_edge_compound_to_compound(
                mpent_source,
                mpent_dest,
                name,
                value
            )
        elif isinstance(mpent_source, CompoundPoliticalEntity):
            self._set_network_edge_compound_source(
                mpent_source,
                mpent_dest,
                name,
                value
            )
        elif isinstance(mpent_dest, CompoundPoliticalEntity):
            self._set_network_edge_compound_dest(
                mpent_source,
                mpent_dest,
                name,
                value
            )
        elif isinstance(mpent_source, ComponentPoliticalEntityGroup) and\
             isinstance(mpent_dest, ComponentPoliticalEntityGroup):
            self._set_network_edge_component_component(
                mpent_source,
                mpent_dest,
                name,
                value
            )
        elif isinstance(mpent_source, ComponentPoliticalEntityGroup):
            self._set_network_edge_component_source(
                mpent_source,
                mpent_dest,
                name,
                value
            )
        elif isinstance(mpent_dest, ComponentPoliticalEntityGroup):
            self._set_network_edge_component_dest(
                mpent_source,
                mpent_dest,
                name,
                value
            )
        else:
            # In this case, both model political entities are Whole
            # political entites and the key of the corresponding network
            # node is given by their name attributes.
            kwargs = {name: value}
            self.network.add_edge(
                mpent_source.name,
                mpent_dest.name,
                **kwargs
            )

    def _set_network_edge_compound_to_compound(self, source, dest, name, value):
        """
        For each pair of constituents value must be scaled by the
        product of their distributions.
        """
        for sname in source.constituent_names:
            sscale = source.scale(sname, value)
            for dname in dest.constituent_names:
                dscale = dest.scale(dname, sscale)
                self.network.add_edge(sname, dname, name=dscale)

    def _set_network_edge_compound_source(self, source, dest, name, value):
        if dest in self.component_political_entities:
            dst = self.component_political_entities[dest]
        for sname in source.constituent_names:
            scaled_value = source.scale(sname, value)
            self.network.add_edge(sname, dst.name, name=scaled_value)

    def _set_network_edge_compound_dest(self, source, dest, attr_name, value):
        if source in self.component_political_entities:
            src = self.component_political_entities[source]
        for dname in dest.constituent_names:
            scaled_value = dest.scale(dname, value)
            self.network.add_edge(src.name, dname, attr_name=scaled_value)

    def set_network_node_attr(self, data_politent, name, value):
        """
        Add the distributed attribute name to the rectified
        data_politent node.

        Params:

            data_politent:
                The data-source defined political entity passed in by
                the data-source specific munger.

            name:
                The name of the attribute we wish to give to the node.

            value:
                The desired value of the attribute.
        """
        # Verify this data-defined political entity should be included
        # in the network.
        if self.filters_exclude(data_politent):
            return

        # Look up the corresponding model political entity.
        mpent = self.get_model_politent(data_politent)

        # Determine the type of the model political entity and route
        # program control to the corresponding method.
        if isinstance(mpent, WholePoliticalEntity):
            self._set_network_node_attr_whole(mpent, name, value)
        elif isinstance(mpent, ComponentPoliticalEntityGroup):
            self._set_network_node_attr_component(mpent, name, value)
        elif isinstance(mpent, CompoundPoliticalEntity):
            self._set_network_node_attr_compound(mpent, name, value)
        else:
            raise TypeError("politent must be a political entity")

    def _set_network_node_attr_whole(self, politent, name, value):
        node = self.rectify(politent)
        if name in node:
            raise RectificationError("node already has an attribute name")
        else:
            node[name] = value

    def _set_network_node_attr_component(self, politent, name, value):
        node = self.rectify(politent)
        if name in node:
            node[name] += value
        else:
            node[name] = value

    def _set_network_node_attr_compound(self, politent, name, value):
        politent.distribute_node_attr(name, value)

    def register_model_component_group(self, group):
        """
        Register the ComponentPoliticalEntityGroup group with this
        rectifier.

        Is this more complicated than saving this group in a collection
        like a list?

        What do we want to do with this in the future? We want to check
        if an effpent is in one of these component groups and if it is,
        fetch its component group.

        We also have to create a node for the component group.

        """
        if group.name in self.network:
            raise RectificationError("Duplicate component group names.")
        else:
            self.network.add_node(group.name)
            node = self.network.node[group.name]

        for component in group:

            if component in self.component_political_entities:
                msg = ("A ComponentPoliticalEntity instance is assigned "
                       "to more than one ComponentPoliticalEntityGroup.")
                raise RectificationError(msg)

            self.component_political_entities[component] = group
            self.mpent_to_node[group] = node

    def _set_network_edge_component_component(self, source, dest, name, value):
        """
        Set the attribute name to value on the edge (source, dest).

        This method handles the case when source and dest are instances
        of ComponentPoliticalEntityGroup. In this case we must be
        careful to check that source and dest are not in fact the same
        group.

        """
        if source is dest:
            self.resolve_intragroup_edge(source, name, value)
        else:
            self._set_network_edge_component_source(source, dest, name, value)

    def _set_network_edge_component_source(self, source, dest, name, value):
        """
        Set the attribute name to value on the edge (source, dest).

        This method handles the case when source is an instance of
        ComponentPoliticalEntityGroup and name is not. Since multiple
        data-defined entities will be contributing edges to the source,
        we must take care to accumulate their values.

        """
        if (source.name, dest.name) in self.network.edges():
            data = self.network[source.name][dest.name]
            if name in data:
                data[name] += value
            else:
                data[name] = value
        else:
            kwargs = {name: value}
            self.network.add_edge(
                source.name,
                dest.name,
                **kwargs
            )

    def _set_network_edge_component_dest(self, source, dest, name, value):
        """
        Set the attribute name to value on the edge (source, dest).

        This method handles the case when dest is an instance of
        ComponentPoliticalEntityGroup and source is not. We must be
        careful to accumulate the multiple possible edges from source
        to the various component political entities of the dest.

        """
        if (source.name, dest.name) in self.network.edges():
            data = self.network[source.name][dest.name]
            if name in data:
                data[name] += value
            else:
                data[name] = value
        else:
            kwargs = {name: value}
            self.network.add_edge(
                source.name,
                dest.name,
                **kwargs
            )

    def resolve_intragroup_edge(self, group, name, value):
        """
        Resolve an edge between components within a group.

        """
        if name in self.intragroup_resolvers:
            resolver = self.intragroup_resolvers[name]
            resolver(self.network, group, value)
        else:
            msg = (
                "The PoliticalRecitifer attempted to set an edge that "
                "is incident upon two political entities in the same "
                "ComponentPoliticalEntityGroup. No resolver has been "
                "registered to handle an intragroup edge for the "
                "attribute {name}. The model build process will "
                "proceed ignoring the information associated with the "
                "requested edge."
            )
            logging.warning(msg.format(name=name))

    def register_model_compound_politent(self, compound):
        """
        Register compound political entity with this rectifier.

        We want to check if an effpent is a compound political entity.

        We need to set up the nodes that this compound politent
        represents.

        The CompoundPoliticalEntity must declare the names of its
        constituent model political entities and define how to
        apportion its data among them.
        """

        for name in compound.constituent_names:

            if name in self.network:
                raise RectificationError("Duplicate constituent names")
            else:
                self.network.add_node(name)
                compound.constituents[name] = self.network[name]

        else:
            self.compound_politents.append(compound)
            self.effpent_to_mpent[compound.effpent] = compound

    def add_filter(self, filter):
        self.filters.append(filter)

    def filters_exclude(self, data_politent):
        """ Return True if data_politent is included in the model. """
        effpent = self.get_effayoh_politent(data_politent)
        return any(map(lambda f: f.excludes(effpent), self.filters))
