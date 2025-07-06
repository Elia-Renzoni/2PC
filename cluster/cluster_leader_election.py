
class LeaderElection:
    def __init__(self):
        self.ranking = list()
    
    def add_node(self, addr: str, port: int, rank: int):
        elem = ListItem(addr, port, rank)
        self.ranking.append(elem)
        

    def get_monarchical_leader(self) -> tuple[str, int, int]:
        self.ranking.sort(key=lambda item: item.get_rank())
        leader = self.ranking.pop(len(self.ranking) - 1)
        return leader.get_addr(), leader.get_port(), leader.get_rank()
    
    def local_leader_election(self, old_leader_addr: str):
        for node in self.ranking:
            if node.get_addr() is old_leader_addr:
                self.ranking.remove(node)
                break
        
        self.ranking.sort(key=lambda item: item.get_rank())


class ListItem:
    def __init__(self, addr: str, port: int, rank: int):
        self.nodeAddr = addr
        self.nodePort = port
        self.nodeRank = rank
    
    def get_addr(self) -> str:
        return self.nodeAddr

    def get_port(self) -> int:
        return self.nodePort
    
    def get_rank(self) -> int:
        return self.nodeRank