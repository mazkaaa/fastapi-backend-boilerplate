from typing import List

from fastapi import APIRouter, HTTPException, Path, status

from app.crud.items import store
from app.schemas.item import Item, ItemCreate, ItemUpdate


router = APIRouter(prefix="/items", tags=["items"]) 


@router.get(
    "/",
    response_model=List[Item],
    summary="List items",
    description="Retrieve all items currently stored in memory.",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "name": "Sample", "description": "Test item"},
                        {"id": 2, "name": "Gadget", "description": "Another item"},
                    ]
                }
            },
        }
    },
)
def list_items():
    return [Item(id=i.id, name=i.name, description=i.description) for i in store.list()]


@router.post(
    "/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create item",
    description="Create a new item with a generated ID.",
    responses={
        201: {
            "description": "Item created successfully",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "Sample", "description": "Test item"}
                }
            },
        },
        422: {"description": "Validation error"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "basic": {
                            "summary": "Minimal",
                            "description": "Minimal valid create payload",
                            "value": {"name": "Sample"},
                        },
                        "withDescription": {
                            "summary": "With description",
                            "value": {"name": "Sample", "description": "Test item"},
                        },
                    }
                }
            }
        }
    },
)
def create_item(payload: ItemCreate):
    item = store.create(name=payload.name, description=payload.description)
    return Item(id=item.id, name=item.name, description=item.description)


@router.get(
    "/{item_id}",
    response_model=Item,
    summary="Get item",
    description="Fetch an item by its ID.",
    responses={
        200: {
            "description": "Item found",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "Sample", "description": "Test item"}
                }
            },
        },
        404: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        },
    },
)
def get_item(item_id: int = Path(..., ge=1, description="ID of the item to retrieve", examples=[1])):
    item = store.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return Item(id=item.id, name=item.name, description=item.description)


@router.patch(
    "/{item_id}",
    response_model=Item,
    summary="Update item",
    description="Partially update an item. Only provided fields will be updated.",
    responses={
        200: {
            "description": "Item updated",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "Sample", "description": "Updated"}
                }
            },
        },
        404: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        },
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "rename": {
                            "summary": "Rename item",
                            "value": {"name": "Updated name"},
                        },
                        "redescribe": {
                            "summary": "Update description",
                            "value": {"description": "Updated"},
                        },
                    }
                }
            }
        }
    },
)
def update_item(
    payload: ItemUpdate,
    item_id: int = Path(..., ge=1, description="ID of the item to update", examples=[1]),
):
    item = store.update(item_id, name=payload.name, description=payload.description)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return Item(id=item.id, name=item.name, description=item.description)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete item",
    description="Delete an item by its ID.",
    responses={
        404: {
            "description": "Item not found",
            "content": {"application/json": {"example": {"detail": "Item not found"}}},
        }
    },
)
def delete_item(item_id: int = Path(..., ge=1, description="ID of the item to delete", examples=[1])):
    deleted = store.delete(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
