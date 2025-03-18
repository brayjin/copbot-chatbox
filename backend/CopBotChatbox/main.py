from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Optional
import logging

from CopBotChatbox.database import initialize_db
import CopBotChatbox.crud as crud
from CopBotChatbox.models import Procedure, ProcedureUpdate, QueryRequest, LoginRequest
from CopBotChatbox.auth import create_access_token, verify_token
from CopBotChatbox.nlp_service import process_query_with_rasa

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = FastAPI(title="CopBotChatbox Backend with FastAPI")

@app.on_event("startup")
def startup_event():
    initialize_db()
    logging.info("Database initialized successfully.")

def admin_required(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    return verify_token(token)

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password123":
        access_token = create_access_token({"sub": request.username})
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/procedures")
def get_procedures():
    try:
        procedures = crud.read_procedures()
        return {"procedures": procedures}
    except Exception as e:
        logging.error(f"Error fetching procedures: {e}")
        raise HTTPException(status_code=500, detail="Error fetching procedures")

@app.post("/procedures", dependencies=[Depends(admin_required)])
def create_new_procedure(procedure: Procedure):
    try:
        proc_id = crud.create_procedure(procedure.title, procedure.description)
        return {"id": proc_id, "message": "Procedure created successfully"}
    except Exception as e:
        logging.error(f"Error creating procedure: {e}")
        raise HTTPException(status_code=500, detail="Error creating procedure")

@app.put("/procedures/{proc_id}", dependencies=[Depends(admin_required)])
def update_existing_procedure(proc_id: int, procedure: ProcedureUpdate):
    try:
        success = crud.update_procedure(proc_id, procedure.title, procedure.description)
        if success:
            return {"message": "Procedure updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Procedure not found")
    except Exception as e:
        logging.error(f"Error updating procedure: {e}")
        raise HTTPException(status_code=500, detail="Error updating procedure")

@app.delete("/procedures/{proc_id}", dependencies=[Depends(admin_required)])
def delete_existing_procedure(proc_id: int):
    try:
        success = crud.delete_procedure(proc_id)
        if success:
            return {"message": "Procedure deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Procedure not found")
    except Exception as e:
        logging.error(f"Error deleting procedure: {e}")
        raise HTTPException(status_code=500, detail="Error deleting procedure")

@app.post("/query")
def query_handler(request: QueryRequest):
    try:
        result = process_query_with_rasa(request.query)
        return {"rasa_response": result}
    except Exception as e:
        logging.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Error processing query")
