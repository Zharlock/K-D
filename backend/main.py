
#C:\Users\torad\Documents\python311\python.exe -m uvicorn main:app --reload    computador Rafael
#C:\Users\torad\Documents\python311\python.exe -m uvicorn Customer:app --reload 

from typing import Union

from fastapi import FastAPI


app = FastAPI()


@app.get("/exemplo")
def exemplo()-> str:
    return "Hello World"

#if __name__ == "__name__":
 #   uvicorn.run(app, port=8000)
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}