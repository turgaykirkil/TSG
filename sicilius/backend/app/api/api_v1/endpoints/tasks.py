from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.task import AppTask
from app.models.b2b_customer import B2BCustomer
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut

router = APIRouter()

@router.get("/", response_model=List[TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    customer_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = db.query(AppTask)
    if status:
        query = query.filter(AppTask.status == status)
    if priority:
        query = query.filter(AppTask.priority == priority)
    if customer_id:
        query = query.filter(AppTask.customer_id == customer_id)
    
    tasks = query.order_by(AppTask.due_date.asc().nullslast()).offset(skip).limit(limit).all()
    
    res = []
    for task in tasks:
        cust_name = ""
        if task.customer_id:
            cust = db.query(B2BCustomer).filter(B2BCustomer.id == task.customer_id).first()
            if cust:
                cust_name = cust.company_name or cust.title
        
        assignee_name = ""
        if task.assigned_to:
            user = db.query(User).filter(User.id == task.assigned_to).first()
            if user:
                assignee_name = user.full_name or user.email
        
        item = TaskOut(
            id=task.id,
            title=task.title,
            description=task.description or "",
            due_date=task.due_date,
            priority=task.priority,
            status=task.status,
            progress=task.progress,
            customer_id=task.customer_id,
            assigned_to=task.assigned_to,
            checklist=task.checklist or [],
            customer_name=cust_name,
            assignee_name=assignee_name,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        res.append(item)
    return res

@router.post("/", response_model=TaskOut)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
) -> Any:
    task = AppTask(
        title=task_in.title,
        description=task_in.description,
        due_date=task_in.due_date,
        priority=task_in.priority,
        status=task_in.status,
        progress=task_in.progress,
        customer_id=task_in.customer_id,
        assigned_to=task_in.assigned_to,
        checklist=[c.model_dump() for c in (task_in.checklist or [])]
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    cust_name = ""
    if task.customer_id:
        cust = db.query(B2BCustomer).filter(B2BCustomer.id == task.customer_id).first()
        if cust:
            cust_name = cust.company_name or cust.title

    return TaskOut(
        id=task.id,
        title=task.title,
        description=task.description or "",
        due_date=task.due_date,
        priority=task.priority,
        status=task.status,
        progress=task.progress,
        customer_id=task.customer_id,
        assigned_to=task.assigned_to,
        checklist=task.checklist or [],
        customer_name=cust_name,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
) -> Any:
    task = db.query(AppTask).filter(AppTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    cust_name = ""
    if task.customer_id:
        cust = db.query(B2BCustomer).filter(B2BCustomer.id == task.customer_id).first()
        if cust:
            cust_name = cust.company_name or cust.title

    return TaskOut(
        id=task.id,
        title=task.title,
        description=task.description or "",
        due_date=task.due_date,
        priority=task.priority,
        status=task.status,
        progress=task.progress,
        customer_id=task.customer_id,
        assigned_to=task.assigned_to,
        checklist=task.checklist or [],
        customer_name=cust_name,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
) -> Any:
    task = db.query(AppTask).filter(AppTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_in.model_dump(exclude_unset=True)
    if "checklist" in update_data and update_data["checklist"] is not None:
        update_data["checklist"] = [c if isinstance(c, dict) else c.model_dump() for c in update_data["checklist"]]

    for field, val in update_data.items():
        setattr(task, field, val)

    db.add(task)
    db.commit()
    db.refresh(task)

    cust_name = ""
    if task.customer_id:
        cust = db.query(B2BCustomer).filter(B2BCustomer.id == task.customer_id).first()
        if cust:
            cust_name = cust.company_name or cust.title

    return TaskOut(
        id=task.id,
        title=task.title,
        description=task.description or "",
        due_date=task.due_date,
        priority=task.priority,
        status=task.status,
        progress=task.progress,
        customer_id=task.customer_id,
        assigned_to=task.assigned_to,
        checklist=task.checklist or [],
        customer_name=cust_name,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
) -> Any:
    task = db.query(AppTask).filter(AppTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "success", "message": "Task deleted"}
