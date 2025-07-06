
from cluster.cluster_manager import ClusterManager
from cluster.cluster_leader_election import LeaderElection

import json

class ConfManager:
    def __init__(self, file: str, cluster: ClusterManager, leaderManager: LeaderElection):
        self.path = file
        self.group_m = cluster
        self.leaderManager = leaderManager
        self.config = None
    
    def deserialize_conf_file(self): 
        with open("conf.json") as f:
            self.config = json.load(f)
    
    def fill_cluster(self):
        group_conf = self.config["process_group"]
        
        for node_conf in group_conf:
            addr = node_conf['addr']
            port = node_conf['port']
            rank = node_conf['rank']

            self.group_m.add_node(addr, port)
            self.leaderManager.add_node(addr, port, rank)