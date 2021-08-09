from enum import Enum
from typing import Counter, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import Request
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "john@doe",
        "full_name": "John Doe",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    }
}

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

def fake_dekode_token(token):
    return User(
        username=token + "fakedecoded", email="johndoe@gmail.com"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_dekode_token(token)
    return user


@app.get("/users/me")
async def read_uses_me(current_user: User = Depends(get_current_user)):
    return get_current_user

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
        return "kenn ich nicht, vielleicht bumsbar"


@app.get("/header", response_class=PlainTextResponse)
def header(request: Request):
    client_port = request.client.port
    client_ip = request.client.host
    client = client_ip + ":" + str(client_port)
    clients.append(client)
    individuell = Counter(clients)
    return f"Host: {client} Count: {individuell[client]}"


@app.get("/filebackup", response_class=PlainTextResponse)
async def fileBackup(token: str = Depends(oauth2_scheme)):
    return {"token": token}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail= "Falscher Nutzername oder Passwort")
    user = UserInDB(**user_dict)
    