import sys
from db.database import SessionLocal
from cli import run_client_menu
from routers import ClientRouter

def print_response(label: str, response: str) -> None:
    # Affiche la reponse renvoyee par le routeur.
    print(f"\n{label}")
    print(response)


def main():
    session = SessionLocal()
    routeur = ClientRouter()

    while True:
        print("\nATELIER VELO - MENU PRINCIPAL")
        print("1. Gerer les clients")
        print("2. Gerer les reparations velos (Bientot)")
        print("3. Quitter le programme")
        
        main_choice = input("\nOu voulez-vous aller ? (1-3) : ").strip()
        
        if main_choice == "1":
            run_client_menu(session, routeur)
        elif main_choice == "2":
            print("\nLe menu des reparations est en cours de developpement.")
        elif main_choice == "3":
            print("\nFermeture de la session")
            session.close()
            sys.exit()
        else:
            print("Option invalide. Veuillez choisir 1, 2 ou 3.")

if __name__ == "__main__":
    main()
