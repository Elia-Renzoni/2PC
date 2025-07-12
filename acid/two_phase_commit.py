import sqlite3
import requests
from cluster.cluster_leader_election import LeaderElection

HTTP_PROTO = "http"
HTTP_TARGET_ENDPOINT = "/results"
LEADER_COMMIT = "commit"
LEADER_ROLLBACK = "rollback"

class DistributedCommit:
    def __init__(self, leader_manager: LeaderElection):
        self.url = None
        self.data = None
        self.leader_decision = None
        self.response = None
        self.leader_m = leader_manager
        self.leader_addr = None

    def forward_result_to_leader(self, execution_result: str) -> bool:
        addr, port, _ = self.leader_m.get_monarchical_leader()
        self.leader_addr = "{}:{}".format(addr, port)
        self.make_forward_request(self.leader_addr, execution_result)

        self.response = requests.post(self.url, data=self.data)
        self.leader_decision = self.response.json()
        if self.leader_decision is LEADER_COMMIT:
            return True
        return False

    def make_forward_request(self, leader_addr: str, local_execution_result: str):
        self.url = "{}://{}{}".format(HTTP_PROTO,
                                      leader_addr,
                                      HTTP_TARGET_ENDPOINT)
        self.data = {
            "tx_result": local_execution_result
        }  

