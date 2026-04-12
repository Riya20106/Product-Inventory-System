from fastapi import Depends, FastAPI
from model import Product 
from sqlalchemy.orm import Session
from database import sessionlocal,engine 
from fastapi.middleware.cors import CORSMiddleware
import modeldatabase
app = FastAPI()
  
app.add_middleware(
CORSMiddleware, 
allow_origins=["http://localhost:3000"],
allow_methods =["*"]
)
modeldatabase.Base.metadata.create_all(bind=engine)

@app.get("/")

def greet():
 return "hello from Riya"
 

Products = [
Product(id=1, name="Phone", description="A smartphone", price =699.99, quantity=50),
Product(id=2, name="Laptop", description="A powerful laptop", price= 999.99, quantity=30),
Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
Product(id=4, name="Table", description="A wooden table", price =199.99, quantity=20),
] 

def get_db():
 db = sessionlocal()
 try : 
   yield db 
 finally: 
   db.close() 

def init_db(): 
  db = sessionlocal()
  count =0 
  count =db.query(modeldatabase.Product).count()
  if count==0:
   for Product in Products:
    db.add(modeldatabase.Product(**Product.model_dump())) 
    db.commit()

init_db()

@app.get("/products") 
def get_all_products(db :Session =Depends(get_db)):   # type: ignore

 db_product = db.query(modeldatabase.Product).all()
 return db_product 

@app.get("/products/{id}") 
def get_productbyid(id:int ,db :Session =Depends(get_db)):
  db_product = db.query(modeldatabase.Product).filter(modeldatabase.Product.id==id).first()
  if db_product:
   return db_product
  return "product not found"

@app.post("/products")
def add_product(product :Product,db :Session =Depends(get_db)):
  
 db.add(modeldatabase.Product(**product.model_dump())) 
 db.commit()
 return product;

@app.put("/products/{id}")
def update_product(id:int,product:Product,db :Session =Depends(get_db)): 
  db_product = db.query(modeldatabase.Product).filter(modeldatabase.Product.id==id).first()
  if db_product: 
     db_product.name = product.name
     db_product.description = product.description
     db_product.price = product.price 
     db_product.quantity = product.quantity 
     db.commit() 
     return "product updated"
  return "no product found" 

@app.delete("/products/{id}") 
def delete_product(id :int,db :Session =Depends(get_db)): 
  db_product = db.query(modeldatabase.Product).filter(modeldatabase.Product.id==id).first()
  if db_product: 
     db.delete(db_product) 
     db.commit()
     return "product deleted" 
  else:
   return "product not found"
      