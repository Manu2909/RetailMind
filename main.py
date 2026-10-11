from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import joblib
import os

# Import our database files
import models
import schemas
from database import get_db, engine

app = FastAPI(title="RetailMind API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ml_model = None

@app.on_event("startup")
async def load_model():
    global ml_model
    model_path = os.path.join(os.path.dirname(__file__), '../ml_pipeline/models/lightgbm_retail_model.pkl')
    try:
        ml_model = joblib.load(model_path)
    except Exception as e:
        print(f"Warning: Could not load ML model. {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": ml_model is not None}

# --- NEW INVENTORY API ENDPOINTS ---

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the inventory database."""
    # Check if product already exists
    db_product = db.query(models.Product).filter(models.Product.item_id == product.item_id).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Item ID already registered")
    
    # Create and save new product
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Fetch a list of all products in the inventory."""
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products