from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

store = {}

class SpreadsheetCreate(BaseModel):
    name: str

class CellUpdate(BaseModel):
    cell: str
    value: str

@app.post("/spreadsheets")
def create_sheet(sheet: SpreadsheetCreate):
    sheet_id = str(uuid.uuid4())
    store[sheet_id] = {"name": sheet.name, "cells": {}}
    return {"id": sheet_id, "name": sheet.name}

@app.get("/spreadsheets/{sheet_id}")
def get_sheet(sheet_id: str):
    if sheet_id not in store:
        raise HTTPException(status_code=404, detail="Sheet not found")
    return {"id": sheet_id, "name": store[sheet_id]["name"]}

@app.post("/spreadsheets/{sheet_id}/cells")
def update_cell(sheet_id: str, cell: CellUpdate):
    if sheet_id not in store:
        raise HTTPException(status_code=404, detail="Sheet not found")
    store[sheet_id]["cells"][cell.cell] = cell.value
    return {"message": "Cell updated"}

@app.get("/spreadsheets/{sheet_id}/cells")
def get_cells(sheet_id: str):
    if sheet_id not in store:
        raise HTTPException(status_code=404, detail="Sheet not found")
    return {"cells": store[sheet_id]["cells"]}
