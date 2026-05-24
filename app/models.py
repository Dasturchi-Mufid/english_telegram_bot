from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Float
from datetime import datetime, timezone
from typing import List

# Base klassini o'zimizning database.py dan import qilamiz
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    level: Mapped[str] = mapped_column(String(50), nullable=True, default="Beginner")
    # datetime.now(timezone.utc) - xatoliklarni oldini olish uchun eng xavfsiz usul
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    language: Mapped[str] = mapped_column(String(5), nullable=True, default=None)

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Material bilan bog'lanish (relationship nomi aniqroq bo'lishi uchun 'materials')
    materials: Mapped[List["Material"]] = relationship(back_populates="category_rel", cascade="all, delete-orphan")

class Material(Base):
    __tablename__ = 'materials'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    file_id: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(20)) # document, audio, video
    level: Mapped[str] = mapped_column(String(50), nullable=True, default="Beginner")
    
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete="CASCADE"))
    category_rel: Mapped["Category"] = relationship(back_populates="materials")

class Question(Base):
    __tablename__ = 'questions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500))
    option_a: Mapped[str] = mapped_column(String(200))
    option_b: Mapped[str] = mapped_column(String(200))
    option_c: Mapped[str] = mapped_column(String(200))
    option_d: Mapped[str] = mapped_column(String(200))
    correct_option: Mapped[str] = mapped_column(String(1)) # 'a', 'b', 'c', 'd'
    level: Mapped[str] = mapped_column(String(20), default="Beginner")

class QuizResult(Base):
    __tablename__ = 'quiz_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    # Foydalanuvchi bilan bog'liqlik (User.tg_id ga ulanadi)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.tg_id", ondelete="CASCADE"))
    
    score: Mapped[int] = mapped_column()  # To'g'ri javoblar soni
    total_questions: Mapped[int] = mapped_column()  # Umumiy savollar soni
    percentage: Mapped[float] = mapped_column(Float) # Foiz ko'rsatkichi (masalan: 85.5)
    
    # Test topshirilgan vaqtdagi erishilgan daraja
    level_achieved: Mapped[str] = mapped_column(String(20)) 
    
    # Test topshirilgan sana
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)




