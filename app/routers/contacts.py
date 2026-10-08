import csv
from pathlib import Path
import pandas as pd


from fastapi import APIRouter, HTTPException, status
from app.models.contacts import Contact, ContactCreate, ContactReplace, ContactUpdate


router = APIRouter()

CONTACTS_FILE = Path(__file__).resolve().parents[2] / "data" / "contacts.csv"
LEGACY_CONTACTS_FILE = CONTACTS_FILE.with_suffix(".txt")


SAMPLE_CONTACTS = [
    {
        "id": 1,
        "name": "deimian",
        "email": "deimian@example.com",
        "phone": "123-456-7890",
        "city": "caracas",
    }
]


def save_contacts(contacts: list[dict]) -> None:
    CONTACTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CONTACTS_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["id", "name", "email", "phone", "city"]
        )
        writer.writeheader()
        writer.writerows(contacts)



def load_contacts():
    if CONTACTS_FILE.exists():
        with CONTACTS_FILE.open("r", newline="", encoding="utf-8") as file:
            return [
                {**row, "id": int(row["id"])}
                for row in csv.DictReader(file)
            ]

    # esto es la parte de txt
    if LEGACY_CONTACTS_FILE.exists():
        with LEGACY_CONTACTS_FILE.open("r", newline="", encoding="utf-8") as file:
            contacts = [
                {
                    "id": int(contact_id),
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "city": city,
                }
                for contact_id, name, email, phone, city in csv.reader(
                    file, delimiter="|"
                )
                if contact_id
            ]
        save_contacts(contacts)
        return contacts

    return []



contacts = load_contacts()
next_id = max((contact["id"] for contact in contacts), default=0) + 1

@router.get("/contacts", response_model=list[Contact])
async def get_contacts(city: str | None = None, name: str | None = None):
    return [
        contact
        for contact in contacts
        if (city is None or contact.get("city") == city)
        and (name is None or contact.get("name") == name)
    ]



@router.get("/contacts/{contact_id}", response_model=Contact)
async def get_contact(contact_id: int):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
    )


@router.post("/contacts", response_model=Contact, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate):
    global next_id
    new_contact = Contact(id=next_id, **contact.model_dump())
    next_id += 1
    contacts.append(new_contact.model_dump())
    save_contacts(contacts)
    return new_contact


@router.put("/contacts/{contact_id}", response_model=Contact)
async def replace_contact(contact_id: int, updated_contact: ContactReplace):
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            replacement = Contact(id=contact_id, **updated_contact.model_dump())
            contacts[index] = replacement.model_dump()
            save_contacts(contacts)
            return replacement
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
    )


@router.patch("/contacts/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, updated_fields: ContactUpdate):
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            updated_contact = Contact.model_validate(contact).model_dump()
            updated_contact.update(updated_fields.model_dump(exclude_unset=True))
            contacts[index] = Contact.model_validate(updated_contact).model_dump()
            save_contacts(contacts)
            return contacts[index]
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
    )


@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int):
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            contacts.pop(index)
            save_contacts(contacts)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
    )
