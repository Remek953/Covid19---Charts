import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('covid.csv')
pd.set_option('display.max_columns', 85)
pd.set_option('display.max_rows', 85)

pol = (df['countriesAndTerritories'] == 'Poland')
dfpol = df.loc[pol]

dates = dfpol['dateRep'][::-1]
cases = dfpol['cases'][::-1]
deaths = dfpol['deaths'][::-1]
sum_of_c_d = [cases.sum(), deaths.sum()]

def dates_cases(dates, cases):
    plt.plot(dates, cases)

    plt.title("Square Numbers", fontsize=24)
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

