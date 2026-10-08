from pydantic import BaseModel, Field, EmailStr


class ContactCreate(BaseModel):
    name: str
    email: EmailStr = Field(..., description="The email address of the contact")
    phone: str
    city: str | None = None


class ContactReplace(BaseModel):
    name: str
    email: EmailStr = Field(..., description="The email address of the contact")
    phone: str
    city: str | None = None


class ContactUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    city: str | None = None


class Contact(ContactCreate):
    id: int