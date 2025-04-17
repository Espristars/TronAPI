from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

class WalletRequest(Base):
    __tablename__ = "wallet_requests"

    id = Column(Integer, primary_key=True, index=True)
    wallet = Column(String, index=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance_trx = Column(Float)
    created_at = Column(DateTime)
