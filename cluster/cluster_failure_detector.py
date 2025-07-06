
from cluster.cluster_manager import ClusterManager
from cluster.cluster_leader_election import LeaderElection
import requests
import asyncio

HTTP_PROTO = "http"
HTTP_TARGET_ENDPOINT = "/ping"

class FailureDetector:
    def __init__(self, clusterM: ClusterManager, leader_m: LeaderElection):
        self.group_m = clusterM
        self.leader_m = leader_m
        self.url = None
        self.data = None
        self.response = None
    
    async def broadcast_ping(self):
        while True:
            await asyncio.sleep(10)

            nodes, _ = self.group_m.get_cluster_group()

            for node in nodes:
                self.create_ping_request(node)
                try:
                    response = requests.post(self.url, json=self.data)
                except requests.Timeout as error:
                    # delete from cluster
                    tcpAddrOnly = node.split(":")
                    self.group_m.remove_node(tcpAddrOnly[0])
                    # perform a local leader election
                    # if is needed
                    addr, _, _ = self.leader_m.get_monarchical_leader()
                    if addr is tcpAddrOnly:
                        self.leader_m.local_leader_election(addr)
    

    def create_ping_request(self, addrAndPort):
        self.url = "{}://{}/{}".format(HTTP_PROTO, addrAndPort, HTTP_TARGET_ENDPOINT)
        self.data = {
            "ping": 1
        }

