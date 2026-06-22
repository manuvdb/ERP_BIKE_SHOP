from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Client

class ClientRepository:

    def create(self, session: Session, client: Client) -> Client:
        session.add(client)
        session.flush()
        return client
    
    def get_by_email(self, session: Session, email: str) -> Client | None:
        stmt = select(Client).where(Client.email == email)
        return session.execute(stmt).scalar_one_or_none()
    
    def get_by_id(self, session: Session, client_id: int) -> Client | None:
        return session.get(Client, client_id)
    
    def get_by_phone(self, session: Session, phone: str) -> Client | None:
        stmt = select(Client).where(Client.phone == phone)
        return session.execute(stmt).scalar_one_or_none()
    
    def get_all(self, session: Session, skip: int, limit: int) -> list[Client]:
        stmt = select(Client).offset(skip).limit(limit)
        return list(session.execute(stmt).scalars().all())

    def update(self, session: Session, client: Client) -> Client:
        session.flush()
        return client
    
    def delete(self, session: Session, client: Client) -> None:
        session.delete(client)
        session.flush()