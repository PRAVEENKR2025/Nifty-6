from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

SECRET_KEY = "supersecretkey"   # replace with env variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_db_connection():
    conn = sqlite3.connect("data/n100.db")
    conn.row_factory = sqlite3.Row
    return conn

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

@router.post("/signup")
def signup(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = get_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    conn.close()
    return {"status": "created", "username": username}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": user["username"]}


@router.post("/signup")
def signup(username: str, password: str, role: str = "viewer"):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_pw = get_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    conn.close()
    return {"status": "created", "username": username, "role": role}


def get_current_user_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user["role"]

def role_required(required_role: str):
    def wrapper(role: str = Depends(get_current_user_role)):
        if role != required_role:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
    return wrapper


@router.get("/admin-only")
def admin_data(role: str = Depends(role_required("admin"))):
    return {"secret": "This is admin-only data"}
