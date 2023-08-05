# Graafilohi

Graafilohi is a library intended to create executable graphs and to provide some basic functions such as determining
the execution order of the nodes. The name "Graafilohi" is a play on the Finnish words "graafi" (meaning "graph") and
"graavilohi" (I guess this is something like "gravlax" or sorts; Dammit man, I'm a programmer, not a chef).

The library uses at least `networkx` and `matplotlib` as a basis, first of which provides most of the features itself
allowing all the graph operations it contains to be used on the graph. This library implements the execution etc. higher
level features.

The intended use is to create tools using this where the problem is related to dependencies and possible to visualize
as a graph.