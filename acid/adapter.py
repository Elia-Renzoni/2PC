import sqlite3
from acid.two_phase_commit import DistributedCommit

class DataAdapter:
    def __init__(self, committer: DistributedCommit):
        self.conn = sqlite3.connect("file.db")
        self.cursor = self.conn.cursor()
        self.leader_forwarder = committer
        self.result = False

    def execute_local_tx(self, transaction: list[str]):
        try:
            for tx in transaction:
                self.cursor.execute(tx)
        except Exception as e:
            self.result = self.leader_forwarder.forward_result_to_leader("rollback")
            if self.result is False:
                self.conn.rollback()
        finally:
            self.result = self.leader_forwarder.forward_result_to_leader("commit")
            if self.result is True:
                self.conn.commit()
            else:
                self.conn.rollback()
