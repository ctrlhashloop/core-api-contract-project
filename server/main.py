from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Core Banking Service")


class AccountResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str
    account_number: str = Field(alias="accountNumber")
    balance: float
    currency: str


# In-memory mock database
ACCOUNTS_DB = {
    "123e4567-e89b-12d3-a456-426614174000": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "accountNumber": "ACC-987654",
        "balance": 1500.50,
        "currency": "USD",
    }
}


@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str):
    if account_id not in ACCOUNTS_DB:
        raise HTTPException(status_code=404, detail="Account not found")
    return ACCOUNTS_DB[account_id]
