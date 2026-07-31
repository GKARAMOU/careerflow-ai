from datetime import datetime
from pydantic import BaseModel,ConfigDict,EmailStr,Field
class Register(BaseModel): email:EmailStr; password:str=Field(min_length=10,max_length=128)
class Login(Register): pass
class Token(BaseModel): access_token:str; token_type:str="bearer"
class ApplicationIn(BaseModel):
    company:str=Field(min_length=1,max_length=120)
    role:str=Field(min_length=1,max_length=160)
    location:str=Field(default="Remote",max_length=160)
    stage:str=Field(default="Wishlist",pattern="^(Wishlist|Applied|Interview|Offer|Rejected)$")
    description:str=Field(default="",max_length=10000)
class ApplicationOut(ApplicationIn):
    id:int; fit_score:int; created_at:datetime
    model_config=ConfigDict(from_attributes=True)
class ScoreRequest(BaseModel): job_description:str=Field(min_length=20,max_length=10000); resume_text:str=Field(min_length=20,max_length=20000)
class ScoreResponse(BaseModel): score:int; matched:list[str]; missing:list[str]
