# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/schemas.py | Selected source lines: 4-43
# This incomplete excerpt is for portfolio review; it is not a runnable application.

class Fields(BaseModel):
    model_config = ConfigDict(extra='forbid')
    supplier: str | None = None
    document_type: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    invoice_date_raw: str | None = None
    due_date_raw: str | None = None
    amount: float | None = Field(default=None, allow_inf_nan=False)
    currency: str | None = None
    subtotal: float | None = Field(default=None, allow_inf_nan=False)
    vat: float | None = Field(default=None, allow_inf_nan=False)
    payment_terms: str | None = None
    payment_details: str | None = None
    recipient: str | None = None

    @field_validator('invoice_date', 'due_date')
    @classmethod
    def check_date(cls, value):
        if value:
            date.fromisoformat(value)
        return value

    @field_validator('currency')
    @classmethod
    def check_currency(cls, value):
        if value is not None and (len(value) != 3 or not value.isalpha()):
            raise ValueError('Use a three-letter currency code')
        return value.upper() if value else None

class Selection(BaseModel):
    document_ids: list[int] = Field(max_length=200)

class Question(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    document_ids: list[int] | None = Field(default=None, max_length=200)
    session_id: str = Field(default='default', min_length=1, max_length=100, pattern=r'^[\w-]+$')

    @field_validator('question')
# END OF EXCERPT. The remaining code is private.
