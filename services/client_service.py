from sqlalchemy.orm import Session
from models.client import Client
from repositories.client_repository import ClientRepository

class ClientService:

    def __init__(self):
        self.repository = ClientRepository()

    def create_client(
            self, 
            session: Session,
            first_name: str,
            last_name: str,
            phone: str,
            email: str 
            ) -> Client:
        
        if self.repository.get_by_email(session, email) is not None:
            raise ValueError(f"Un client avec l'email {email} existe déjà !")
        
        if self.repository.get_by_phone(session, phone) is not None:
            raise ValueError(f"Un client avec le numéro {phone} existe déjà !")
        
        client = Client(
            first_name= first_name.strip(),
            last_name=last_name.strip(),
            phone=phone.strip(),
            email=email.strip().lower(),
        )

        return self.repository.create(session, client)
    
    def get_client(self, session: Session, client_id: int) -> Client:
        client = self.repository.get_by_id(session, client_id)
        if client is None:
            raise ValueError(f"Aucun client avec l'id {client_id} n'existe !")
        return client
    
    def list_clients(self, session: Session, skip: int, limit: int) -> list[Client]:
        return self.repository.get_all(session, skip=skip, limit=limit)
    
    def update_client(
            self, 
            session: Session, 
            client_id: int,
            first_name: str,
            last_name: str,
            phone: str,
            email: str
            ) -> Client:
        
        client = self.get_client(session, client_id)

        if email is not None and email.strip().lower() != client.email:
            existing = self.repository.get_by_email(session, email.strip().lower())
            if existing is not None and existing.id != client_id:
                raise ValueError(f"Un client avec l'email {email} existe déjà !")
            client.email = email.strip().lower()
        
        if phone is not None and phone.strip() != client.phone:
            existing = self.repository.get_by_phone(session, phone.strip())
            if existing is not None and existing.id != client_id:
                raise ValueError(f"Un client avec le téléphone '{phone}' existe déjà.")
            client.phone = phone.strip()
        
        if first_name is not None:
            client.first_name = first_name.strip()
        
        if last_name is not None:
            client.last_name = last_name.strip()

        return self.repository.update(session, client)
    
    def delete_client(self, session: Session, client_id: int) -> None:
        client = self.get_client(session, client_id)
        self.repository.delete(session, client)
