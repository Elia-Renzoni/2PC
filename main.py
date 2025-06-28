from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("")
def execute_client_tx():
    pass

@app.post("")
def execute_leader_election():
    pass

@app.post("")
def execute_join_cluster(): 
    pass
