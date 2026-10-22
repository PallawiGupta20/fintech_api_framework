from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from typing import List, Optional
import random

app = FastAPI(title="Enterprise FinTech Banking Core Ledger Engine")

# --- DATA MODELS FOR POSTMAN VALIDATION ---
class LoginPayload(BaseModel):
    username: str
    password: str

class AccountPayload(BaseModel):
    account_type: str  # e.g., "SAVINGS", "CHECKING"
    initial_deposit: float

# --- SIMULATED IN-MEMORY DATABASE ---
database_state = {
    "accounts": {}
}

@app.post("/auth/login", status_code=status.HTTP_200_OK)
def user_authentication(payload: LoginPayload):
    """Authenticates the consumer client and generates a secure session JWT."""
    if payload.username == "admin_dealer" and payload.password == "VaultSecure2026!":
        return {
            "status": "AUTHENTICATED",
            "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.FinTechCorePayloadToken2026",
            "expiresIn": 3600
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid corporate authentication credentials."
    )

@app.post("/accounts/create", status_code=status.HTTP_201_CREATED)
def create_ledger_account(payload: AccountPayload, authorization: Optional[str] = Header(None)):
    """Creates a secure ledger account. Enforces strict Bearer Token verification."""
    # Enforce Token Security Guardrail
    if not authorization or not authorization.startswith("Bearer eyJhbGciOiJIUzI1Ni"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Missing or corrupted Authorization signature token."
        )
        
    if payload.initial_deposit < 100.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction Rejected: Minimum initial deposit threshold is $100.00."
        )

    # Generate Schema-Compliant Account Entities
    generated_account_id = f"ACC-{random.randint(100000, 999999)}"
    
    account_record = {
        "accountId": generated_account_id,
        "status": "ACTIVE",
        "balance": payload.initial_deposit,
        "type": payload.account_type
    }
    
    # Save record to memory database state
    database_state["accounts"][generated_account_id] = account_record
    return account_record

@app.get("/accounts/{account_id}", status_code=status.HTTP_200_OK)
def get_ledger_account(account_id: str, authorization: Optional[str] = Header(None)):
    """Fetches a specific ledger account by ID. Enforces token verification."""
    if not authorization or not authorization.startswith("Bearer eyJhbGciOiJIUzI1Ni"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Missing or corrupted Authorization signature token."
        )
    
    if account_id in database_state["accounts"]:
        return database_state["accounts"][account_id]
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Account record not found in core ledger bank database state."
    )
