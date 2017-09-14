# Package level challenges

1. Disparate Data Source Integration
2. Political Reconciliation
3. Marchand Model customization

# Disparate data source integration

The base model alone requires integrating multiple sources of data.

## Solution

Data Mungers. The first step in processing the data. Mungers provide hooks for
processing individual values as well as grouped values.

# Political reconciliation

Different data sources have different political entities.

## Solution

Political Rectifier. An object that is responsible for mapping the data source
specific political entities to one or more political entities in the Marchand
model.

# Marchand model customization

We would like the Marchand model to be extensible and customizable.

## Solution

Construction of the Marchand model is managed by a builder class. The builder
class exposes hooks for implementing the desired extensions and customizations.
