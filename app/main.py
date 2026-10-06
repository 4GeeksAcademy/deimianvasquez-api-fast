from fastapi import FastAPI, HTTPException, status

app = FastAPI()
from app.routers import contacts

app.include_router(contacts.router, tags=["Contacts"])

@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# CRUD
# C-reate - POST
# R-ead - GET
# U-pdate - PUT(Se actualiza todo el recurso) o PATCH(Se actualiza parcialmente el recurso)
# D-elete - DELETE


# {
#     "name":"deimian"
# }

# {
#     "name":"deimian",
#     "age": 45,
#     "email": "deimian@example.com",
#     "url_avatar": "https://example.com/avatar.jpg"
# }

