from pydantic import BaseModel


class ContactCreate(BaseModel):
    name: str
    email: str
    phone: str
    city: str | None = None


class ContactReplace(BaseModel):
    name: str
    email: str
    phone: str
    city: str


class ContactUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    city: str | None = None


class Contact(ContactCreate):
    id: int