from cluster.cluster_conf_manager import ConfManager


class Server:
    def __init__(self, address: str, port: int, ):
        self.addr = address
        self.port = port

