import re
from contextlib import asynccontextmanager
from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine,get_db
from app.models import Base,User,Application
from app.schemas import Register,Login,Token,ApplicationIn,ApplicationOut,ScoreRequest,ScoreResponse
from app.security import hasher,token_for,current_user
@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn: await conn.run_sync(Base.metadata.create_all)
    yield
app=FastAPI(title="CareerFlow API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.get("/health")
async def health(): return {"status":"ok","service":"careerflow-api"}
@app.post("/auth/register",response_model=Token,status_code=201)
async def register(data:Register,db:AsyncSession=Depends(get_db)):
    if await db.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,"Email already registered")
    user=User(email=data.email,password_hash=hasher.hash(data.password));db.add(user);await db.commit();await db.refresh(user)
    return Token(access_token=token_for(user.id))
@app.post("/auth/login",response_model=Token)
async def login(data:Login,db:AsyncSession=Depends(get_db)):
    user=await db.scalar(select(User).where(User.email==data.email))
    if not user or not hasher.verify(data.password,user.password_hash): raise HTTPException(401,"Invalid credentials")
    return Token(access_token=token_for(user.id))
@app.get("/applications",response_model=list[ApplicationOut])
async def list_applications(user:User=Depends(current_user),db:AsyncSession=Depends(get_db)):
    return list((await db.scalars(select(Application).where(Application.user_id==user.id).order_by(Application.created_at.desc()))).all())
@app.post("/applications",response_model=ApplicationOut,status_code=201)
async def create_application(data:ApplicationIn,user:User=Depends(current_user),db:AsyncSession=Depends(get_db)):
    item=Application(**data.model_dump(),user_id=user.id,fit_score=0);db.add(item);await db.commit();await db.refresh(item);return item
@app.patch("/applications/{item_id}/stage",response_model=ApplicationOut)
async def change_stage(item_id:int,stage:str,user:User=Depends(current_user),db:AsyncSession=Depends(get_db)):
    if stage not in {"Wishlist","Applied","Interview","Offer","Rejected"}: raise HTTPException(422,"Unsupported stage")
    item=await db.scalar(select(Application).where(Application.id==item_id,Application.user_id==user.id))
    if not item: raise HTTPException(404,"Application not found")
    item.stage=stage;await db.commit();await db.refresh(item);return item
@app.post("/analysis/fit",response_model=ScoreResponse)
async def score_fit(data:ScoreRequest,user:User=Depends(current_user)):
    stop={"and","the","with","for","you","our","are","this","that","from","will"}
    words=lambda text:{w for w in re.findall(r"[a-zA-Z+#.]{3,}",text.lower()) if w not in stop}
    required=words(data.job_description);resume=words(data.resume_text);matched=sorted(required&resume);missing=sorted(required-resume)
    score=min(98,round(100*len(matched)/max(1,len(required))))
    return ScoreResponse(score=score,matched=matched[:12],missing=missing[:12])
