from fastapi import APIRouter, HTTPException, status

from app.models.todos import Todo, TodoCreate, TodoReplace, TodoUpdate


router = APIRouter()

todos: list[dict] = []
next_id = 1


@router.get("/todos", response_model=list[Todo])
async def get_todos(completed: bool | None = None):
    if completed is None:
        return todos
    return [todo for todo in todos if todo["completed"] is completed]


@router.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(id=next_id, **todo.model_dump())
    next_id += 1
    todos.append(new_todo.model_dump())
    return new_todo


@router.put("/todos/{todo_id}", response_model=Todo)
async def replace_todo(todo_id: int, updated_todo: TodoReplace):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            replacement = Todo(id=todo_id, **updated_todo.model_dump())
            todos[index] = replacement.model_dump()
            return replacement
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.patch("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_fields: TodoUpdate):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            updated_todo = Todo.model_validate(todo).model_dump()
            updated_todo.update(updated_fields.model_dump(exclude_unset=True))
            todos[index] = Todo.model_validate(updated_todo).model_dump()
            return todos[index]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(index)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")