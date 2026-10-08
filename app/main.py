import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import contacts, todos


load_dotenv()

server_url = os.getenv("SERVER_URL", "http://127.0.0.1:8000")

app = FastAPI(servers=[{"url": server_url, "description": "URL Base"}])

app.include_router(contacts.router, tags=["Contacts"])
app.include_router(todos.router, tags=["Todos"])


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
