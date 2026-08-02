from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ChecklistItemSchema(BaseModel):
    id: str
    title: str
    completed: bool = False

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"
    status: str = "todo"
    progress: int = 0
    customer_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None
    checklist: Optional[List[ChecklistItemSchema]] = []

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    progress: Optional[int] = None
    customer_id: Optional[UUID] = None
    assigned_to: Optional[UUID] = None
    checklist: Optional[List[ChecklistItemSchema]] = None

class TaskOut(TaskBase):
    id: UUID
    customer_name: Optional[str] = None
    assignee_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
