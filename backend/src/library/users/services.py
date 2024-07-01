from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import secrets

# Local imports
from library.config import users_collection

# Secret key to encode and decode JWT tokens
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = users_collection.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return user

def register_user_on_db(username: str, password: str):
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    user = {"username": username, "hashed_password": hashed_password}
    result = users_collection.insert_one(user)
    if result.inserted_id:
        print(f"User {username} registered successfully")
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=500, detail="User registration failed")

def log_in_user(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Trying to log in with username: {form_data.username}")
    user = users_collection.find_one({"username": form_data.username})
    print(f"User found: {user}")
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        print(f"Login failed for user: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


