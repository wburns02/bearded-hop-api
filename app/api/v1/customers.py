from fastapi import APIRouter, Query
from sqlalchemy import select
from uuid import UUID

from app.api.deps import DbSession, CurrentUser
from app.models.customer import Customer
from app.models.visit_record import VisitRecord
from app.models.customer_note import CustomerNote
from app.schemas.customers import CustomerCreate, CustomerUpdate, CustomerResponse
from app.exceptions import NotFoundError

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=list[CustomerResponse])
async def list_customers(
    db: DbSession,
    current_user: CurrentUser,
    search: str | None = Query(default=None),
):
    stmt = select(Customer)
    if search:
        term = f"%{search}%"
        stmt = stmt.where(
            Customer.first_name.ilike(term)
            | Customer.last_name.ilike(term)
            | Customer.email.ilike(term)
            | Customer.phone.ilike(term)
        )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{id}", response_model=CustomerResponse)
async def get_customer(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Customer).where(Customer.id == id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise NotFoundError("Customer")
    return customer


@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_customer(body: CustomerCreate, db: DbSession, current_user: CurrentUser):
    customer = Customer(**body.model_dump())
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer


@router.patch("/{id}", response_model=CustomerResponse)
async def update_customer(id: UUID, body: CustomerUpdate, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Customer).where(Customer.id == id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise NotFoundError("Customer")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    await db.commit()
    await db.refresh(customer)
    return customer


@router.delete("/{id}", status_code=204)
async def delete_customer(id: UUID, db: DbSession, current_user: CurrentUser):
    result = await db.execute(select(Customer).where(Customer.id == id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise NotFoundError("Customer")
    await db.delete(customer)
    await db.commit()


@router.get("/all-visits")
async def list_all_visits(db: DbSession, current_user: CurrentUser):
    """Return all visit records for all customers."""
    result = await db.execute(select(VisitRecord))
    return result.scalars().all()


@router.get("/all-notes")
async def list_all_notes(db: DbSession, current_user: CurrentUser):
    """Return all customer notes for all customers."""
    result = await db.execute(select(CustomerNote))
    return result.scalars().all()


@router.get("/{id}/visits")
async def list_customer_visits(id: UUID, db: DbSession, current_user: CurrentUser):
    # Ensure customer exists
    cust_result = await db.execute(select(Customer).where(Customer.id == id))
    if not cust_result.scalar_one_or_none():
        raise NotFoundError("Customer")
    result = await db.execute(select(VisitRecord).where(VisitRecord.customer_id == id))
    return result.scalars().all()


@router.get("/{id}/notes")
async def list_customer_notes(id: UUID, db: DbSession, current_user: CurrentUser):
    cust_result = await db.execute(select(Customer).where(Customer.id == id))
    if not cust_result.scalar_one_or_none():
        raise NotFoundError("Customer")
    result = await db.execute(select(CustomerNote).where(CustomerNote.customer_id == id))
    return result.scalars().all()


@router.post("/{id}/notes", status_code=201)
async def add_customer_note(
    id: UUID,
    body: dict,
    db: DbSession,
    current_user: CurrentUser,
):
    cust_result = await db.execute(select(Customer).where(Customer.id == id))
    if not cust_result.scalar_one_or_none():
        raise NotFoundError("Customer")
    note = CustomerNote(customer_id=id, **body)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note
