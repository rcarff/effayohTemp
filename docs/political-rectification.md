# Political Rectification

Political rectification refers to the process of adjusting the political
entities in the raw data to match the nodes in the Marchand model network.

Political rectification is made up of two stages. Data-source political entity
rectification and effayoh political entity rectification. The former declares
the mapping of data-source defined political entities to the effayoh political
entities thereby matching all the data-source defined political entities to
each other from their data sources. The latter manages the merges and splits of
political entites from the data to the time period under consideration.

Fortunately we don't have to solve the much more difficult problem of tracing
the lineage and evolution of political entities over the entire time period of
the data. For the model runs, the experiment designers will have to fix a time
period which will typically be much smaller than the data time period. Within
that time period, for each effayoh defined political entity (PE), the
designer has to decide the PE's **type** which can be one of three things: the
PE is a **whole** entity, the PE is a **component** of an compound political
entity, or the PE is a **compound** political entity that is to be split up in
some way for the model.


# Data-Source Political Entity Reconciliation

**effayoh** defines its own set of constants for political entities. Each
data-source must provide a mapping form its own political entities to the
**effayoh** political entities.

The political rectifier uses the mappings from data source defined political
entities to **effayoh** political entities in order to create the final
network.


# effayoh Political Entity Rectification

Rectification of the effayoh political entities is a matter of resolving the
type of the political entity to determine which node or nodes the entity is
mapped to in the current experiment.

## Type Resolution

On any instantiation of the Marchand model every effayoh political entity will
have a type corresponding to its relationship to one of the nodes in the model
network.

There are three possible relationships between effayoh political entities and
nodes: **whole**, **component**, and **compound**.

If the effayoh political entity is one of the nodes in the network, then has
type **whole**.

If the effayoh political entity is one of two or more effayoh political
entities which comprise a node, then it has type **component**.

If the effayoh political entity comprises two or more nodes, then it has type
**compound**.


# Political Rectifier

The political rectifier uses the mapping of data-source defined political
entities to effayoh political entities to integrate data across different
sources. The integrated data is apportioned to nodes in the network by
resolving the type of the effayoh political entity.

# Rectification instances

## East Germany

East Germany appears as "Germany Nl" in the FAOSTAT standards and definitions.
The USDA database refers to East Germany as "German Democratic Republic."

## West Germany

West Germany is referenced as "Germany Fr by FAOSTAT and "Germany, Federal
Republic of" by the USDA.

The Wikipedia article on [UN
M49](https://en.wikipedia.org/wiki/UN_M.49#cite_note-Germany-18) codes was used
to resolve the FAOSTAT terms.

# Excluded USDA Countries

- GN: Gilbert and Ellice Islands. Population.
- IO: British Ind. Ocean Territory. Population.
- MB: Martinique. Population.
- MQ: Midway Islands. Population.
- MT: Malta and Gozp. Population.
- MV: Maldive Islands. Population.
- NA: Netherlands Antilles. Population.
- NC: New Caledonia. Population.
- NH: Vanuatu/New Hebrides. Population.
- NQ: Trust Territory of the Pacific. Population.
- NR: Nauru. Population.
- SB: St. Pierre and Miquelon. Population.
- SC: St. Kitts and Nevis. Population.
- SE: Seychelles. Population.
- SH: St. Helena (Br W Afr). Population.
- ST: St. Lucia. Population.
- T3: Africa, NEC. Unable to identify.
- T8: Fernando Po. Now known as Bioko, population.
- TK: Turks and Caicos Islands. Population.
- TN: Tonga. Population.
- TP: Sao Tome and Principe. Population.
- VC: St. Vincent and the Grendines. Population.
- VI: British Virgin Islands. Population.
- VO: Virgin Islands of the U.S.. Population.
- W7: British West Pacific Islands. Unable to identify.
- WE: West Bank. No corresponding FAOSTAT entity.
- WQ: Wake Island. Population.
- WS: Western Samoa. Population.
- X3: Canton and Enderbury Islands. Population.
- X6: FrenchInd. Ocean Territory. Unable to identify.
- X8: Southern Asia NEC. Unable to Identify.
- Y1: Leeward-Windward Islands. Population.
- Y2: French West Indies. Refers to several countries that do not break the
  Population threshold.
- Y3: Azores. Population.
- Y7: Canary Islands. No corresponding FAOSTAT entity.
- Y9: Madeira Islands. Population.
- Z7: Other Pacific Islands, NEC. Unable to identify.
