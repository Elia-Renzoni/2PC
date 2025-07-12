import sqlite3

class DataAdapter:
    def __init__(self):
        self.conn = sqlite3.connect("file.db")
        self.cursor = self.conn.cursor()

    def execute_local_tx(self, transaction: list[str]):
        try:
            for tx in transaction:
                self.cursor.execute(tx)
        except Exception as e:
            self.conn.rollback()
            # TODO -> contact the leader
        finally:
            # TODO -> contact the leader in case of commit
            pass
