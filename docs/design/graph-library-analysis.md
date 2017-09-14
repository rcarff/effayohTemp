# Graph Library Analysis

This document analyzes graph libraries to inform a decision as to which to use
in the effayoh library.

## Purpose of the graph library

The basis of the global food trade network data structure that the effayoh
library will provide will be the graph data structure of whichever library is
selected.

### Requirements

- The graph data structure should be reasonably intuitive. Any large network
  library project should easily meet this requirement.
- Need to be able to change the network after it has been initially constructed.
- Need to be able to name and index nodes in the network.
- Need to be able to perform arbitrary, iterated traversals of the network.
- Need to be able to compute statistics on the network.
- Need to be able to render the network to an image.
- Need to be able to extend the network rendering facilities.

## Candidates

1. [NetworkX][NetworkX Home].
2. [iGraph][iGraph Home].
3. [graph-tool][graph-tool Home].

### NetworkX

License: BSD
Install: via pip
Drawing: Not compatible with Python 3.0 and above

NetworkX appeared to be very intuitive and easy to use on the graph
manipulation side. Unfortunately, the drawing facilities are not compatible
with Python 3.0 and above so I will only use NetworkX if iGraph and graph-tool
are completely inappropriate.

Haha! So funny story. iGraph and graph-tool are completely inappropriate.

### graph-tool

License: GPL
Install: From source

- graph-tool is the most [performant][graph-tool benchmark] of these three libraries.
- GraphViews are a nice feature.

#### Dependencies

1. Boost
2. Python 2.7
3. expat XML library
4. SciPy
5. Numpy
6. CGAL
7. Cairo

There are way too many dependencies. Installing this will be too complicated
for many potential users and I do not believe that the increased performance
and drawing capabilities are worth it.

### iGraph

Cannot seem to get this thing installed so... moving on.


[NetworkX Home]: https://networkx.github.io/
[iGraph Home]: http://igraph.org/python/
[graph-tool Home]: https://graph-tool.skewed.de/
[graph-tool benchmark]: https://graph-tool.skewed.de/performance
