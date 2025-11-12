import uvicorn
from fastapi import FastAPI, Response, Request
from pydantic import BaseModel


class Student(BaseModel):
    name: str
    age: str



LANGUAGES = {
    1: "C++",
    2: "Python",
    3: "GO"
}

app = FastAPI()


@app.get("/health")
async def helth():
    return {"mes": "ok"}


@app.get("/language/{item_id}")
async def lang(item_id):
    return {"mes": LANGUAGES.get(int(item_id), "js")}

@app.get("/add")
async def add(a:int, b:int):
    return {"sum": a + b}

@app.post("/add_student")
async def add_sudent(model: Student):
    print(model.model_dump())
    return model.model_dump()

@app.get("/exam_resp")
async def add_resp(resp: Response):
    resp.headers["X-Custom-REsponse-Header"] = "fastapi"
    
    return {"mes: ""{fastapi}"}

@app.get("/exam_req")
async def add_req(req: Request):
    print(req.headers)
    
    return {"mes: ""{fastapi}"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "0.0.0.0",
        port = 8000,
        reload=True
    )