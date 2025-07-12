from fastapi import FastAPI, Request, Response
from cluster.cluster_conf_manager import ConfManager
from cluster.cluster_manager import ClusterManager
from cluster.cluster_failure_detector import FailureDetector
from cluster.cluster_leader_election import LeaderElection
from cluster.cluster_spreader import ClusterSpreader
from server.api_server import ServerNode
import asyncio
import json

HOST = "127.0.0.1"
PORT = 6567

app = FastAPI()

@app.post("/tx")
def execute_client_tx(req: Request, res: Response):
    addr, port, _ = leader_election_m.get_monarchical_leader()
    if addr is HOST and port is PORT:
        pass

    server_m.server_execute_transaction()

'''
json body:
-----------
{
   "addr": "<IPv4>"
   "port": "<Listen Port>"
}
-----------
'''
@app.post("/newnode")
async def execute_join_cluster(req: Request, res: Response): 
    body_content = await req.json()
    address = body_content['addr']
    port = body_content['port']

    server_m.server_execute_join_cluster(address, port)
    data = {"message": "Join Message Arrived"}
    json_data = json.dumps(data)  # serializzo dict in JSON string
    res.headers["Content-Type"] = "application/json"
    return Response(content=json_data)

@app.post("/ping")
def execute_pong(req: Request, res: Response):
    pong_data = {"message": "pong"}
    json_pong_data = json.dumps(pong_data)
    res.headers["Content-Type"] = "application/json"
    return Response(content=json_pong_data)

@app.post("/reults")
def execute_result_comparison(req: Request, res: Response):
    pass

if __name__ == "__main__":
    cluster_m = ClusterManager()
    leader_election_m = LeaderElection()
    conf_m = ConfManager("conf.json", cluster_m, leader_election_m)
    failure_detector_m = FailureDetector(cluster_m, leader_election_m)
    broadcaster = ClusterSpreader(cluster_m)
    server_m = ServerNode(cluster_m, broadcaster)

    conf_m.deserialize_conf_file()
    conf_m.fill_cluster()
    asyncio.run(failure_detector_m.broadcast_ping())

    
    