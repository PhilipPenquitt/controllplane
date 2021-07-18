from enum import Enum
from typing import Counter, Optional
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

people = {
    "ise": "ise",
    "katja": "katja"
}

clients = []


class Modelname(str, Enum):
    alex = "alex"
    benito = "benito"
    robin = "robin"


@app.get("/echo/{input}")
def echo(input: int):
    return {"Nachricht": input}


@app.get("/")
def simpleanswer():
    return {"message": "Hello World"}


@app.get("/choose/{model_name}")
async def get_model(model_name: Modelname):
    if model_name == Modelname.alex:
        return Modelname.alex
    if model_name == Modelname.benito:
        return Modelname.benito
    if model_name.value == "robin":
        return "alex oder Benito"
    else:
        return "Das war falsch"


@app.get("/weiber/{weibername}")
async def get_weibernamen(weibername: str):
    if weibername in people:
        return {"Weib": weibername, "Status": "bumsbar!"}
    else:
        return "falsch geraten"


@app.get("/header", response_class=PlainTextResponse)
def header(request: Request):
    client_port = request.client.port
    client_ip = request.client.host
    client = client_ip + ":" + str(client_port)
    clients.append(client)
    individuell = Counter(clients)
    return f"Host: {client} Count: {individuell[client]}"
