from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db, create_tables, Item, User
from schemas import ItemCreate, ItemResponse, ErrorResponse, UserCreate, UserResponse, UserLogin, Token
from config import API_TITLE, API_DESCRIPTION, API_VERSION, logger
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Args:
        user (UserCreate): User registration data
        
    Returns:
        UserResponse: The created user information
    """
    try:
        logger.info(f"Attempting to register user: {user.email}")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            logger.warning(f"User with email '{user.email}' already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{user.email}' already exists"
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"Successfully registered user with ID: {db_user.id}")
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        )

@app.post("/auth/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password to get access token.
    
    Args:
        user_credentials (UserLogin): Login credentials
        
    Returns:
        Token: Access token and user information
    """
    try:
        logger.info(f"Login attempt for user: {user_credentials.email}")
        
        # Authenticate user
        user = authenticate_user(user_credentials.email, user_credentials.password, db)
        if not user:
            logger.warning(f"Failed login attempt for user: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        logger.info(f"Successful login for user: {user.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@app.get("/items", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def get_all_items(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all items for the authenticated user.
    
    Returns:
        List[ItemResponse]: List of items owned by the current user
    """
    try:
        logger.info(f"Fetching items for user: {current_user.email}")
        items = db.query(Item).filter(Item.owner_id == current_user.id).all()
        logger.info(f"Successfully retrieved {len(items)} items for user {current_user.email}")
        return items
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve items"
        )

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new item for the authenticated user.
    
    Args:
        item (ItemCreate): The item data to create
        
    Returns:
        ItemResponse: The created item with its ID and timestamp
    """
    try:
        logger.info(f"Creating new item: {item.name} for user: {current_user.email}")
        
        # Check if item with same name already exists for this user
        existing_item = db.query(Item).filter(
            Item.name == item.name,
            Item.owner_id == current_user.id
        ).first()
        if existing_item:
            logger.warning(f"Item with name '{item.name}' already exists for user {current_user.email}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with name '{item.name}' already exists"
            )
        
        # Create new item
        db_item = Item(
            name=item.name,
            description=item.description,
            owner_id=current_user.id
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        logger.info(f"Successfully created item with ID: {db_item.id} for user: {current_user.email}")
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
async def get_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific item by ID for the authenticated user.
    
    Args:
        item_id (int): The ID of the item to retrieve
        
    Returns:
        ItemResponse: The requested item
    """
    try:
        logger.info(f"Fetching item with ID: {item_id} for user: {current_user.email}")
        item = db.query(Item).filter(
            Item.id == item_id,
            Item.owner_id == current_user.id
        ).first()
        
        if not item:
            logger.warning(f"Item with ID {item_id} not found for user {current_user.email}")
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