import sys

def menu():
    choice = None

    while choice != '4':
        print("""

MENU:
1 - Choose Country   

2 - Download newest file   

3 - About Program   

4 - Exit       

         """)
        choice = input("Choice: ")
        print()

        # NewGame
        if choice == "1":

            return main_menu()

        # Scores
        elif choice == "2":

            return main_menu()

        # About Me
        elif choice == "3":
            about_me()
            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return main_menu()

        # Exit
        elif choice == "4":
            print("Goodbye!")
            time.sleep(1)
            sys.exit()

        # Unknown choice
        else:
            print(f"Sorry, but {choice} isn't a valid choice.")


if __name__ == "__main__":
    menu()
