import math
import re


class Graph:
    """
    it's the base class of Graph object, containing two class as component, Vertex and Edge
    The structure of graph is based on Adjacency Map Structure.
    it also contains some fundamental methods
    """
    class Vertex:
        """
        _element: the name of vertex
        _visited: the status of vertex, not used in this case
        """
        __slots__ = '_element', '_visited'

        def __init__(self, x):
            self._element = x
            self._visited = False

        def element(self):
            return self._element

        def is_visit(self):
            return self._visited

        def get_visited(self):
            self._visited = True

        def __hash__(self):
            return hash(id(self))

    class Edge:
        __slots__ = '_origin', '_destination'

        def __init__(self, u, v):
            """
            :param u: the origin vertex of edge
            :param v: the end vertex of edge
            """
            self._origin = u
            self._destination = v

        def endpoints(self):
            return self._origin, self._destination

        def opposite(self, v):
            return self._destination if v is self._origin else self._origin

        def __hash__(self):
            return hash((self._origin, self._destination))

    def __init__(self, directed=False):
        """
        _outgoing is a dictionary of dictionary. the value inside is a certain edge.
            the outer key is the origin vertex and the inside key is the destination of edge
        _incoming is just opposite to _outgoing.
        _vertex_dict will give you the vertex object when you have the name of vertex
        :param directed: if it's a directed graph
        """
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing
        self._vertex_dict = {}

    def check_reverse_edge(self, e):
        try:
            self._outgoing[e.endpoints()[1]][e.endpoints()[0]]
            return True
        except KeyError:
            return False

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()
        for secondaty_map in self._outgoing.values():
            result.update(secondaty_map.values())
        return result

    def get_edge(self, u, v):
        u_vertex = self._vertex_dict[u]
        v_vertex = self._vertex_dict[v]
        return self._outgoing[u_vertex].get(v_vertex)

    def degree(self, v, outgoing=True):
        v_vertex = self._vertex_dict[v]
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v_vertex])

    def incident_edges(self, v, outgoing=True):
        if isinstance(v, self.Vertex):
            v_vertex = v
        else:
            v_vertex = self._vertex_dict[v]
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v_vertex].values():
            yield edge

    def incident_vertex(self, v, outgoing=True):
        return self._outgoing[v].keys() if outgoing else self._incoming[v].keys()

    def insert_vertex(self, x=None):
        v = self.Vertex(x)
        self._vertex_dict[x] = v
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u_element, v_element, **kwargs):
        u_vertex = self._vertex_dict[u_element]
        v_vertex = self._vertex_dict[v_element]
        e = self.Edge(u_vertex, v_vertex)
        self._outgoing[u_vertex][v_vertex] = e
        self._incoming[v_vertex][u_vertex] = e


class BlastGraph(Graph):
    """
    it's the graph designed for our project to store the result of blast.
    it contains a BlastEdge class, which is customized version of base Edge class. the slots '_pident' and '_qcovs' are
    from blast stats and '_score' is defined as the multiply of '_pident' and '_qcovs'
    this class also has three methods for constructing the graph from a particular format of blast result.
    """
    class BlastEdge(Graph.Edge):
        __slots__ = '_origin', '_destination', '_pident', '_qcovs', '_evalue', '_score'

        def __init__(self, u, v, pident, qcovs, evalue=None):
            self._pident = pident
            self._qcovs = qcovs
            self._evalue = evalue
            if evalue:
                if float(evalue) == 0:
                    evalue = "1e-180"
                self._score = 1 - (math.log10(float(evalue)) + 180) / (1 + 180)
                #  1 / (1 + math.exp(0.1 * (math.log10(float(evalue)) + 30)))
            else:
                self._score = float(pident) * float(qcovs) / 10000

            super().__init__(u, v)

        def get_pident(self):
            return self._pident

        def get_qcovs(self):
            return self._qcovs

        def get_score(self):
            return self._score

    def insert_edge(self, u, v, **kwargs):
        cutoff = min(kwargs["thresholds"])
        del kwargs["thresholds"]
        u_vertex = self._vertex_dict[u]
        v_vertex = self._vertex_dict[v]
        e = self.BlastEdge(u_vertex, v_vertex, **kwargs)
        if e.get_score() < cutoff:
            return 0
        else:
            self._outgoing[u_vertex][v_vertex] = e
            self._incoming[v_vertex][u_vertex] = e
            return e

    def read_vertex(self, file):
        with open(file, "r") as vertex_file:
            for cnt, line in enumerate(vertex_file):
                self.insert_vertex(line.rstrip())

    def read_edge(self, file, qseqid, sseqid, pident, qcovs, evalue, thresholds):
        with open(file, "r") as edge_file:
            for cnt, line in enumerate(edge_file):
                words = re.split(r"\s+", line.rstrip())
                query_id = words[qseqid]
                subject_id = words[sseqid]

                if query_id != subject_id:
                    # if evalue is specified, then enter evalue mode
                    if evalue:
                        self.insert_edge(query_id, subject_id,
                                         pident=words[pident], qcovs=words[qcovs],
                                         evalue=words[evalue], thresholds=thresholds)
                    else:
                        self.insert_edge(query_id, subject_id,
                                         pident=words[pident], qcovs=words[qcovs],
                                         thresholds=thresholds)

        '''
        for u in self._outgoing.keys():
            for v in self._outgoing[u].keys():
                if self.self._outgoing[u][v].get_score() == 1:
                    try:
                        if self.self._outgoing[v][u].get_score() != 1:
                            del self.self._outgoing[v][u]
                    except KeyError:
                        continue
        '''
