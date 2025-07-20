from fastapi import FastAPI
from paramiko import SSHClient
import socket
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import NoValidConnectionsError
from .models import models

client = SSHClient()
client.load_system_host_keys()


app = FastAPI()

@app.get("/")
async def hello():
    return {"Hello" : "World!"} 

@app.on_event("startup")
async def on_startup():
    models.create_db_and_tables()

@app.get("/all_servers")
async def get_all_servers(session: models.SessionDep) -> list[models.Server]:
    return models.get_servers(session)
    

@app.get("/connect")
async def connect(session: models.SessionDep, host: str, username: str = None):
    """
    Функция для подключения к удаленному серверу через SSH 
    params: 
    hostname - адрес удаленного сервера
    username - имя пользователя удаленного сервера
    """
    try:
        client.connect(hostname=host, username=username, port=22)
        stdin, stdout, stderr = client.exec_command("whoami")
        data = stdout.read() + stderr.read()
        client.close()
        server = models.Server(hostname=host, private_key_path="None", username=username)
        models.add_server(server, session)
        return {"response" : data}
    except SSHException:
        return {"error" : "Error while try to connect server! Please check hostname!"}
    except socket.gaierror:
        return {"error" : "name or service not known"}
    except TimeoutError:
        return {"error" : "connection time out!"}
    except NoValidConnectionsError:
        return {"error" : f"Unable to connect {host} on port {host}"}



if __name__ == "__main__":
    app.run()

