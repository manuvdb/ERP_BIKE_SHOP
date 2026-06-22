from sqlalchemy.orm import Session
from controllers import ClientController

class ClientRouter:

    def __init__(self):
        self.controller = ClientController()

    #Simule : POST /clients
    def post_clients(self, session: Session, payload: dict) -> str:
        return self.controller.create_client(session, payload) 
    
    # Simule : GET /clients/{client_id}
    def get_client(self, session: Session, client_id: int) -> str:
        return self.controller.get_client(session, client_id)

    # Simule : GET /clients?skip=&limit=
    def get_clients(self, session: Session, skip: int = 0, limit: int = 100) -> str:
        return self.controller.list_clients(session, skip=skip, limit=limit)

    # Simule : PATCH /clients/{client_id}
    def patch_client(self, session: Session, client_id: int, payload: dict) -> str:
        return self.controller.update_client(session, client_id, payload)

    # Simule : DELETE /clients/{client_id}
    def delete_client(self, session: Session, client_id: int) -> str:
        return self.controller.delete_client(session, client_id)
