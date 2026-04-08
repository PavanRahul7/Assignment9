# main.py

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from typing import List, Optional
from app.operations import add, subtract, multiply, divide
from app.database import Base, engine, get_db, User, Calculation
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables (idempotent; init.sql already handles first run)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Calculator with PostgreSQL")

# Setup templates directory
templates = Jinja2Templates(directory="templates")

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class OperationRequest(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")

    @field_validator('a', 'b')
    def validate_numbers(cls, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Both a and b must be numbers.')
        return value

class OperationResponse(BaseModel):
    result: float = Field(..., description="The result of the operation")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")

class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    email: str    = Field(..., max_length=100)

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class CalcCreate(BaseModel):
    operation: str  = Field(..., max_length=20)
    operand_a: float
    operand_b: float
    result:    float
    user_id:   int

class CalcOut(BaseModel):
    id:        int
    operation: str
    operand_a: float
    operand_b: float
    result:    float
    user_id:   int

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException on {request.url.path}: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    logger.error(f"ValidationError on {request.url.path}: {error_messages}")
    return JSONResponse(status_code=400, content={"error": error_messages})

# ---------------------------------------------------------------------------
# Calculator routes (original)
# ---------------------------------------------------------------------------

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/add", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def add_route(operation: OperationRequest):
    try:
        return OperationResponse(result=add(operation.a, operation.b))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/subtract", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def subtract_route(operation: OperationRequest):
    try:
        return OperationResponse(result=subtract(operation.a, operation.b))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/multiply", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def multiply_route(operation: OperationRequest):
    try:
        return OperationResponse(result=multiply(operation.a, operation.b))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/divide", response_model=OperationResponse, responses={400: {"model": ErrorResponse}})
async def divide_route(operation: OperationRequest):
    try:
        return OperationResponse(result=divide(operation.a, operation.b))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ---------------------------------------------------------------------------
# User CRUD routes
# ---------------------------------------------------------------------------

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

# ---------------------------------------------------------------------------
# Calculation CRUD routes
# ---------------------------------------------------------------------------

@app.post("/calculations", response_model=CalcOut, status_code=201)
def create_calculation(calc: CalcCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == calc.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_calc = Calculation(**calc.model_dump())
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

@app.get("/calculations", response_model=List[CalcOut])
def list_calculations(db: Session = Depends(get_db)):
    return db.query(Calculation).all()

@app.get("/calculations/{calc_id}", response_model=CalcOut)
def get_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc

@app.put("/calculations/{calc_id}", response_model=CalcOut)
def update_calculation(calc_id: int, result: float, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    calc.result = result
    db.commit()
    db.refresh(calc)
    return calc

@app.delete("/calculations/{calc_id}", status_code=204)
def delete_calculation(calc_id: int, db: Session = Depends(get_db)):
    calc = db.query(Calculation).filter(Calculation.id == calc_id).first()
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    db.delete(calc)
    db.commit()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
