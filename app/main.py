from fastapi import FastAPI
from paramiko import SSHClient

client = SSHClient()
client.load_system_host_keys()
client.connect("45.137.188.181", username="base_user", port=22)

stdin, stdout, stderr = client.exec_command('ls -al')
data = stdout.read() + stderr.read()

client.close()

app = FastAPI()

@app.get("/")
async def hello():
    return {"Hello" : data}

@app.get("/connect")
async def connect(host: str, username: str):
    client.connect(hostname=host, username=username, port=22)
    stdin, stdout, stderr = client.exec_command("whoami")

    data = stdout.read() + stderr.read()
    return {"response" : data}

if __name__ == "__main__":
    app.run()

