from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db, create_tables, Item
from schemas import ItemCreate, ItemResponse, ErrorResponse
from config import API_TITLE, API_DESCRIPTION, API_VERSION, logger

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    create_tables()
    logger.info("Database tables created and application started")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception handler caught: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "status_code": 500}
    )

@app.get("/")
async def root():
    return {"message": "Items API", "docs": "/docs", "redoc": "/redoc"}

@app.get("/items", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def get_all_items(db: Session = Depends(get_db)):
    """
    Retrieve all items from the database.
    
    Returns:
        List[ItemResponse]: List of all items in the database
    """
    try:
        logger.info("Fetching all items from database")
        items = db.query(Item).all()
        logger.info(f"Successfully retrieved {len(items)} items")
        return items
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items"
        )

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item in the database.
    
    Args:
        item (ItemCreate): The item data to create
        
    Returns:
        ItemResponse: The created item with its ID and timestamp
    """
    try:
        logger.info(f"Creating new item: {item.name}")
        
        # Check if item with same name already exists
        existing_item = db.query(Item).filter(Item.name == item.name).first()
        if existing_item:
            logger.warning(f"Item with name '{item.name}' already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with name '{item.name}' already exists"
            )
        
        # Create new item
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        logger.info(f"Successfully created item with ID: {db_item.id}")
        return db_item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )

@app.get("/items/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific item by ID.
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        ItemResponse: The requested item
    """
    try:
        logger.info(f"Fetching item with ID: {item_id}")
        item = db.query(Item).filter(Item.id == item_id).first()
        
        if not item:
            logger.warning(f"Item with ID {item_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found"
            )
        
        logger.info(f"Successfully retrieved item: {item.name}")
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve item"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)