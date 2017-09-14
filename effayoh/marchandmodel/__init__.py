"""
Provide the MarchandModel class.

"""

import networkx as nx

from effayoh.rectification.rectifier import PoliticalRectifier


class MarchandModelError(Exception): pass


class MarchandModel:

    """
    A model of global trade shock dynamics.

    The Marchand model is a model of the behavior of the global food
    trade network when a production shock occurs in one country.
    Rules are applied to propagate the shock and distribute the loss in
    production throughout the trade network.

    """

    def __init__(self,
                 static_params,
                 dynamic_params,
                 policy,
                 recorders,
                 politent_maps,
                 builder):
        self.network = nx.DiGraph()
        self.static_params = static_params
        self.dynamic_params = dynamic_params
        self.policy = policy
        self.recorders = recorders
        self.builder = builder
        self.political_rectifier = PoliticalRectifier(self.network,
                                                      politent_maps)
        self.max_iterations = 50
        self.affected_nodes = {}

    def get_political_rectifier(self):
        return self.political_rectifier

    def run(self, iterations=100):
        pass

    def step(self):
        pass

    def set_execution_function(self, func):
        pass

    def execute(self):
        """
        Execute the Marchand model.
        """
        print("Executing the model.")
        self.inject_params()
        self.apply_recorders()
        production = self.network.node[self.epicenter]["production"]
        shock = fp*production
        self.network.node[self.epicenter]["production"] -= shock
        self.affected_nodes[self.epicenter] = shock

        for i in range(1, self.max_iterations+1):
            print("Executing iteration {i}".format(i=i))
            self.update_params()
            self.affected_edges = {}
            self.iterate()
            self.apply_recorders()
            if not self.iterate_again():
                break

    def iterate(self):
        # Apply the node update policy to each of the affected nodes.
        # Changes to trade flows are recorded in the model instance
        # attribute affected_edges.
        for node, shock in self.affected_nodes.items():
            self.node_update(node, shock)
        self.affected_nodes = {}
        # Apply the updates to trade flows. Trade flows updates are
        # managed because a unilateral update within an iteration might
        # subsequently affect further updates in that same iteration.
        for (u, v), edge_data in self.affected_edges.items():
            adjustments = edge_data["adjustments"]
            if u in adjustments:  # v is shocked
                inc = adjustments[u]
                if v in self.affected_nodes:
                    self.affected_nodes[v] += abs(inc)
                else:
                    self.affected_nodes[v] = abs(inc)
            if v in adjustments:  # u is shocked
                inc = adjustments[v]
                if u in self.affected_nodes:
                    self.affected_nodes[u] += abs(inc)
                else:
                    self.affected_nodes[u] = abs(inc)

            edge_data["exports"] += sum(adjustments.values())

            if abs(edge_data["exports"]) < 0.001:
                edge_data.pop("exports")

            edge_data.pop("adjustments")

            if not edge_data:
                self.network.remove_edge(u, v)

    def node_update(self, node, shock):
        """
        Update node.
        """
        # Absorb some of the shock through reserves.
        dR = min(shock, fr*self.network.node[node]["reserves"])
        shock -= dR
        # Absorb some of the shock through consumption.
        max_dC = fc*self.network.node[node]["consumption"]
        dC = min(max_dC, shock)
        if dC > 0.0:
            self.network.node[node]["shocked"] = True
        shock -= dC

        if shock <= alpha*self.network.node[node]["supply"]:
            dC += shock
            self.network.node[node]["reserves"] -= dR
            self.network.node[node]["consumption"] -= dC
            self.network.node[node]["supply"] -= (dR + dC)
            return

        # Compute the adjustable trade volume of this node.
        Tvol = 0.0
        # Sum exports.
        export_links = self.network.out_edges_iter(nbunch=[node],
                                                   data=True)
        for u, v, data in export_links:
            Tvol += data["exports"]

        # Sum imports from countries that have not been shocked.
        import_links = self.network.in_edges_iter(nbunch=[node],
                                                  data=True)
        for u, v, data in import_links:
            if self.network.node[u]["shocked"]:
                continue
            Tvol += data["exports"]

        if Tvol == 0.0:  # This node is has no trade.
            dC += shock
            self.network.node[node]["reserves"] -= dR
            self.network.node[node]["consumption"] -= dC
            self.network.node[node]["supply"] -= (dR + dC)
            return

        Tshock = min(shock, Tvol)
        if shock > Tshock:
            shock -= Tshock
            dC += shock

        # Set the amount this node wants to adjust exports by.
        export_links = self.network.out_edges_iter(nbunch=[node], data=True)
        for u, v, data in export_links:
            self.affected_edges[(u, v)] = data
            adjustment = -(Tshock*data["exports"]/Tvol)
            if "adjustments" in data:
                data["adjustments"][u] = adjustment
            else:
                data["adjustments"] = {u: adjustment}

        # Set the amount this node wants to adjust imports by
        import_links = self.network.in_edges_iter(nbunch=[node], data=True)
        for u, v, data in import_links:
            if self.network.node[u]["shocked"]:
                continue
            self.affected_edges[(u, v)] = data
            adjustment = Tshock*data["exports"]/Tvol
            if "adjustments" in data:
                data["adjustments"][v] = adjustment
            else:
                data["adjustments"] = {v: adjustment}

        self.network.node[node]["reserves"] -= dR
        self.network.node[node]["consumption"] -= dC
        self.network.node[node]["supply"] -= (dR + dC)

    def set_node_update(self, func):
        raise NotImplementedError()

    def iterate_again(self):
        return bool(self.affected_nodes)

    def set_iterate_again_function(self, func):
        raise NotImplementedError()

    def inject_params(self):
        """
        Inject the static and dynamic parameters.

        Precondition
        ------------
        Model execution has just begun and no iteration has been
        executed and none of the parameter names is already defined in
        the global namespace.

        Postcondition
        -------------
        The parameters in self.static_params have been injected into
        the global namespace. The parameters in self.dynamic_params
        have been evaluated and injected into the global namespace.
        """
        globals_ = globals()

        for param, value in self.static_params.items():
            if param in globals_:
                msg = ("Static parameter {param} is already defined "
                       "you are clobbering a previous value.")
                print(msg.format(**locals()))

            globals_[param] = value

        for param, func in self.dynamic_params.items():
            if param in globals_:
                msg = ("Static parameter {param} is already defined "
                       "in module {__name__}")
                raise MarchandModelError(msg.format(**locals()))
            else:
                model = self
                globals_[param] = func(model)

    def update_params(self):
        """
        Update dynamic parameter values.
        """
        globals_ = globals()
        for param, func in self.dynamic_params.items():
            model = self
            globals_[param] = func(model)

    def apply_recorders(self):
        for recorder in self.recorders:
            recorder.record(self.network)

    def set_epicenter(self, country):
        self.epicenter = country
