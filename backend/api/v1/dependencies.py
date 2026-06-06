from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from backend.database.session import get_db
from backend.database.models.users import User
from backend.auth.jwt import verify_token
from backend.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        if settings.APP_ENV == "development":
            user = db.query(User).filter(User.email == "testwriter@regudraft.com").first()
            if not user:
                from backend.auth.hashing import Hasher
                user = User(
                    email="testwriter@regudraft.com",
                    hashed_password=Hasher.get_password_hash("securepassword123"),
                    role="WRITER"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            return user
        else:
            raise credentials_exception

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    email = payload.get("email")
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


def require_role(roles: List[str]):
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user role",
            )
        return current_user
    return dependency
