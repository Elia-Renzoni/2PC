from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/tx")
def execute_client_tx():
    pass

@app.post("/election")
def execute_leader_election():
    pass

@app.post("/newnode")
def execute_join_cluster(): 
    pass

@app.post("/hearbeat")
def execute_heartbeat():
    pass