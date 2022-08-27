from fastapi import FastAPI, Body, Depends
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.post("/")
def addItem(item:schemas.Item, session = Depends(get_session)):
    item = models.Item(address = item.address)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/{id}")
def getItem(id:int, session = Depends(get_session)): 
    return session.query(models.Item).get(id)

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session = Depends(get_session)):
    item_task = session.query(models.Item).get(id)
    item_task.address = item.address
    session.commit()
    return item_task

@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'