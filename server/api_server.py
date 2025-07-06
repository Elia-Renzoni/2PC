from cluster.cluster_spreader import ClusterSpreader
from cluster.cluster_conf_manager import ClusterManager
from cluster.cluster_leader_election import LeaderElection


class ServerNode:
    def __init__(self, cluster_m: ClusterManager, broadcaster: ClusterSpreader, election_m: LeaderElection):
        self.cluster_m = cluster_m
        self.broadcaster = broadcaster
        self.leader_election_m = election_m

    def server_execute_transaction(self) -> bool:
        pass

    def server_execute_join_cluster(self, incoming_node_addr: str, incoming_node_listen_port: int):
        self.cluster_m.add_node(incoming_node_addr, incoming_node_listen_port)
        self.leader_election_m.add_node(incoming_node_addr, incoming_node_listen_port)

        joined = "{}:{}".format(incoming_node_addr, incoming_node_listen_port)
        self.broadcaster.broadcast_cluster_node(joined)
        

    def server_execute_pong(self):
        pass

