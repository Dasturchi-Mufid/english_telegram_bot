from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    level: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True) # Masalan: Reading, Listening
    
    # Kategoriya o'chsa, ichidagi materiallar ham o'chishi uchun (optional)
    materials: Mapped[List["Material"]] = relationship(back_populates="category_rel", cascade="all, delete-orphan")

class Material(Base):
    __tablename__ = 'materials'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))       # Fayl nomi (masalan: IELTS Reading Mock #1)
    category: Mapped[str] = mapped_column(String(50))    # Bo'lim (Reading, Listening, etc.)
    file_id: Mapped[str] = mapped_column(String(255))     # Telegram bergan file_id
    file_type: Mapped[str] = mapped_column(String(20))   # document, audio, video