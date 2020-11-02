import pandas as pd
from matplotlib import pyplot as plt


def read_file():
    global df
    df = pd.read_csv('covid.csv')
    pd.set_option('display.max_columns', 85)
    pd.set_option('display.max_rows', 85)
    df.rename(columns={'countriesAndTerritories': 'Country'}, inplace=True)
    df['dateRep'] = pd.to_datetime(df['dateRep'])


def date_info():
    df['dateRep'] = df['dateRep'].dt.date
    print("\n")
    print(f"Covid data is from {df['dateRep'].min()} to {df['dateRep'].max()}.")
    print(f"The total time of the covid pandemic data collected: {df['dateRep'].max() - df['dateRep'].min()}.\n")


def the_most_global():
    country_grp = df.groupby(['Country']).sum()
    cases = country_grp['cases'].nlargest(5)
    deaths = country_grp['deaths'].nlargest(5)
    print(f'\nThe 5 countries with the highest total cases:\n{cases.to_string(header=False)}')
    print(f'\nThe 5 countries with the highest total deaths:\n{deaths.to_string(header=False)}')


def the_most_global_daily():
    sub_df = df.copy()
    sub_df.set_index('dateRep', inplace=True)
    country_group = sub_df.groupby(['Country'])
    cases = country_group['cases'].nlargest(1).nlargest(5)
    deaths = country_group['deaths'].nlargest(1).nlargest(5)
    print(f'\nThe 5 countries of the most daily cases in the World:\n{cases.to_string(header=False)}')
    print(f'\nThe 5 countries of the most daily deaths in the World:\n{deaths.to_string(header=False)}')


def the_most_ratio():
    country_group = df.groupby(['Country']).sum()
    country_group['death/cases'] = (country_group['deaths'] / country_group['cases']) * 100
    ratio = country_group['death/cases'].nlargest(5).round(2).astype(str) + '%'
    print(f'\nThe 5 countries of the highest total deaths/cases ratio in the World:\n{ratio.to_string(header=False)}')


"""
read_file()
date_info()
the_most_global()
the_most_global_daily()
the_most_ratio()
"""
###################################


def check_country():
    name = str(input("Please enter country name: "))
    countries = []
    for item in df['Country'].unique():
        countries.append(item.title())

    while name.title() not in countries or name.title() != 'x':
        print("Wrong.")
        name = input("Please enter valid country name or enter 'x' to exit.")
    if name.lower() == 'x':
        print('success')

    return name.title()


def the_most_country(country_name):
    country_grp = df.groupby(['Country']).sum()
    cases = country_grp.loc[country_name]['cases'].astype(int).astype(str)
    deaths = country_grp.loc[country_name]['deaths'].astype(int).astype(str)
    print(f'{country_name} has total {cases} cases.')
    print(f'{country_name} has total {deaths} deaths.')


def the_most_country_daily(country_name):
    df.set_index('dateRep', inplace=True)
    name = (df['Country'] == country_name)
    cases = df.loc[name]['cases'].nlargest(5)
    deaths = df.loc[name]['deaths'].nlargest(5)
    print(f'\nThe 5 days of the most daily cases in the {country_name}:\n{cases.to_string(header=False)}')
    print(f'\nThe 5 days of the most daily deaths in the {country_name}:\n{deaths.to_string(header=False)}')


def the_country_ratio(country_name):
    country_group = df.groupby(['Country']).sum()
    country_group['death/cases'] = (country_group['deaths'] / country_group['cases']) * 100
    ratio = country_group.loc[country_name]['death/cases'].round(2).astype(str) + '%'
    print(f'\nThe deaths/cases ratio in the {country_name} is {ratio}.')

read_file()
country_name = 'Poland'
the_most_country(country_name)
the_most_country_daily(country_name)
the_country_ratio(country_name)


###################################

read_file()


pol = (df['Country'] == 'Poland')
dfpol = df.loc[pol]

dates = dfpol['dateRep'][::-1]
cases = dfpol['cases'][::-1]
#
deaths = dfpol['deaths'][::-1]
#
sum_of_c_d = [cases.sum(), deaths.sum()]


def dates_cases(dates, cases):
    plt.plot(dates, cases)

    plt.title("Number of cases", fontsize=24)
    plt.xlabel("Date")
    plt.ylabel("Cases")

    plt.show()



def dates_cases(dates, deaths):
    plt.plot(dates, deaths)

    plt.title("Square Numbers", fontsize=24)
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.show()


def cases_deaths(sum_of_c_d):

    explode = [0, 0.1]

    plt.pie(sum_of_c_d, explode = explode, shadow=True, startangle=0, autopct='%1.1f%%',
        wedgeprops={'edgecolor': 'black'})

    plt.title('Cases/Deaths ratio in Poland')
    plt.tight_layout()
    plt.savefig('plot3.png')
    plt.show()


def charts_of_2(dates, cases, deaths):
    plt.bar(dates, cases,
         color = 'y', label='Cases')
    plt.plot(dates, deaths)

    plt.xlabel('Ages')
    plt.ylabel('Median Salary (USD')
    plt.title('Median Salary (USD) by Age')

    plt.legend()
    plt.tight_layout()
    plt.show()





