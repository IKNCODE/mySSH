from fastapi import FastAPI
from paramiko import SSHClient
import socket
from paramiko.ssh_exception import SSHException

client = SSHClient()
client.load_system_host_keys()


app = FastAPI()

@app.get("/")
async def hello():
    return {"Hello" : data}

@app.get("/connect")
async def connect(host: str, username: str):
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
        return {"response" : data}
    except SSHException:
        return {"error" : "Error while try to connect server! Please check hostname!"}


if __name__ == "__main__":
    app.run()

