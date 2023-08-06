import re
import operator
import time
import networkx
from .helper import BlastGraph

"""
Main module.

This scripts is to remove redundancy in a collections of sequences.
input:
    all sequences ids in the collections
    self blast output in format 6 (blast agains it self)
output:
    a tsv file, which group each sequence into a cluster
"""


# Graph Based Sequence Clustering Algorithm
class GBSCA(BlastGraph):
    """
    it's the main body of our Graph Based Sequence Clustering Algorithm(GBSCA). the class Cluster contain method of
    cluster constructor, checking if a node can be added to that cluster and checking if two clusters can be merged.
    the '_cluster_nodes' slots contain a dictionary of node and their outdegree. the '_path_distance' is the shortest
    path between any two node, if reachable, in the cluster.
    GBSCA class itself also has a method dispatch to guide the analysis into certain method. for the four dispatched
    method, they all consist of four parts: firstly, initial the tested nodes and clusters and do some simple test;
    Secondly, get the in_edges and out_edges between them. Thirdly, check it they can be added/merged. Fourth, update
    the cluster and node information in GBSCA.
    """
    class Cluster:
        __slots__ = "_cluster_nodes",  "_path_distance", "_cluster_representative", "_verbose"

        def __init__(self, u, v, e, verbose):
            self._cluster_nodes = {u: 1, v: 0}  # node as key and outdegree as value
            self._path_distance = {}
            self._cluster_representative = []

            self._path_distance[u] = {v: e.get_score()}
            self._path_distance[v] = {u: 0}
            self._verbose = verbose

        def set_verbose(self, verbose):
            self._verbose = verbose

        def get_cluster_nodes(self):
            return self._cluster_nodes

        def get_outdegree(self, u):
            return self._cluster_nodes[u]

        def get_path_distance(self, u):
            return self._path_distance[u]

        def get_shortest_distance(self, u, v=None, incoming=False):
            if incoming:
                return self._path_distance[v][u]
            else:
                return self._path_distance[u][v]

        def initialize_node_insertion(self, u):
            self._cluster_nodes[u] = 0
            self._path_distance[u] = {}

        def set_shortest_distance(self, u, v, dist):
            self._path_distance[u][v] = dist

        def check_threshold(self, dist_in, dist_out, cluster_threshold):
            '''
            if 0 < dist_in < cluster_threshold and 0 < dist_out < cluster_threshold:
                return 1
            else:
                return 0
            '''
            if 0 < dist_in < cluster_threshold and 0 < dist_out < cluster_threshold:
                return 1
            elif 0 < dist_in + dist_out < cluster_threshold:
                return 1
            else:
                return 0

        def get_reachable_nodes(self, u, incoming=False):
            """
            :param u: certain node in the cluster
            :param incoming: it's for direction. if you want to regard u as the destination of the path,
                                make "incoming" True.
            :return: all the node that can connect to u in certain direction
            """
            if incoming:
                return [v for v in self.get_cluster_nodes().keys() if u in self._path_distance[v].keys()]
            else:
                return self._path_distance[u].keys()

        def calculate_one_to_cluster_distance(self, v, bridge_dict, edges_check, incoming=False):
            """
            :param v: any vertex in this cluster
            :param bridge_dict: the collection of edges connect the nodes in this cluster and outside. its keys are the
                nodes in this clusters (so there is a possibility that v may appear in bridge_dict too). its values are
                the bridge edges.
            :param edges_check: threshold to check if there is any need to do a score multiply
            :param incoming: get the direction information. if the bridge edges are from outside into the clusters,
                incoming should be true. otherwise, it's false
            :return: the shortest distance from a bridges edge to node v inside the cluster.
            """
            if v in bridge_dict.keys():
                dist = bridge_dict[v].get_score()
            else:
                dist = max([bridge_dict[t].get_score() * self.get_shortest_distance(v, t, incoming)
                            for t in bridge_dict.keys()
                            if self.get_shortest_distance(v, t, incoming) > edges_check] + [0])
            return dist

        def check_and_insert_node(self, u, cluster_threshold, in_edges, out_edges, double_edges,
                                  in_edges_max_score, out_edges_max_score):
            """
            temp_in and temp_out will store all the shortest distance between u and any node in the clusters,
            if reachable. if temp_in and temp_out pass the cluster_threshold test, they can also be used to update
            "_path_distance" when u is added. At the same time, outdegree of any node in the clusters is also updated.
            :param u: the node to be checked
            :param cluster_threshold: threshold for the minimum _path_distance in cluster
            :param in_edges: all the edges from u to the clusters
            :param out_edges: all the edges from the clusters to u
            :param in_edges_max_score: threshold to check if there is any need to do a score multiply
            :param out_edges_max_score: threshold to check if there is any need to do a score multiply
            :return: if u is added to the cluster or not
            """
            in_edges_check = cluster_threshold / in_edges_max_score[0]
            out_edges_check = cluster_threshold / out_edges_max_score[0]

            temp_in_nodes = {e.endpoints()[1]: e for e in in_edges}
            temp_out_nodes = {e.endpoints()[0]: e for e in out_edges}
            temp_in = {}
            temp_out = {}

            if u.element() == "TRINITY_DN1896_c0_g3_i5" and \
                    "TRINITY_DN1896_c0_g3_i4" in [i.element() for i in self.get_cluster_nodes().keys()]:
                self._verbose = True
                print("IF it works +++++++++++++++++++++++++")

            for v in self.get_cluster_nodes().keys():
                dist_in = self.calculate_one_to_cluster_distance(
                    v, temp_in_nodes, in_edges_check, incoming=True
                )
                dist_out = self.calculate_one_to_cluster_distance(
                    v, temp_out_nodes, out_edges_check
                )
                if self.check_threshold(dist_in, dist_out, cluster_threshold):
                    if self._verbose:
                        print("first cluster is: " +
                              "; ".join([j.element() for j in self.get_cluster_nodes().keys()]) +
                              "\nThe failed insertion is from: " + u.element() + " to " + v.element() +
                              "\nforward distance is " + str(dist_in) + "; backward distance is " + str(dist_out))
                    # fail
                    return 0
                else:
                    temp_in.update({v: dist_in})
                    temp_out.update({v: dist_out})

            # success
            self.initialize_node_insertion(u)

            self._cluster_nodes[u] += len([1 for i in in_edges
                                           if i not in double_edges])
            for i in out_edges:
                if i not in double_edges:
                    self._cluster_nodes[i.endpoints()[0]] += 1

            for v, dist in temp_in.items():
                self._path_distance[u][v] = dist
            for v, dist in temp_out.items():
                self._path_distance[v][u] = dist
            return 1

        def check_and_merge_cluster(self, clu_v, cluster_threshold, in_edges, out_edges, double_edges,
                                    in_edges_max_score, out_edges_max_score):
            """
            the idea is similar to check_and_insert_node method. but expand the one-to-many relation to a many-to-many
            relation.
            the border nodes are the ones who are in both the endpoints of bridges edges and clu_v
            :param clu_v: the other cluster
            :param cluster_threshold: threshold for the minimum _path_distance in cluster
            :param in_edges: all the edges from clu_u to clu_v
            :param out_edges: all the edges from clu_v to clu_u
            :param in_edges_max_score: threshold to check if there is any need to do a score multiply
            :param out_edges_max_score: threshold to check if there is any need to do a score multiply
            :return: if two clusters are merged or not
            """

            in_edges_check = cluster_threshold / in_edges_max_score[0]
            out_edges_check = cluster_threshold / out_edges_max_score[0]

            border_nodes_set = set([e.endpoints()[0] for e in in_edges] +
                                   [e.endpoints()[1] for e in out_edges])

            temp_border_dist = {}
            for i in border_nodes_set:
                temp_in_nodes = {e.endpoints()[1]: e for e in in_edges if e.endpoints()[0] == i}
                temp_out_nodes = {e.endpoints()[0]: e for e in out_edges if e.endpoints()[1] == i}
                temp_in = {}
                temp_out = {}

                for v in clu_v.get_cluster_nodes().keys():
                    dist_in = clu_v.calculate_one_to_cluster_distance(
                        v, temp_in_nodes, in_edges_check, incoming=True
                    )
                    dist_out = clu_v.calculate_one_to_cluster_distance(
                        v, temp_out_nodes, out_edges_check
                    )
                    if self.check_threshold(dist_in, dist_out, cluster_threshold):
                        # fail
                        if self._verbose:
                            print("The failed insertion is from: " + i.element() + " to " + v.element())
                        return 0
                    else:
                        temp_in.update({(i, v): dist_in})
                        temp_out.update({(v, i): dist_out})

                temp_border_dist.update({i: [temp_in, temp_out]})

            temp_distance = {"in": {}, "out": {}}
            for i in self.get_cluster_nodes().keys():
                if i in border_nodes_set:
                    temp_distance["in"].update({
                        pair_key: dist for pair_key, dist in temp_border_dist[i][0].items()
                    })
                    temp_distance["out"].update({
                        pair_key: dist for pair_key, dist in temp_border_dist[i][1].items()
                    })
                else:
                    for v in clu_v.get_cluster_nodes().keys():
                        # only if the edge with score more than edge_check will get multiplication,
                        # which is the most time-consuming step.
                        dist_in = max([self.get_shortest_distance(i, border_node) *
                                       temp_border_dist[border_node][0][(border_node, v)]
                                       for border_node in border_nodes_set
                                       if self.get_shortest_distance(i, border_node) > in_edges_check] + [0])
                        dist_out = max([self.get_shortest_distance(border_node, i) *
                                        temp_border_dist[border_node][1][(v, border_node)]
                                        for border_node in border_nodes_set
                                        if self.get_shortest_distance(border_node, i) > out_edges_check] + [0])
                        if self.check_threshold(dist_in, dist_out, cluster_threshold):
                            if self._verbose:
                                print("The failed insertion is from: " + i.element() + " to " + v.element())
                            # fail
                            return 0
                        else:
                            temp_distance["in"].update({(i, v): dist_in})
                            temp_distance["out"].update({(v, i): dist_out})

            # success
            for i in clu_v.get_cluster_nodes().keys():
                self._cluster_nodes[i] = clu_v.get_outdegree(i)
                self._path_distance[i] = clu_v.get_path_distance(i)

            for pair_key in temp_distance["in"]:
                self._path_distance[pair_key[0]][pair_key[1]] = temp_distance["in"][pair_key]

            for pair_key in temp_distance["out"]:
                self._path_distance[pair_key[0]][pair_key[1]] = temp_distance["out"][pair_key]

            for i in out_edges:
                if i not in double_edges:
                    self._cluster_nodes[i.endpoints()[0]] += 1
            for i in in_edges:
                if i not in double_edges:
                    self._cluster_nodes[i.endpoints()[0]] += 1
            return 1

        def show_cluster_component(self, out_file=None):
            """
            This method will show you the nodes, edges information in a cluster
            :param out_file: if you want to push the output to a file, specify the file name here
            :return: None
            """
            nodes = self.get_cluster_nodes().keys()
            edges = []
            for i in nodes:
                edges.append("\n".join([i.element() + "\t" + j.element() + "\t" + str(self.get_shortest_distance(i, j))
                                        for j in self.get_reachable_nodes(i)]))

            msg = "nodes are\n" + "\n".join(map(operator.methodcaller('element'), nodes)) + \
                  "\nedges are\n" + "\n".join(edges)

            if out_file:
                out_fh = open(out_file, "w+")
                out_fh.write(msg)
            else:
                print(msg)

    def __init__(self, verbose=False, directed=True, out_degree=3):
        """
        constructor of GBSCA
        :param verbose: if you need the intermediate result
        :param directed: if it's a directed graph
        """
        super().__init__(directed)
        self._VisitedVertex = {}
        self._NotVisitedEdges = set()
        self._cluster_collection = set()
        self._verbose = verbose
        self._cluster_count = 0
        # out degree checking
        self._start_to_checking_outdegree = out_degree
        self._method_count = {"node_to_node": 0, "node_to_cluster": 0, "cluster_to_node": 0, "cluster_to_cluster": 0}
        self._clu_count = {"clu_u_nodes": 0, "clu_u_edges": 0, "clu_v_nodes": 0, "clu_v_edges": 0}

    def set_verbose(self, verbose):
        self._verbose = verbose

    def get_visited_vertex(self):
        # also include their clusters
        return self._VisitedVertex.keys()

    def get_cluster(self, u_element=None):
        if u_element:
            u_vertex = self._vertex_dict[u_element]
            try:
                return self._VisitedVertex[u_vertex]
            except KeyError:
                print("There is no such clusters")
        else:
            return self._cluster_collection

    def get_number_of_clusters(self):
        return self._cluster_count

    def visiting_vertex(self, u, clu):
        self._VisitedVertex[u] = clu
        if u not in clu.get_cluster_nodes().keys():
            raise ValueError("how come")

    def visiting_edge(self, e):
        if isinstance(e, list):
            for i in e:
                if i in self._NotVisitedEdges:
                    self._NotVisitedEdges.remove(i)
        else:
            if e in self._NotVisitedEdges:
                self._NotVisitedEdges.remove(e)

    def insert_edge(self, u, v, **kwargs):
        e = super().insert_edge(u, v, **kwargs)
        if e and e.get_score() > max(kwargs["thresholds"]):
            self._NotVisitedEdges.add(e)

    def remove_low_quality_edges(self, thresholds):
        cutoff = min(thresholds)
        deleted_edges = set()
        for i in self._NotVisitedEdges:
            if i.get_score() <= cutoff:
                deleted_edges.add(i)
                del self._outgoing[i.endpoints()[0]][i.endpoints()[1]]
                del self._incoming[i.endpoints()[1]][i.endpoints()[0]]
        self._NotVisitedEdges -= deleted_edges

    def get_bridge_edges(self, u, clu_v):
        if isinstance(u, self.Vertex):
            return self.get_in_and_out_edges(u, clu_v)

        if isinstance(u, self.Cluster):
            edge_info = {"in_edges": [], "out_edges": [], "double_edges": [],
                         "in_edges_max_score": [], "out_edges_max_score": []}
            for node in u.get_cluster_nodes().keys():
                res = self.get_in_and_out_edges(node, clu_v)
                for i in edge_info.keys():
                    edge_info[i].extend(res[i])
            return edge_info

    def get_in_and_out_edges(self, u, clu_v):
        in_edges = []
        in_edges_max_score = 0
        out_edges = []
        out_edges_max_score = 0
        for x, f in self._outgoing[u].items():
            if x in clu_v.get_cluster_nodes().keys():
                in_edges.append(f)
                in_edges_max_score = max(in_edges_max_score, f.get_score())
        for x, f in self._incoming[u].items():
            if x in clu_v.get_cluster_nodes().keys():
                out_edges.append(f)
                out_edges_max_score = max(out_edges_max_score, f.get_score())

        double_edges = []
        for i in in_edges:
            if self.check_reverse_edge(i):
                double_edges.append(i)
                double_edges.append(self._outgoing[i.endpoints()[1]][i.endpoints()[0]])
        return {"in_edges": in_edges, "out_edges": out_edges, "double_edges": double_edges,
                "in_edges_max_score": [in_edges_max_score if in_edges_max_score != 0 else 1],
                "out_edges_max_score": [out_edges_max_score if out_edges_max_score != 0 else 1]}

    def check_graph_integrity(self, clu):
        key_list = [j for j in self._VisitedVertex.keys() if self._VisitedVertex[j] == clu]
        for i in key_list:
            if i not in clu.get_cluster_nodes().keys():
                raise ValueError("there is a key missing")

        for i in clu.get_cluster_nodes().keys():
            if i not in key_list:
                raise ValueError("there is a key missing")

    def get_candidate_edges(self, edge_threshold):
        print("the size of not visited edges are " + str(len(self._NotVisitedEdges)))
        candidate_edges = [e for e in self._NotVisitedEdges if e.get_score() > edge_threshold]

        return candidate_edges

    def determine_cluster(self, e, cluster_threshold):
        u, v = e.endpoints()
        self.visiting_edge(e)
        method = self.dispatch_determine_method(u, v)
        self._method_count[method] += 1
        eval("self."+method+"(u, v, e, cluster_threshold)")

    def dispatch_determine_method(self, u, v):
        cluster_type = [u not in self.get_visited_vertex(), v not in self.get_visited_vertex()]
        if self._verbose:
            msg = [re.sub(r"False", "a cluster", re.sub(r"True", "a node", str(i)))
                   for i in cluster_type]
            print("\t".join(msg))

        if cluster_type == [True, True]:
            return "node_to_node"

        if cluster_type == [True, False]:
            return "node_to_cluster"

        if cluster_type == [False, True]:
            return "cluster_to_node"

        if cluster_type == [False, False]:
            return "cluster_to_cluster"

    def node_to_node(self, u, v, e, cluster_threshold):
        if e.get_score() > cluster_threshold:
            clu = self.Cluster(u, v, e, verbose=self._verbose)
            self._cluster_collection.add(clu)
            self._cluster_count += 1

            self.visiting_vertex(u, clu)
            self.visiting_vertex(v, clu)
        if self._verbose:
            print("successfully initialize a cluster with two seed nodes: " + u.element() + " and " + v.element())

    def node_to_cluster(self, u, v, e, cluster_threshold):
        clu = self._VisitedVertex[v]
        edge_information = self.get_bridge_edges(u, clu)

        if clu.check_and_insert_node(u, cluster_threshold, **edge_information):
            self.visiting_vertex(u, clu)
            self.visiting_edge(edge_information["in_edges"])
            self.visiting_edge(edge_information["out_edges"])
            if self._verbose:
                print("successfully insert the node " + v.element() + " into cluster")
        else:
            if self._verbose:
                print("Unsuccessfully insert the node " + v.element() + " into cluster")

    def cluster_to_node(self, u, v, e, cluster_threshold):
        clu = self._VisitedVertex[u]

        # when the cluster has more nodes than a check point,
        # then only if the the origin of bridge edge, which is in clu cluster,
        # has a outdegree equal to 0, we will process it further
        # the aim of outdegree check is to avoid the situation that two distinct transcripts
        # are falsely grouped together because there is one exons shared between them
        # if clu.get_outdegree(u) != 0 and \
        #        len(clu.get_cluster_nodes().keys()) > self._start_to_checking_outdegree:
        #    return 0

        edge_information = self.get_bridge_edges(v, clu)

        if clu.check_and_insert_node(v, cluster_threshold, **edge_information):
            self.visiting_vertex(v, clu)
            self.visiting_edge(edge_information["in_edges"])
            self.visiting_edge(edge_information["out_edges"])
            if self._verbose:
                print("successfully insert the node " + v.element() + " into cluster")
        else:
            if self._verbose:
                print("Unsuccessfully insert the node " + v.element() + " into cluster")

    def cluster_to_cluster(self, u, v, e, cluster_threshold):
        clu_u = self._VisitedVertex[u]
        clu_v = self._VisitedVertex[v]

        if clu_u == clu_v:
            return 0

        # when the cluster has more nodes than a check point,
        # then only if the the origin of bridge edge, which is in clu_v cluster,
        # has a outdegree equal to 0, we will consider it further
        # if clu_v.get_outdegree(v) != 0 and \
        #        len(clu_v.get_cluster_nodes().keys()) > self._start_to_checking_outdegree:
        #    return 0

        edge_information = self.get_bridge_edges(clu_u, clu_v)

        # self._clu_count = {"clu_u_nodes": 0, "clu_u_edges": 0, "clu_v_nodes": 0, "clu_v_edges": 0}
        # self._clu_count["clu_u_nodes"] += len(clu_u.get_cluster_nodes().keys())
        # self._clu_count["clu_u_edges"] += sum(
        #     [len(clu_u._path_distance[i].keys()) for i in clu_u._path_distance.keys()]
        # )
        #
        # self._clu_count["clu_v_nodes"] += len(clu_v.get_cluster_nodes().keys())
        # self._clu_count["clu_v_edges"] += sum(
        #     [len(clu_v._path_distance[i].keys()) for i in clu_v._path_distance.keys()]
        # )
        #
        # if self._clu_count["clu_v_edges"] > 1000000:
        #     print("There is an important cluster: " + str(self._clu_count["clu_v_edges"]))
        #     with open(str(self._clu_count["clu_v_edges"]) + "_high_clu.obj", 'wb') as clusters_file:
        #         pickle.dump(clu_v, clusters_file)

        if clu_u.check_and_merge_cluster(clu_v, cluster_threshold, **edge_information):
            self.visiting_edge(edge_information["in_edges"])
            self.visiting_edge(edge_information["out_edges"])
            for i in clu_v.get_cluster_nodes().keys():
                self._VisitedVertex[i] = clu_u
            self._cluster_collection.remove(clu_v)
            self._cluster_count -= 1

            if self._verbose:
                print("successfully merge two clusters")
        else:
            if self._verbose:
                print("Unsuccessfully merge two clusters")

    def train_part(self, initial_edge_threshold, final_edge_threshold, cluster_threshold):
        edge_threshold = initial_edge_threshold
        lower_amp = (initial_edge_threshold - final_edge_threshold) / 100
        while edge_threshold > final_edge_threshold:
            time_tmp = time.time()
            candidate_edges = list(self.get_candidate_edges(edge_threshold))
            # sort the candidate edges by their scores
            candidate_edges.sort(key=operator.methodcaller('get_score'), reverse=True)
            print("first part takes " + str(time.time() - time_tmp))
            time_tmp = time.time()
            while candidate_edges:
                # process the edges one by one
                test_edge = candidate_edges.pop(0)
                self.determine_cluster(test_edge, cluster_threshold)
                # if len(candidate_edges) % 500 == 0:
                #     print("every part takes " + str(time.time() - time_tmp))
                #     time_tmp = time.time()
                #     print(self._clu_count)
                #     self._clu_count = {"clu_u_nodes": 0, "clu_u_edges": 0, "clu_v_nodes": 0, "clu_v_edges": 0}
                #     print(self._method_count)
                #     print("\n")

            print("second part takes " + str(time.time() - time_tmp))
            edge_threshold = edge_threshold - lower_amp
            print("number of clusters is " + str(self.get_number_of_clusters()) + "\nedge_threshold = " + str(edge_threshold))
            print(time.ctime())
            print()

    def print_cluster_report(self, out_base=None):
        cnt = 0
        clu_nodes = []
        output_cluster = open(out_base + "_clusters.txt", "w")
        for clu in self._cluster_collection:
            cnt += 1
            clu_nodes.append(len(clu.get_cluster_nodes().keys()))

            output_cluster.write("\n".join([str(i) + "\tCluster_" + str(cnt)
                                            for i in
                                            map(operator.methodcaller('element'), clu.get_cluster_nodes().keys())])
                                 + "\n")

        print(len(self._outgoing.keys()))
        for single_seq in self._outgoing.keys():
            if single_seq not in self.get_visited_vertex():
                cnt += 1
                output_cluster.write(single_seq.element() + "\tCluster_" + str(cnt) + "\n")

        print("there are " + str(cnt) + " clusters.\nTheir number of nodes are "
              + ", ".join([str(i) for i in clu_nodes]) +
              "\n" + str(sum(clu_nodes)) + " nodes are involved in the clusters")

    def check_with_known_isoforms(self):
        luci_gene_id = "TRINITY_DN8457_c0_g1"
        ribo_gene_id = "TRINITY_DN3636_c0_g1"
        check_luci = set()
        check_ribo = set()
        for clu in self._cluster_collection:
            for i in map(operator.methodcaller('element'), clu.get_cluster_nodes().keys()):
                if re.match(luci_gene_id, i):
                    check_luci.add(clu)
                if re.match(ribo_gene_id, i):
                    check_ribo.add(clu)

        print("the luciferases are in " + str(len(check_luci)) + " different clusters")
        print("the ribosomals are in " + str(len(check_ribo)) + " different clusters")
        return check_luci, check_ribo

    def plot_a_cluster(self, clu):
        nodes_set = clu.get_cluster_nodes().keys()
        G = networkx.DiGraph()
        G.add_nodes_from(nodes_set)

        edges_set = []
        for i in nodes_set:
            edges_set.extend([e.endpoints() for e in self.incident_edges(i) if e.endpoints()[1] in nodes_set])
        G.add_edges_from(edges_set)
        networkx.draw_circular(G, labels={i: re.sub(r"TRINITY_DN", "", i.element()) for i in nodes_set})

    def plot_adjacent(self, node):
        node_obj = self._vertex_dict[node]

        G = networkx.DiGraph()
        incident_node_set = set()
        for i in self.incident_vertex(node_obj, outgoing=True):
            incident_node_set.add(i)

        for i in self.incident_vertex(node_obj, outgoing=False):
            incident_node_set.add(i)

        G.add_nodes_from(incident_node_set)

        edges_col = {}
        for e in self._outgoing[node_obj].values():
            G.add_edge(e.endpoints()[0], e.endpoints()[1], weights=round(e.get_score(), 3), color='r')
            edges_col[e] = "r"

        for e in self._incoming[node_obj].values():
            G.add_edge(e.endpoints()[0], e.endpoints()[1], weights=round(e.get_score(), 3), color='b')
            edges_col[e] = "b"

        pos = networkx.circular_layout(G)  # positions for all nodes

        # nodes
        networkx.draw_networkx_nodes(G, pos, node_size=200)

        # edges
        networkx.draw_networkx_edges(G, pos, width=2)
        networkx.draw_networkx_edge_labels(G, pos, edge_labels=networkx.get_edge_attributes(G, 'weights'))

        # labels
        networkx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif',
                                      labels={i: re.sub(r"TRINITY_DN", "", i.element()) for i in incident_node_set})
