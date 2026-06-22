from sqlalchemy.orm import Session
from services import ClientService

class ClientController:

    def __init__(self):
        self.service = ClientService()

    def create_client(self, session: Session, payload: dict) -> str:
        try:
            client = self.service.create_client(
                session,
                first_name=payload["first_name"],
                last_name=payload["last_name"],
                phone=payload["phone"],
                email=payload["email"],
            )
            session.commit()
            session.refresh(client)
            return f"Succès ! Le client {client.first_name} {client.last_name} a bien été créé avec l'ID {client.id}."
        except KeyError as e:
            session.rollback()
            return f"Champ manquant dans la requête : {e}"
        except Exception as e:
            session.rollback()
            return f"Erreur:  {e}"
    
    def get_client(self, session: Session, client_id: int) -> str:
        try:
            client = self.service.get_client(session, client_id)
            return f"Succès : Le client avec l'id {client_id} a bien été renvoyé !"
        except Exception as e:
            return f"Erreur : {e}"
    
    def list_clients(self, session: Session, skip: int=0, limit: int=50) -> str:
        clients = self.service.list_clients(session, skip=skip, limit=limit)
        return f"Succès : La liste de client a bien été renvoyée"
    
    def update_client(self, session: Session, client_id: int, payload: dict) -> str:
        try:
            client = self.service.update_client(
                session,
                client_id=client_id,
                first_name=payload.get("first_name"),
                last_name=payload.get("last_name"),
                phone=payload.get("phone"),
                email=payload.get("email"),
            )
            session.commit()
            session.refresh(client)
            return f"Succès ! Le client {client.first_name} {client.last_name} a bien été mis à jour."
        except Exception as e:
            session.rollback()
            return f"Erreur: {e}"
    
    def delete_client(self, session: Session, client_id: int) -> str:
        try:
            self.service.delete_client(session, client_id)
            session.commit()
            return f"Succès : Le client avec l'id {client_id} a bien été supprimé !"
        except Exception as e:
            session.rollback()
            return f"Erreur: {e}"