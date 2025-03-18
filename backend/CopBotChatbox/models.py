from pydantic import BaseModel

class Procedure(BaseModel):
    title: str
    description: str

class ProcedureUpdate(BaseModel):
    title: str
    description: str

class QueryRequest(BaseModel):
    query: str

class LoginRequest(BaseModel):
    username: str
    password: str
