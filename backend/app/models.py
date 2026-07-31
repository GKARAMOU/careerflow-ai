from datetime import datetime
from sqlalchemy import String,Text,ForeignKey,func,Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(primary_key=True)
    email:Mapped[str]=mapped_column(String(255),unique=True,index=True)
    password_hash:Mapped[str]=mapped_column(String(255))
class Application(Base):
    __tablename__="applications"
    id:Mapped[int]=mapped_column(primary_key=True)
    company:Mapped[str]=mapped_column(String(120))
    role:Mapped[str]=mapped_column(String(160))
    location:Mapped[str]=mapped_column(String(160),default="Remote")
    stage:Mapped[str]=mapped_column(String(30),default="Wishlist")
    description:Mapped[str]=mapped_column(Text,default="")
    fit_score:Mapped[int]=mapped_column(Integer,default=0)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),index=True)
    created_at:Mapped[datetime]=mapped_column(server_default=func.now())
