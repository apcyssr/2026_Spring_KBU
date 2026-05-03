from typing import Annotated
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

# --- 1. First Steps ---
@app.get("/")
async def root():
    return {"message": "Hello World"}

# --- 2. Path Parameters ---
# รับค่าจาก URL path เช่น /items/5
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# --- 3. Query Parameters ---
# รับค่าจาก query string เช่น /users/?skip=0&limit=10
@app.get("/users/")
async def read_users(skip: int = 0, limit: int = 10):
    fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
    return fake_items_db[skip : skip + limit]

# --- 4. Request Body ---
# รับข้อมูลแบบ JSON ผ่าน Body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

# --- 5. Query Parameters and String Validations ---
# ใช้ Annotated และ Query เพื่อตรวจสอบเงื่อนไข (เช่น ความยาวตัวอักษร)
@app.get("/items-validation/")
async def read_items_validation(
    q: Annotated[
        str | None, 
        Query(
            alias="item-query",      # ชื่อเรียกใน URL
            title="Query string",    # ชื่อหัวข้อใน Docs
            description="ค้นหาไอเท็มตามชื่อ",
            min_length=3,            # ขั้นต่ำ 3 ตัวอักษร
            max_length=50,           # สูงสุด 50 ตัวอักษร
            pattern="^fixedquery$",  # ใช้ Regex ตรวจสอบรูปแบบ
        )
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# รวมหลายแบบในอันเดียว (Path + Query + Body)
@app.put("/items-complex/{item_id}")
async def update_item(
    item_id: int, 
    item: Item, 
    q: str | None = None
):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result