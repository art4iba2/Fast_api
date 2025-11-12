import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI(title="Простой калькулятор")

current_expression = ""


class Operation(BaseModel):
    a: float
    b: float
    op: str


class Expression(BaseModel):
    expression: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/add")
async def add(op: Operation):
    result = op.a + op.b
    return {"operation": f"{op.a} + {op.b}", "result": result}


@app.post("/subtract")
async def subtract(op: Operation):
    result = op.a - op.b
    return {"operation": f"{op.a} - {op.b}", "result": result}


@app.post("/multiply")
async def multiply(op: Operation):
    result = op.a * op.b
    return {"operation": f"{op.a} * {op.b}", "result": result}


@app.post("/divide")
async def divide(op: Operation):
    if op.b == 0:
        raise HTTPException(status_code=400, detail="Деление на ноль невозможно")
    result = op.a / op.b
    return {"operation": f"{op.a} / {op.b}", "result": result}


@app.post("/create_expression")
async def create_expression(expr: Expression):
    global current_expression
    current_expression = expr.expression
    return {"message": "Выражение сохранено", "expression": current_expression}


@app.get("/get_expression")
async def get_expression():
    if not current_expression:
        return {"message": "Выражение не задано"}
    return {"current_expression": current_expression}


@app.post("/evaluate_expression")
async def evaluate_expression():
    global current_expression
    if not current_expression:
        raise HTTPException(status_code=400, detail="Выражение не задано")
    if not re.fullmatch(r"[0-9+\-*/().\s]+", current_expression):
        raise HTTPException(status_code=400, detail="Выражение содержит недопустимые символы")
    try:
        result = eval(current_expression)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Ошибка: деление на ноль")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка вычисления: {str(e)}")
    return {"expression": current_expression, "result": result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
