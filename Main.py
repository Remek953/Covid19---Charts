from charts import *
import sys
import time


def menu():
    read_file()
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
            date_info()
            the_most_global()
            the_most_global_daily()
            the_most_ratio()

            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return menu()

        elif choice == "2" or choice.lower() == "global charts":
            total_country_charts()
            total_numbers_charts()
            cases_deaths_charts()
            random_10()

            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return menu()

        elif choice == "3" or choice.lower() == "list of the countries" or choice.lower() == "list":
            list_of_countries()

            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return menu()

        elif choice == "4" or choice.lower() == "choose country - info":
            country_name = check_country()
            the_most_country(country_name)
            the_most_country_daily(country_name)
            the_country_ratio(country_name)

            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return menu()

        elif choice == "5" or choice.lower() == "choose country - charts":
            country_name_charts = check_country_charts()
            last_14_days(country_name_charts)
            the_most_country_charts(country_name_charts)
            cases_deaths_country_charts(country_name_charts)

            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return menu()

        elif choice == "6" or choice.lower() == "download newest file":
            download_file()
            time.sleep(1)
            return menu()

        elif choice == "7" or choice.lower() == "about program":
            print("""Project in Python that displays the statistics and graphs of the coronavirus for the countries and worldwide. 
I used the pandas, matplotlib and seaborn library to show data.
In this project you can download the latest data from https://www.ecdc.europa.eu and check the statistics and graphs about:
- Total number of cases and deaths worldwide and in selected countries,
- 5 countries with the highest number of cases and deaths in the world,
- 10 random countries with total number of cases and deaths over months,
- 5 countries with the highest death / case rates in the world,
- Total number of cases and deaths in months in the world and in selected countries,
- The total number of cases and deaths in the selected countries in the last 14 days.""")

            print('\n====press KEY and ENTER to return====')
            key = input('>>>')
            if key != "Z":
                return menu()

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


