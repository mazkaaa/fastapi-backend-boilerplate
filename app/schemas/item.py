from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Human-friendly name of the item", examples=["Sample", "Gadget"]
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Optional details about the item", examples=["Some details", "Limited edition"]
    )


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="New name for the item", examples=["Updated name"]
    )
    description: Optional[str] = Field(
        None, max_length=500, description="New description for the item", examples=["Updated description"]
    )


class Item(ItemBase):
    id: int

    # Pydantic v2 configuration
    model_config = ConfigDict(from_attributes=True)
