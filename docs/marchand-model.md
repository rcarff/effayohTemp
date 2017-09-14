# The MarchandModel class

The MarchandModel class is the Python representation of the Marchand model. In
the package we focus on those aspects of the model which are not related
directly to the implementation of the network because the NetworkX package
meets this need. The package implementation instead focuses on customizing
execution behavior. This is accomplished by providing mechanisms for: injecting
static and dynamic parameters, defining new execution behavior, and modifying
the base execution behavior.

In the most extreme case, arbitrary execution behavior can be defined by
passing a function `foo` which implements the desired behavior to the
`MarchandModel.set\_execution\_function` method.
`set\_execution\_function` takes a single argument, `model`, the MarchandModel
instance invoking the function. Calling `marchand\_model.execute()` in the
usual way will then execute `foo`.

More likely, however, the client will want to modify execution within the
structure of the model. For example, the client may wish to change how trade
flows are redistributed in response to a shock or change the value of a global
parameter. In this case, the model exposes hooks for making these
modifications.

## Marchand model execution structure

The outermost layer of the Marchand model execution structure is that the model
is executed. Modifying this layer of structure is the extreme case of setting
an arbitrary execution function.

After the execution layer is the iteration layer. Marchand model execution is
iterated until all shocks are absorbed or a maximum number of iterations is
executed. The iteration layer updates dynamic parameters, checks the
iteration continuation condition (icc) applies an update policy to affected
nodes and serves as the time step at which changes are made. The MarchandModel
provides hooks for adding dynamic parameters, setting the icc, setting the
update policy and adding recorders.

Underneath the iteration layer is the node update layer (nul). In the nul the
response of a node to the shock it receives on this iteration is computed. The
nul consists in two parts, trade flows adjustment and non-trade flows
adjustment.
