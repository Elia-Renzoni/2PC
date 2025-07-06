import requests
from cluster.cluster_manager import ClusterManager

HTTP_PROTO = "http"
HTTP_TARGET_ENDPOINT = "/newnode"

class ClusterSpreader:
    def __init__(self, cluster: ClusterManager):
        self.cluster_nodes = cluster
        self.url = None
        self.data = None
        self.response = None

    def broadcast_cluster_node(self, newNode: str):
        nodes, length = self.cluster_nodes.get_cluster_group()
        if length < 2:
            return

        for node in nodes:
            if node == newNode:
                continue

            self.create_post_call(newNode)
            try:
                self.response = requests.post(self.url, json=self.data)
            except requests.Timeout as error:
                # fault 
                tpcAddrOnly = node.split(":")
                self.cluster_nodes.remove_node(tpcAddrOnly[0])
    
    def join_call_ack(self) -> str:
        pass

    def create_post_call(self, addrAndPort: str):
        self.url = "{}://{}/{}".format(HTTP_PROTO, addrAndPort, HTTP_TARGET_ENDPOINT)
        self.data = {
            "freshman": addrAndPort
        }