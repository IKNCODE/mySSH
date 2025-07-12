from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return {"Hello" : "world!"}

if __name__ == "__main__":
    app.run()

