# effayoh classes

This file documents the effayoh classes.

1. The MarchandModel class implements the Marchand model.
1. The MarchandModelBuilder class.
3. The `MarchandModelCommodity` class represents the commodity that forms the
   trade network at the heart of the Marchand model. The MarchandModelCommodity
   class synthesizes the information

# Marchand Model

The Marchand Model is a representation of the dynamics of the global food trade
system under shock.

## Functionality

1. Specify what commodity will from the basis of the network. The different
   types of commodity that can be specified are:

   - FAO Atomic: a commodity that corresponds to exactly 1 item from the FAO
     food balance sheet definition and standard. This can be specified by
     either the value of the item code or item fields in the food balance
     sheets definitions and standards.
   - MarchandModelCommodity subclass: a commodity that does not correspond to
     exactly 1 item from the FAO food balance sheet definition and standards.
     The user must define a subclass of MarchandModelCommodity that knows how
     to produce the information needed by the MarchandModel to operate.

2. Specify the time period that the model should consider. This can be done by:

   - Passing in a collection of integers.
   - Passing a slice object to the \_\_getitem\_\_ method.

3. Set model global parameters.
4. Set individual values on the underlying NetworkX graph.
5. Conveniently specify a distribution of reserves, production, consumption,
   imports and exports.
6. Build the model from a file.
7. Add dynamic global variables (price for example).
8. Allow for custom policy creation, for example creating a new policy that
   redistributes based on price, so the policy needs to be able to examine
   the state of individual nodes in the network as well as global variables.

   Perhaps it would be better to have a Builder class for the MarchandModel.

   The intent of the builder pattern in the big 4's seminal work is:

        Separate the construction of a complex object from its representation
        so that the same construction process can create different
        representations.

   This is exactly what the doctor ordered. The builder class should allow for
   the addition of global variables that are derived from system state and in
   turn affect system state.

   ```python
   from effayoh.common.marchandmodel import MarchandModelBuilder

   from custom_package import price, node_update_policy

   builder = MarchandModelBuilder()
   builder.setup_base_model()
   builder.define_dynamic_global_state_variable("price", price)

   builder.set_update_policy(update_policy)
   ```

   ```python
   def update_policy(epicenter, shock, network, globals_):
       delta_reserves = max(0, globals_.fr*node.reserves)
       if delta_reserves:
         node.reserves -= delta_reserves

       ...

       # Do something with price
       price = globals_.price
       # Stuff
   ```

# Marchand Model Builder

The Marchand Model Builder breaks construction of the Marchand Model down into
5 components:

1. Network initializers.
3. Static model parameters.
4. Dynamic model parameters.
5. Iteration policy.

## Network initializers

A `network initializer` is a function that takes as argument a NetworkX graph
and adds or modifies nodes and edges. The `country initializer` adds a node to
the network for each country and sets up countries that consist in the
aggregation of UN FAO codes. The Marchand model `base initializer` adds to each
country in the network its production, reserves, export edges, domestic
consumption, and net supply.

### Country initializer

In the simplest case where no FAO country code aggregations are declared, the
`country initializer` simply creates a new node in the graph for each FAO
country code. If an aggregation is defined, however, then the `country
initializer` creates an `aggregate country` object which is added to the
network in place of its constituent codes (ccs). The `aggregate country` object
maintains the information associated with each of its ccs and aggregates that
information when it is requested.

### Base initializer

The `base initializer` sets up the basic Marchand model, annotating each
country with its production, reserves, exort edges, domestic consumption and
net supply.

## Static model parameters

A `static model parameter` is an immutable value that is visible to every
component of the model.

## Dynamic model parameters

A `dynamic model parameter` is a function of network state that is recomputed
at the end of each simulation iteration and is visible to every component of
the model.

## Iteration policy

The `iteration policy` is a function that takes as argument the network and
applies some policy to the network. Iteration policies **must** be defined in
their own module.

## Functionality

1. Add network initializer.
2. Add static model parameter.
3. Add dynamic model parameter.
4. Set iteration policy.
5. Add country codes for aggregation.

For the price you need to add a global computed attribute.

Possible optional functionality:

1. add edge generator.

## Extending the base Marchand model

The `effayoh` library supports extending the base Marchand model in several
ways.

### Add parameters

It is possible to add parameters to the model. These parameters can be
static, as in the base model parameter 𝑓ᵣ, the fraction of actual reserves
that are available to absorb shocks. Parameters can also be dynamic, as in a
possible commodity price parameter that is a function of network state.

#### Static parameters

A static parameter can be added to the model by invoking the `add_static_param`
method of a `MarchandModelBuilder` instance. `add_static_param` takes the name
of the additional static parameter and its value as the formal parameters
`name` and `val`. The value of the parameter is made accessible through its
name in the namespace of the `update_policy` method. Thus after adding a new
static parameter, `SUR_threshold` to represent the stocks-to-use ratio
threshold for imposing trade restrictions, by:

```python
# builder is an instance of MarchandModelBuilder
builder.add_static_param("SUR_threshold", 0.15)
```

The new static parameter can simply be accessed by its name in the body of the
`update_policy` function passed to the MarchandModelBuilder instance's
`set_update_policy' method as in:

```python
# Custom policy for updating the network.
def update_policy(epicenter, shock, network):
    # Foo
    # ...

    if (country.stocks/country.use) < SUR_threshold:
        # Catastrophe!
        pass

    # Bar
    # ...

builder.set_update_policy(update_policy)
```

#### Dynamic parameters

A dynamic parameter is a parameter whose value is a function of network state.
This can be useful for adding a parameter for price to the model. The value of
price can then vary as the production shock propagates through the global trade
network. A dynamic parameter is added to the Marchand model by calling the
`add_dynamic_param` method of a `MarchandModelBuilder` instance passing the
name of the parameter and a function which takes as argument a `MarchandModel`
instance and returns the value of the parameter determined by the state of the
`MarchandModel` instance.

# FAO Data Sheet Requirements

The Marchand model requires information from the detailed trade matrix data
sheet and the food balance data sheet.

1. Trade volumes for the atomic or aggregate item under consideration derived
   from the detailed trade matrix.
2. Production, reserves and consumption from the food balance sheet.
