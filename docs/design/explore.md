# effayoh exploration document

effayoh meets two needs:

  1. effayoh provides easy-to-use data structures that represent FAO data. These
     data structures allow researchers to experiment with the FAO data without
     having to munge the data themselves.
  2. in the case that effayoh does not directly provide an appropriate data
     structure it provides constructs for building a suitable data structure.

## effayoh data structures

1. Trade Network.
2. Marchand model. The Marchand model internally makes use of a Trade Network.
3. Trade matrix.

### Marchand model

#### Sample Usage

Basic use case; pick a commodity trade network that is represented by exactly one
item code in the FAO detailed trade matrix and a time period, apply the shock and
render the result.

```python
from effayoh import MarchandModel

# We specify that the model should use the Wheat trade network.
# The slice syntax offers a nice way of choosing a time range. As in
# standard Python, we will take the left inclusive range of the bounds.
model = MarchandModel(commodity="Wheat")[1992:1997]
model.process_data()

# Run the simulation with a production shock of 0.20 applied to the
# United States.
model.shock(epicenter="United States", magnitude=0.20)

# Render the shock absorbed network to an image.
model.render(title="United-States-0.20-Wheat-Shock")
```

More advanced use cases collected in the following example; the ability
to customize the behavior of the model.

```python
from effayoh.common import MarchandModel
from effayoh.common.commodities import AggregateCerealsCalories

# Specify an aggregate item to use for this model's simulation.
model = MarchandModel(commodity=AggregateCerealsCalories())[1992:1997][2005:2010]
```

The behavior of an aggregate item is much more sophisticated than an atomic
item. The aggregate item will need to be passed all the filtered data and
then typically there will be some conversion necessary to combine each
constituent item's data.

## effayoh core constructs

1. Trade Matrix Item.
2. Country Food Reserves.
3. Country Food Production.

### Trade Matrix Item

The FAO detailed trade matrix gives information on trade of many different
items. Often we will want to treat a group of the FAO items as one. For this
purpose the effayoh library has the Trade Matrix Item construct which is
implemented in the `TradeMatrixItem` class.


## effayoh data processing phases

- Sheet analysis
- Sheet synthesis
- Data structure generation


### Sheet analysis phase

The sheet analysis phase consists in the following steps applied to each sheet
in isolation from all the other sheets:

  - Column filtering: whole columns may be omitted from processing in this
    step.
  - Row filtering: the possibly truncated rows are filtered for those
    containing field-specific values.
  - Reconciliation: inconsistencies in the data are possibly reconciled.

Column and row filtering do not have to be distinct algorithmically, in
implementation they may occur simultaneously for the sake of efficiency.
Logically, however, I find it useful to think of them as distinct.

### Sheet synthesis phase

In the sheet synthesis phase the sheet analyses are possibly combined. The
sheet synthesis phase consists in applying each declared Sheet Synthesizer to
the analyses.

Each Sheet Synthesizer uses one or possibly more of the sheet analyses to
produce an object directly consumable in the data structure generation phase.

### Data structure generation phase

In the data structure generation phase, the synthesized sheet information is
used to construct some data structure of interest such as the Marchand Model or
the trade matrix.
