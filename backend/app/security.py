from datetime import datetime,timedelta,timezone
import jwt
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import get_db
from app.models import User
hasher=PasswordHash.recommended(); bearer=OAuth2PasswordBearer(tokenUrl="/auth/login")
def token_for(user_id:int)->str:
    return jwt.encode({"sub":str(user_id),"exp":datetime.now(timezone.utc)+timedelta(minutes=45)},settings.jwt_secret,algorithm="HS256")
async def current_user(raw:str=Depends(bearer),db:AsyncSession=Depends(get_db))->User:
    try: user_id=int(jwt.decode(raw,settings.jwt_secret,algorithms=["HS256"])["sub"])
    except (jwt.PyJWTError,KeyError,ValueError): raise HTTPException(401,"Invalid or expired token")
    user=await db.get(User,user_id)
    if not user: raise HTTPException(401,"User not found")
    return user
