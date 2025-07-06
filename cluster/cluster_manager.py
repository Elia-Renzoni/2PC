import ipaddress as controller

MIN_PORT = 0x0
MAX_PORT = 0xFFFF

class ClusterManager:
    def __init__(self):
        self.group = dict()
        self.bindedConns = list()
    
    def add_node(self, nodeAddres: str, nodeListePort: int) -> bool:
        try:
            controller.ip_address(nodeAddres)
            if nodeListePort < MIN_PORT or nodeListePort > MAX_PORT:
                raise Exception("Invalid TCP Listen Port")
            self.group[nodeAddres] = nodeListePort
        except ValueError:
            return False
        return True
    
    def remove_node(self, nodeAddress: str):
        self.group.pop(nodeAddress)
    
    def get_cluster_group(self) -> list[str]:
        for nodeTCPAddr, nodeTCPPort in self.group.items():
            self.bindedConns.append(self.join_addr_and_port(nodeTCPAddr, nodeTCPPort))
        
        return self.bindedConns


    
    def join_addr_and_port(self, tcpAddress: str, tcpPort: int) -> str:
        return "{}:{}".format(tcpAddress, tcpPort)
