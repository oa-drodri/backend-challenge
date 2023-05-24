from auth.jwt_bearer import JWTBearer
from fastapi import Body, APIRouter, Depends, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import decode_jwt, sign_jwt
from database.database import add_user
from models.admin import User, UserData, UserSignIn

router = APIRouter()

token_listener = JWTBearer()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def user_login(admin_credentials: UserSignIn = Body(...)):
    admin_exists = await User.find_one(
        User.email == admin_credentials.username
    )
    if admin_exists:
        password = hash_helper.verify(
            admin_credentials.password, admin_exists.password)
        if password:
            return sign_jwt(
                admin_credentials.username, admin_exists.role
            )

        raise HTTPException(
            status_code=403,
            detail="Incorrect email or password"
        )

    raise HTTPException(
        status_code=403,
        detail="Incorrect email or password"
    )


@router.post("/new", response_model=UserData)
async def user_signup(
    new_user: User = Body(...), token: str = Depends(token_listener)
):
    admin = decode_jwt(token)
    if admin.get('role') != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="User does not have enough permission"
        )
    user_exists = await User.find_one(User.email == new_user.email)
    if user_exists:
        raise HTTPException(
            status_code=409,
            detail="User with email supplied already exists"
        )

    new_user.password = hash_helper.encrypt(new_user.password)
    new_user.role = "NORMAL"
    new_user = await add_user(new_user)
    return new_user
