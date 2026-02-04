import diagnostic
import backup
import audit
import sys


def menu():

    while True:

        print("\n===== NTL SysToolbox =====")
        print("1 - Diagnostic système")
        print("2 - Sauvegarde WMS")
        print("3 - Audit obsolescence")
        print("4 - Quitter")

        choix = input("Choix : ")

        if choix == "1":
            diagnostic.run()

        elif choix == "2":
            backup.run()

        elif choix == "3":
            audit.run()

        elif choix == "4":
            print("Au revoir")
            sys.exit(0)

        else:
            print("Choix invalide")


if __name__ == "__main__":
    menu()
