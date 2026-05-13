from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
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
    name: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Material bilan bog'lanish
    materials: Mapped[list["Material"]] = relationship(back_populates="category_rel")

class Material(Base):
    __tablename__ = 'materials'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    file_id: Mapped[str] = mapped_column(String(255))
    file_type: Mapped[str] = mapped_column(String(20))
    level: Mapped[str] = mapped_column(String(50), nullable=True, default="Beginner")
    
    # MANA SHU QATOR JUDA MUHIM:
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    category_rel: Mapped["Category"] = relationship(back_populates="materials")

class Question(Base):
    __tablename__ = 'questions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500)) # Savol matni
    option_a: Mapped[str] = mapped_column(String(200))
    option_b: Mapped[str] = mapped_column(String(200))
    option_c: Mapped[str] = mapped_column(String(200))
    option_d: Mapped[str] = mapped_column(String(200))
    correct_option: Mapped[str] = mapped_column(String(1)) # 'a', 'b', 'c', yoki 'd'
    level: Mapped[str] = mapped_column(String(20), default="Beginner")