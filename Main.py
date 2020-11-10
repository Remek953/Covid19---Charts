import sys

def menu():
    choice = None

    while choice != '8':
        print("""

MENU:

1 - Global Info

2 - Global Charts

3 - List of the Countries

4 - Choose Country - Info

5 - Choose Country - Charts

6 - Download newest file   

7 - About Program   

8 - Exit       

         """)
        choice = input("Choice: ")
        print()


        if choice == "1" or choice.lower() == "global info":

            return main_menu()


        elif choice == "2" or choice.lower() == "global charts":

            return main_menu()


        elif choice == "3" or choice.lower() == "list of the countries":
            about_me()
            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return main_menu()

        # Exit
        elif choice == "8":
            print("Goodbye!")
            time.sleep(1)
            sys.exit()

        # Unknown choice
        else:
            print(f"Sorry, but {choice} isn't a valid choice.")


if __name__ == "__main__":
    menu()
