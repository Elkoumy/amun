import sys

#replaced sys.maxint to inf
# --------------------------------------------------------------------------------- #
from math import inf


def _input(filename):
    prices = {}
    names = {}

    for line in open(filename).readlines():
        (name, src, dst, price) = line.rstrip().split()
        name = int(name.replace('M', ''))
        src = int(src.replace('C', ''))
        dst = int(dst.replace('C', ''))

        price = int(price)
        t = (src, dst)
        if t in prices and prices[t] <= price:
            continue
        prices[t] = price
        names[t] = name

    return prices, names


def _load(arcs, weights):
    g = {}
    for (src, dst) in arcs:
        if src in g:
            g[src][dst] = weights[(src, dst)]
        else:
            g[src] = {dst: weights[(src, dst)]}
    return g


def _reverse(graph):
    r = {}
    for src in graph:
        for (dst, c) in graph[src].items():
            if dst in r:
                r[dst][src] = c
            else:
                r[dst] = {src: c}
    return r


def _getCycle(n, g, visited=None, cycle=None):
    if visited is None:
        visited = set()
    if cycle is None:
        cycle = []
    visited.add(n)
    cycle += [n]
    if n not in g:
        return cycle
    for e in g[n]:
        if e not in visited:
            cycle = _getCycle(e, g, visited, cycle)
    return cycle


def _mergeCycles(cycle, G, RG, g, rg):
    allInEdges = []
    minInternal = None
    minInternalWeight = inf

    # find minimal internal edge weight
    for n in cycle:
        for e in RG[n]:
            if e in cycle:
                if minInternal is None or RG[n][e] < minInternalWeight:
                    minInternal = (n, e)
                    minInternalWeight = RG[n][e]
                    continue
            else:
                allInEdges.append((n, e))

                # find the incoming edge with minimum modified cost
    minExternal = None
    minModifiedWeight = 0
    for s, t in allInEdges:
        u, v = rg[s].popitem()
        rg[s][u] = v
        w = RG[s][t] - (v - minInternalWeight)
        if minExternal is None or minModifiedWeight > w:
            minExternal = (s, t)
            minModifiedWeight = w

    u, w = rg[minExternal[0]].popitem()
    rem = (minExternal[0], u)
    rg[minExternal[0]].clear()
    if minExternal[1] in rg:
        rg[minExternal[1]][minExternal[0]] = w
    else:
        rg[minExternal[1]] = {minExternal[0]: w}
    if rem[1] in g:
        if rem[0] in g[rem[1]]:
            del g[rem[1]][rem[0]]
    if minExternal[1] in g:
        g[minExternal[1]][minExternal[0]] = w
    else:
        g[minExternal[1]] = {minExternal[0]: w}


# --------------------------------------------------------------------------------- #

def mst(root, G):
    """ The Chu-Lui/Edmond's algorithm

    arguments:

    root - the root of the MST
    G - the graph in which the MST lies

    returns: a graph representation of the MST

    Graph representation is the same as the one found at:
    http://code.activestate.com/recipes/119466/

    Explanation is copied verbatim here:

    The input graph G is assumed to have the following
    representation: A vertex can be any object that can
    be used as an index into a dictionary.  G is a
    dictionary, indexed by vertices.  For any vertex v,
    G[v] is itself a dictionary, indexed by the neighbors
    of v.  For any edge v->w, G[v][w] is the length of
    the edge.  This is related to the representation in
    <http://www.python.org/doc/essays/graphs.html>
    where Guido van Rossum suggests representing graphs
    as dictionaries mapping vertices to lists of neighbors,
    however dictionaries of edges have many advantages
    over lists: they can store extra information (here,
    the lengths), they support fast existence tests,
    and they allow easy modification of the graph by edge
    insertion and removal.  Such modifications are not
    needed here but are important in other graph algorithms.
    Since dictionaries obey iterator protocol, a graph
    represented as described here could be handed without
    modification to an algorithm using Guido's representation.

    Of course, G and G[v] need not be Python dict objects;
    they can be any other object that obeys dict protocol,
    for instance a wrapper in which vertices are URLs
    and a call to G[v] loads the web page and finds its links.
    """

    RG = _reverse(G)
    if root in RG:
        RG[root] = {}
    g = {}
    for n in RG:
        if len(RG[n]) == 0:
            continue
        minimum = inf
        s, d = None, None
        for e in RG[n]:
            if RG[n][e] < minimum:
                minimum = RG[n][e]
                s, d = n, e
        if d in g:
            g[d][s] = RG[s][d]
        else:
            g[d] = {s: RG[s][d]}

    cycles = []
    visited = set()
    for n in g:
        if n not in visited:
            cycle = _getCycle(n, g, visited)
            cycles.append(cycle)

    rg = _reverse(g)
    for cycle in cycles:
        if root in cycle:
            continue
        _mergeCycles(cycle, G, RG, g, rg)

    return g


def transform_dfg(dfg):
    names={}
    result={}
    reverse_result={}
    idx=0
    for ix, key in enumerate(list(dfg.keys())):
        activity1, activity2=0,0
        if key[0] in names:
            activity1=names[key[0]]
        else:
            names[key[0]]=idx
            activity1=idx
            idx+=1

        if key[1] in names:
            activity2=names[key[1]]
        else:
            names[key[1]]=idx
            activity2=idx
            idx+=1

        result[(activity1,activity2)]=dfg[key]
        reverse_result[(activity2, activity1)] = dfg[key]

    return names,result, reverse_result



def get_optimal_branching(dfg, root, tail):
    names, result, reverse_result = transform_dfg(dfg)

    root = "11"
    tail = ""
    g_forward = _load(result, result)
    h_forward = mst(int(root), g_forward)

    g_backward = _load(reverse_result, reverse_result)
    h_backward = mst(int(tail), g_backward)

    result=merge_graphs(h_forward, h_backward, names)

    for s in h_forward:
        for t in h_forward[s]:
            print("%d-%d" % (s, t))

# --------------------------------------------------------------------------------- #

def find_key(dictionary, value):
    for name,idx in dictionary.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if idx == value:
            return name
    return -1
def merge_graphs(result, reverse_result,names):
    dfg={}
    renamed={}
    for s in result:
        for t in result[s]:
            dfg[(s,t)]=result[s][t]
    for s in reverse_result:
        for t in reverse_result[s]:
            if (t,s) not in list(dfg.keys()):
                dfg[(t,s)] =reverse_result[s][t]

    for key in list(dfg.keys()):
        renamed[(find_key(names,key[0]), find_key(names,key[1]))]= dfg[key]

    return renamed


if __name__ == "__main__":
    # try:
    #     filename = sys.argv[1]
    #     root = sys.argv[2]
    # except IndexError:
    #     sys.stderr.write('no input and/or root node specified\n')
    #     sys.stderr.write('usage: python edmonds.py <file> <root>\n')
    #     sys.exit(1)

    # prices, names = _input(filename)
    # prices, names = _input('edges')

    names={(1, 2): 1, (1, 5): 2, (1, 8): 3, (2, 3): 4, (3, 6): 5, (3, 4): 6, (4, 11): 7, (5, 2): 8, (5, 6): 9, (6, 8): 10,
     (6, 7): 11, (7, 3): 12, (7, 11): 13, (7, 10): 14, (8, 9): 15, (9, 10): 16, (9, 7): 17, (10, 11): 18, (10, 10): 18}
    prices={(1, 2): 5, (1, 5): 10, (1, 8): 5, (2, 3): 10, (3, 6): 25, (3, 4): 10, (4, 11): 5, (5, 2): 15, (5, 6): 20, (6, 8): 5, (6, 7): 30, (7, 3): 15, (7, 11): 15, (7, 10): 5, (8, 9): 10, (9, 10): 10, (9, 7): 5, (10, 11): 10, (10, 10): 40}
    root="1"
    g = _load(prices, prices)
    h1 = mst(int(root), g)
    for s in h1:
        for t in h1[s]:
            print("%d-%d" % (s, t))

    print("****** Reversed ********")
    """" reversed way"""
    # prices, names = _input('edges_reversed')
    dfg= {('Leucocytes', 'CRP'): 1778, ('ER Registration', 'ER Triage'): 971, ('ER Triage', 'ER Sepsis Triage'): 905, ('LacticAcid', 'Leucocytes'): 565, ('IV Liquid', 'IV Antibiotics'): 501, ('IV Antibiotics', 'Admission NC'): 489, ('Admission NC', 'Leucocytes'): 408, ('CRP', 'Release A'): 322, ('ER Sepsis Triage', 'IV Liquid'): 285, ('Release A', 'Return ER'): 276, ('IV Antibiotics', 'Admission IC'): 46, ('Admission IC', 'LacticAcid'): 41, ('CRP', 'Release B'): 19, ('CRP', 'Release C'): 13, ('CRP', 'Release D'): 12, ('CRP', 'Release E'): 3}

    names={(2, 1): 1, (5, 1): 2, (8, 1): 3, (3, 2): 4, (6, 3): 5, (4, 3): 6, (11, 4): 7, (2, 5): 8, (6, 5): 9, (8, 6): 10, (7, 6): 11, (3, 7): 12, (11, 7): 13, (10, 7): 14, (9, 8): 15, (10, 9): 16, (7, 9): 17, (11, 10): 18}
    names, result, reverse_result=transform_dfg(dfg)

    prices={(2, 1): 5, (5, 1): 10, (8, 1): 5, (3, 2): 10, (6, 3): 25, (4, 3): 10, (11, 4): 5, (2, 5): 15, (6, 5): 20, (8, 6): 5, (7, 6): 30, (3, 7): 15, (11, 7): 15, (10, 7): 5, (9, 8): 10, (10, 9): 10, (7, 9): 5, (11, 10): 10}
    root="11"
    g = _load(prices, prices)
    h2 = mst(int(root), g)

    merged = merge_graphs(h1,h2, names)
    for s in h2:
        for t in h2[s]:
            print("%d-%d" % (s, t))
