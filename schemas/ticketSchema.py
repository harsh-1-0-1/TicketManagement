from pydantic import BaseModel

class TicketSchema(BaseModel):
    title: str
    description: str
    price: int

    class Config:
        orm_mode = True

class TicketCreate(TicketSchema):
    pass

class TicketDelete(BaseModel):
    id: int  # assuming deletion by ticket ID

    class Config:
        orm_mode = True
