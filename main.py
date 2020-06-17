from typing import List

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db import interaction, models, schemas
from db.database import SessionLocal, engine

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import auth, counters, registry, users

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")

app = FastAPI(title="RCAS API", version="0.1", description="API of the resource consumption accounting system.")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, prefix="/api/token", tags=["Authentication"])
app.include_router(counters.router, prefix="/api/counters", tags=["Counters"])
app.include_router(registry.router, prefix="/api/registry", tags=["Registry"])
app.include_router(users.router, prefix="/api/users", tags=["Users"]) # , dependencies=[Depends(get_db)])


@app.get("/")
async def http_main_page(request: Request):
    #return {"version": "1.0"}
    return templates.TemplateResponse("index.html", {"request": request})


#@app.post("/users/", response_model=schemas.User)
#def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#    db_user = crud.get_user_by_email(db, email=user.email)
#    if db_user:
#        raise HTTPException(status_code=400, detail="Email already registered")
#    result = interaction.create_user(db=db, user=user)
#    if result:
#        return result
#    else:
#        raise HTTPException(status_code=400, detail="Phone number must contain 10 digit.")
#
#
#@app.get("/users/", response_model=List[schemas.User])
#def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    users = interaction.get_users(db, skip=skip, limit=limit)
#    return users
#
#
#@app.get("/users/{user_uuid}", response_model=schemas.User)
#def read_user(user_uuid: str, db: Session = Depends(get_db)):
#    db_user = interaction.get_user(db, user_uuid=user_uuid)
#    if db_user is None:
#        raise HTTPException(status_code=404, detail="User not found")
#    return db_user
#
###
#@app.post("/users/{user_id}/items/", response_model=schemas.Item)
#def create_item_for_user(
#    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
#    ):
#    return interaction.create_user_item(db=db, item=item, user_id=user_id)
#
#
#@app.get("/items/", response_model=List[schemas.Item])
#def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#    items = interaction.get_items(db, skip=skip, limit=limit)
#    return items