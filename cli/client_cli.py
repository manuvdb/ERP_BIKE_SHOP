from sqlalchemy.orm import Session
from routers import ClientRouter

def run_client_menu(session: Session, router: ClientRouter):
    while True:
        print("\nGESTION DES CLIENTS")
        print("1. Creer un client")
        print("2. Voir un client par ID")
        print("3. Voir la liste des clients")
        print("4. Modifier un client")
        print("5. Supprimer un client")
        print("6. Retour au menu principal")
        
        choix = input("\nVotre choix (1-6) : ").strip()
        
        if choix == "1":
            print("\nSaisie POST /clients")
            payload = {
                "first_name": input("Prenom : "),
                "last_name": input("Nom : "),
                "phone": input("Telephone : "),
                "email": input("Email : ")
            }
            response = router.post_clients(session, payload=payload)
            print(f"\nResultat : {response}")
            
        elif choix == "2":
            print("\nSaisie GET /clients/{id}")
            try:
                client_id = int(input("Entrez l'ID du client : "))
                response = router.get_client(session, client_id=client_id)
                print(f"\nResultat : {response}")
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier valide pour l'ID.")    
        
        elif choix == "3":
            print("\nSaisie GET /clients")
            response = router.get_clients(session)
            print(f"\nResultat : {response}")
            
        elif choix == "4":
            print("\nSaisie PATCH /clients/{id}")
            try:
                client_id = int(input("ID du client a modifier : "))
                print("(Laissez vide et appuyez sur Entree si vous ne voulez pas changer le champ)")
                
                first_name = input("Nouveau prenom : ").strip() or None
                last_name = input("Nouveau nom : ").strip() or None
                phone = input("Nouveau telephone : ").strip() or None
                email = input("Nouveau email : ").strip() or None
                
                payload = {}
                if first_name: payload["first_name"] = first_name
                if last_name: payload["last_name"] = last_name
                if phone: payload["phone"] = phone
                if email: payload["email"] = email
                
                response = router.patch_client(session, client_id=client_id, payload=payload)
                print(f"\nResultat : {response}")
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier valide pour l'ID.")
                
        elif choix == "5":
            print("\nSaisie DELETE /clients/{id}")
            try:
                client_id = int(input("ID du client a supprimer : "))
                confirmer = input(f"Etes-vous sur de vouloir supprimer le client {client_id} ? (oui/non) : ").strip().lower()
                if confirmer == "oui":
                    response = router.delete_client(session, client_id=client_id)
                    print(f"\nResultat : {response}")
                else:
                    print("Action annulee.")
            except ValueError:
                print("Erreur : Veuillez entrer un nombre entier valide pour l'ID.")
                
        elif choix == "6":
            break
        else:
            print("Option invalide. Veuillez choisir un nombre entre 1 et 6.")
