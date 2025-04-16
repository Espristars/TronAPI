from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime
import asyncio
from models import AsyncSessionLocal, engine, Base, WalletRequest
from tron import get_tron_info


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.create_task(init_models())

app = FastAPI()


class AddressRequest(BaseModel):
    address: str


class TronInfoResponse(BaseModel):
    address: str
    bandwidth: int
    energy: int
    balance_trx: float
    timestamp: datetime


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/wallet", response_model=TronInfoResponse)
async def get_wallet_info(request: AddressRequest, db=Depends(get_db)):
    try:
        info = await asyncio.get_event_loop().run_in_executor(None, get_tron_info, request.address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка получения данных: {e}")

    wallet_record = WalletRequest(
        wallet=request.address,
        bandwidth=info["bandwidth"],
        energy=info["energy"],
        balance_trx=info["balance_trx"],
        created_at=datetime
    )
    db.add(wallet_record)
    await db.commit()
    await db.refresh(wallet_record)

    return TronInfoResponse(
        address=request.address,
        bandwidth=info["bandwidth"],
        energy=info["energy"],
        balance_trx=info["balance_trx"],
        timestamp=wallet_record.created_at
    )


@app.get("/records", response_model=List[TronInfoResponse])
async def list_records(page: int = Query(1, ge=1), size: int = Query(10, ge=1), db=Depends(get_db)):
    offset = (page - 1) * size
    result = await db.execute(
        WalletRequest.__table__.select().order_by(WalletRequest.created_at.desc()).offset(offset).limit(size)
    )
    records = result.fetchall()

    return [
        TronInfoResponse(
            address=record.wallet,
            bandwidth=record.bandwidth,
            energy=record.energy,
            balance_trx=record.balance_trx,
            timestamp=record.created_at
        )
        for record in records
    ]
