from fastapi import APIRouter, Response
from sqlalchemy import select

from app.api.deps import DbSession, CurrentUser, verify_password, get_password_hash, create_access_token
from app.models.user import User
from app.schemas.auth import LoginRequest, Token, UserCreate, UserResponse
from app.exceptions import AuthError, CRMException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(request: LoginRequest, response: Response, db: DbSession):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(request.password, user.hashed_password):
        raise AuthError("Invalid email or password")

    token = create_access_token(data={"sub": str(user.id), "email": user.email})
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24,
    )
    return Token(access_token=token)


@router.post("/register", response_model=UserResponse)
async def register(request: UserCreate, db: DbSession):
    result = await db.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none():
        raise CRMException("Email already registered")

    user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session", httponly=True, secure=True, samesite="none")
    return {"message": "Logged out"}
