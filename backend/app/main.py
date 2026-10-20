
import os
import re
import secrets
import uuid
from contextlib import asynccontextmanager
from datetime import date

import httpx
from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    Header,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Order, SupportTicket

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID", "")
TOOL_SECRET = os.getenv("SUPPORT_TOOL_SECRET", "")

if not TOOL_SECRET:
    raise RuntimeError("SUPPORT_TOOL_SECRET is required")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    # Sample records for local testing only.
    # Never overwrite an existing order.
    from app.database import SessionLocal

    with SessionLocal() as db:
        existing = db.scalar(
            select(Order).where(
                Order.order_id == "ORD-1001"
            )
        )
        if existing is None:
            db.add(
                Order(
                    order_id="ORD-1001",
                    customer_email="demo@example.com",
                    status="shipped",
                    estimated_delivery="2026-10-21",
                )
            )
            db.commit()

    yield


app = FastAPI(
    title="Voice AI Customer Support API",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [
    item.strip()
    for item in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173",
    ).split(",")
    if item.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Support-Tool-Secret"],
)


def require_tool_secret(
    supplied: str | None = Header(
        default=None,
        alias="X-Support-Tool-Secret",
    ),
):
    if (
        not supplied
        or not secrets.compare_digest(
            supplied, TOOL_SECRET
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )


class OrderLookup(BaseModel):
    order_id: str = Field(
        min_length=3, max_length=40
    )
    customer_email: EmailStr


class TicketRequest(BaseModel):
    issue: str = Field(
        min_length=5, max_length=2000
    )
    customer_email: EmailStr | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/voice/signed-url")
async def get_voice_signed_url():
    if not API_KEY or not AGENT_ID:
        raise HTTPException(
            status_code=503,
            detail="Voice service is not configured",
        )

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                "https://api.elevenlabs.io/v1/convai/"
                "conversation/get-signed-url",
                params={"agent_id": AGENT_ID},
                headers={"xi-api-key": API_KEY},
            )
            response.raise_for_status()
            payload = response.json()

        signed_url = payload.get("signed_url")
        if not signed_url:
            raise HTTPException(
                status_code=502,
                detail="Voice provider returned no session URL",
            )

        return {"signed_url": signed_url}

    
    except httpx.HTTPStatusError as exc:
        # Log status and response body, never the API key.
        print(
            "ElevenLabs API error:",
            exc.response.status_code,
            exc.response.text[:500],
        )
        raise HTTPException(
            status_code=502,
            detail=(
                "ElevenLabs returned HTTP "
                f"{exc.response.status_code}. "
                "Check backend terminal."
            ),
        ) from None

    except httpx.RequestError as exc:
        print("ElevenLabs connection error:", str(exc))
        raise HTTPException(
            status_code=502,
            detail="Could not connect to ElevenLabs API.",
        ) from None



@app.post(
    "/api/tools/check-order",
    dependencies=[Depends(require_tool_secret)],
)
def check_order(
    payload: OrderLookup,
    db: Session = Depends(get_db),
):
    order_id = payload.order_id.strip()
    email = str(payload.customer_email).strip().lower()

    order = db.scalar(
        select(Order).where(
            Order.order_id == order_id,
            Order.customer_email == email,
        )
    )

    # Use the same response for unknown IDs and
    # mismatched emails to avoid revealing order existence.
    if order is None:
        return {
            "ok": False,
            "message": (
                "Order not found or customer details "
                "could not be verified."
            ),
        }

    return {
        "ok": True,
        "order_id": order.order_id,
        "status": order.status,
        "estimated_delivery": order.estimated_delivery,
    }


@app.post(
    "/api/tools/create-ticket",
    dependencies=[Depends(require_tool_secret)],
)
def create_ticket(
    payload: TicketRequest,
    db: Session = Depends(get_db),
):
    ticket = SupportTicket(
        ticket_id=f"TKT-{uuid.uuid4().hex[:10].upper()}",
        issue=payload.issue.strip(),
        customer_email=(
            str(payload.customer_email).strip().lower()
            if payload.customer_email
            else None
        ),
        status="open",
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "ok": True,
        "ticket_id": ticket.ticket_id,
        "status": ticket.status,
        "message": "Support ticket created successfully.",
    }
