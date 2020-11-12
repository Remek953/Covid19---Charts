import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import datetime
import requests
import random


#6 - Download newest file
def download_file():
    """Download the latest data from https://www.ecdc.europa.eu"""
    url = r'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
    print("Download the latest file. Please wait.")
    r = requests.get(url, allow_redirects=True)
    open('covid.csv', 'wb').write(r.content)
    print("Download Completed.")


def read_file():
    global df
    try:
        df = pd.read_csv('covid.csv',   parse_dates=True)
        df.rename(columns={'countriesAndTerritories': 'Country'}, inplace=True)
        df['dateRep'] = pd.to_datetime(df['dateRep'], dayfirst=True)

    except IOError:
        print("The file doesnt exist.")
        download_file()
        read_file()


#3 - List of the Countries
def list_of_countries():
    """List of the countries in the covid.csv"""
    countries = []
    for item in df['Country'].unique():
        countries.append(item.title())
    countries.sort()
    for country in countries:
        print(country)


################################################################
#1 - Global Info


def date_info():
    df_info = df.copy()
    df_info['dateRep'] = df_info['dateRep'].dt.date
    print("\n")
    print(f"Covid data is from {df_info['dateRep'].min()} to {df_info['dateRep'].max()}.")
    print(f"The total time of the covid pandemic data collected: {df_info['dateRep'].max() - df_info['dateRep'].min()}.")
    print(f"The total number of cases: {df_info['cases'].sum()}.")
    print(f"The total number of deaths: {df_info['deaths'].sum()}.\n")

def the_most_global():
    """The 5 countries with the highest total cases and deaths"""
    country_grp = df.groupby(['Country']).sum()
    cases = country_grp['cases'].nlargest(5)
    deaths = country_grp['deaths'].nlargest(5)
    print(f'\nThe 5 countries with the highest total cases:\n{cases.to_string(header=False)}')
    print(f'\nThe 5 countries with the highest total deaths:\n{deaths.to_string(header=False)}')


def the_most_global_daily():
    """The 5 countries with the highest daily number of cases and deaths in the World"""
    sub_df = df.copy()
    sub_df.set_index('dateRep', inplace=True)
    country_group = sub_df.groupby(['Country'])
    cases = country_group['cases'].nlargest(1).nlargest(5)
    deaths = country_group['deaths'].nlargest(1).nlargest(5)
    print(f'\nThe 5 countries with the highest number of cases in the World:\n{cases.to_string(header=False)}')
    print(f'\nThe 5 countries with the highest number of deaths in the World:\n{deaths.to_string(header=False)}')


def the_most_ratio():
    """The 5 countries of the highest total deaths/cases ratio in the World"""
    country_group = df.groupby(['Country']).sum()
    country_group['death/cases'] = (country_group['deaths'] / country_group['cases']) * 100
    ratio = country_group['death/cases'].nlargest(5).round(2).astype(str) + '%'
    print(f'\nThe 5 countries of the highest total deaths/cases ratio in the World:\n{ratio.to_string(header=False)}')

################################################################
#2 - Global Charts


def total_country_charts():
    """The 5 countries with the highest total cases and deaths"""
    fig, axs = plt.subplots(ncols=2, figsize=(10,8))

    grouped_values = df.groupby('Country').sum().reset_index()
    global_high_deaths = grouped_values.nlargest(5, ['cases']).sort_values('cases')

    global_deaths = sns.barplot(x='Country', y='cases', palette='YlOrRd', data=global_high_deaths , ax=axs[0],)

    for p in global_deaths.patches:
        global_deaths.annotate(format(p.get_height(), '.1f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               textcoords='offset points')
    axs[0].ticklabel_format(style='plain',  axis='y')
    axs[0].xaxis.get_majorticklabels()[0].set_y(-.03)
    axs[0].xaxis.get_majorticklabels()[2].set_y(-.03)
    axs[0].xaxis.get_majorticklabels()[4].set_y(-.03)

    axs[0].set_xlabel('Countries', size=14)
    axs[0].set_ylabel('Number of cases', size=14)
    axs[0].grid(axis="y",linestyle='dashed', color='w')
    axs[0].set_title("The 5 countries with the highest total cases", size=12)

    global_high_cases = grouped_values.nlargest(5, ['deaths']).sort_values('deaths')
    global_cases = sns.barplot(x='Country', y='deaths', palette='CMRmap_r', data=global_high_cases, ax=axs[1])
    for p in global_cases.patches:
        global_cases.annotate(format(p.get_height(), '.1f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               textcoords='offset points')

    axs[1].set_xlabel('Countries', size=14)

    axs[1].xaxis.get_majorticklabels()[0].set_y(-.03)
    axs[1].xaxis.get_majorticklabels()[2].set_y(-.03)
    axs[1].xaxis.get_majorticklabels()[4].set_y(-.03)

    axs[1].set_ylabel('Number of deaths', size=14)
    axs[1].set_title("The 5 countries with the highest total deaths", size=12)
    axs[1].grid(axis="y",linestyle='dashed', color='w')

    plt.tight_layout()
    plt.show()


def total_numbers_charts():
    """The total number of cases and deaths over months"""
    groupedmonths = df.groupby(df['dateRep'].dt.to_period('M')).sum()
    groupedmonths = groupedmonths.resample('M').asfreq().fillna(0)
    groupedmonths['dateRep']=groupedmonths.index

    fig, axs = plt.subplots(ncols=2, figsize=(10, 8))
    global_cases = sns.barplot(x='dateRep', y='cases', palette='YlOrRd', data=groupedmonths, ax=axs[0])

    for p in global_cases.patches:
        global_cases.annotate(format(p.get_height(), '.1f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               size=8,
                               textcoords='offset points')

    axs[0].ticklabel_format(style='plain', axis='y')
    axs[0].set_xlabel('Date', size=14)
    axs[0].set_ylabel('Number of cases', size=14)
    axs[0].grid(axis="y",linestyle='dashed', color='w')
    axs[0].set_title("The total number of cases over months", size=12)

    global_deaths = sns.barplot(x='dateRep', y='deaths', palette='PuBuGn', data=groupedmonths, ax=axs[1])

    for p in global_deaths.patches:
        global_deaths.annotate(format(p.get_height(), '.1f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               size=8,
                               textcoords='offset points')

    axs[1].set_xlabel('Date', size=14)
    axs[1].set_ylabel('Number of deaths', size=14)
    axs[1].grid(axis="y", linestyle='dashed', color='w')
    axs[1].set_title("The total number of deaths over months", size=12)

    for label in axs[0].get_xmajorticklabels() + axs[1].get_xmajorticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")

    plt.tight_layout()
    plt.show()


def cases_deaths_charts():
    """The total number of cases and deaths over months in one chart"""
    pd.plotting.register_matplotlib_converters()
    groupedmonths = df.groupby(df['dateRep'].dt.to_period('M')).sum()
    groupedmonths = groupedmonths.resample('M').asfreq().fillna(0)
    groupedmonths['dateRep']=groupedmonths.index

    fig, ax1 = plt.subplots(figsize=(10, 8))

    global_cases = sns.barplot(x='dateRep', y='cases', palette='CMRmap_r', data=groupedmonths, ax=ax1)

    for p in global_cases.patches:
        global_cases.annotate(format(p.get_height(), '.1f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               size=8,
                               textcoords='offset points')

    ax1.ticklabel_format(style='plain', axis='y')
    ax1.xaxis.set_tick_params(rotation=45,)
    ax1.set_xlabel('Date', size=14)
    ax1.set_ylabel('Number of cases', size=14, color='gray')
    ax1.grid(axis="y",linestyle='dashed', color='w')
    ax1.set_title("The total number of cases and deaths over months", size=16)

    ax2 = ax1.twinx()
    color = 'tab:red'

    ax2 = sns.lineplot(x=groupedmonths['dateRep'].dt.to_timestamp('s').dt.strftime('%Y-%m'), y='deaths',
                       data=groupedmonths, sort=False, color=color,  marker='o', ax=ax2)
    ax2.set_ylabel('Number of deaths ', fontsize=14, color=color)
    ax2.tick_params(axis='y', color=color)
    plt.show()


def random_10():
    """10 random countries with total number of cases and deaths over months"""
    countries = []
    for item in df['Country'].unique():
        countries.append(item.title())

    random_countries = random.sample(countries, 10)

    newDF = pd.DataFrame()  # creates a new dataframe that's empty

    for random_country in random_countries:
        pd.plotting.register_matplotlib_converters()
        country_name = (df['Country'] == random_country)
        country = df.loc[country_name]

        groupedmonths = country.groupby(country['dateRep'].dt.to_period('M')).sum()
        groupedmonths = groupedmonths.resample('M').asfreq().fillna(0)
        groupedmonths['dateRep'] = groupedmonths.index
        groupedmonths['Country'] = random_country
        newDF = newDF.append(groupedmonths, ignore_index=True)

    newDF['dateRep'] = newDF['dateRep'].astype(str)
    newDF['dateRep'] = pd.to_datetime(newDF['dateRep'])
    newDF = newDF.sort_values(by=['Country'])

    fig, axs = plt.subplots(ncols=2, figsize=(10, 8))
    global_cases = sns.lineplot(x='dateRep', y='cases', palette='bright', data=newDF, hue='Country', marker='o', ax=axs[0])

    from matplotlib import dates
    axs[0].ticklabel_format(style='plain', axis='y')
    axs[0].set_xlabel('Date', size=14)
    axs[0].set_ylabel('Number of cases', size=14)
    axs[0].grid(axis="y",linestyle='dashed', color='b')
    axs[0].grid(axis="x", linestyle='dashed', color='gray')
    axs[0].set_title("10 random countries with total number of cases over months", size=10)
    axs[0].set(xticks=newDF.dateRep.values)
    axs[0].xaxis.set_major_formatter(dates.DateFormatter("%b-%Y"))

    global_deaths = sns.lineplot(x='dateRep', y='deaths', palette='bright', data=newDF, hue='Country', marker='o', ax=axs[1])

    axs[1].set_xlabel('Date', size=14)
    axs[1].set_ylabel('Number of deaths', size=14)
    axs[1].grid(axis="y", linestyle='dashed', color='b')
    axs[1].grid(axis="x", linestyle='dashed', color='gray')
    axs[1].set_title("10 random countries with total number of deaths over months", size=10)
    axs[1].set(xticks=newDF.dateRep.values)
    axs[1].xaxis.set_major_formatter(dates.DateFormatter("%b-%Y"))


    for label in axs[0].get_xmajorticklabels() + axs[1].get_xmajorticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")

    plt.tight_layout()
    plt.show()


################################################################
#4 - Choose Country - Info


def check_country():
    name = str(input("Please enter country name: "))
    countries = []
    for item in df['Country'].unique():
        countries.append(item.title())

    while name.title() not in countries:
        if name.lower() == 'x':
            break
        print("Wrong.")
        name = input("Please enter valid country name or enter 'x' to exit.")
    return name.title()


def the_most_country(country_name):
    """Total number of cases and deaths for the selected country"""
    country_grp = df.groupby(['Country']).sum()
    cases = country_grp.loc[country_name]['cases'].astype(int).astype(str)
    deaths = country_grp.loc[country_name]['deaths'].astype(int).astype(str)
    print(f'{country_name} has total {cases} cases.')
    print(f'{country_name} has total {deaths} deaths.')


def the_most_country_daily(country_name):
    """The 5 days with the highest number of cases and deaths for the selected country"""
    df.set_index('dateRep', inplace=True)
    name = (df['Country'] == country_name)
    cases = df.loc[name]['cases'].nlargest(5)
    deaths = df.loc[name]['deaths'].nlargest(5)
    print(f'\nThe 5 days with the highest number of cases in the {country_name}:\n{cases.to_string(header=False)}')
    print(f'\nThe 5 days with the highest number of deaths in the {country_name}:\n{deaths.to_string(header=False)}')


def the_country_ratio(country_name):
    """The deaths/cases ratio for the seleceted country"""
    country_group = df.groupby(['Country']).sum()
    country_group['death/cases'] = (country_group['deaths'] / country_group['cases']) * 100
    ratio = country_group.loc[country_name]['death/cases'].round(2).astype(str) + '%'
    print(f'\nThe deaths/cases ratio in the {country_name} is {ratio}.')


################################################################
#5 - Choose Country - Charts


def check_country_charts():
    name = str(input("Please enter country name: "))
    countries = []
    for item in df['Country'].unique():
        countries.append(item.title())

    while name.title() not in countries:
        if name.lower() == 'x':
            print('success')
            break
        print("Wrong.")
        name = input("Please enter valid country name or enter 'x' to exit.")
    return name.title()


def the_most_country_charts(country_name_charts):
    """The total number of cases and deaths in selected country"""
    country_name = (df['Country'] == country_name_charts)
    country = df.loc[country_name]

    groupedmonths = country.groupby(country['dateRep'].dt.to_period('M')).sum()
    groupedmonths = groupedmonths.resample('M').asfreq().fillna(0)
    groupedmonths['dateRep'] = groupedmonths.index

    fig, axs = plt.subplots(ncols=2, figsize=(10, 8))
    global_cases = sns.barplot(x='dateRep', y='cases', palette='YlOrRd', data=groupedmonths, ax=axs[0])

    for p in global_cases.patches:
        global_cases.annotate(format(p.get_height(), '.1f'),
                              (p.get_x() + p.get_width() / 2., p.get_height()),
                              ha='center', va='center',
                              xytext=(0, 5),
                              size=8,
                              textcoords='offset points')

    axs[0].ticklabel_format(style='plain', axis='y')
    axs[0].set_xlabel('Date', size=14)
    axs[0].set_ylabel('Number of cases', size=14)
    axs[0].grid(axis="y", linestyle='dashed', color='w')
    axs[0].set_title(f"The total number of cases in {country_name_charts}", size=12)

    global_deaths = sns.barplot(x='dateRep', y='deaths', palette='PuBuGn', data=groupedmonths, ax=axs[1])

    for p in global_deaths.patches:
        global_deaths.annotate(format(p.get_height(), '1.0f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               size=8,
                               textcoords='offset points')

    axs[1].set_xlabel('Date', size=14)
    axs[1].set_ylabel('Number of deaths', size=14)
    axs[1].grid(axis="y", linestyle='dashed', color='w')
    axs[1].set_title(f"The total number of deaths in {country_name_charts}", size=12)

    for label in axs[0].get_xmajorticklabels() + axs[1].get_xmajorticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")

    plt.tight_layout()
    plt.show()


def cases_deaths_country_charts(country_name_charts):
    """The total number of cases and deaths in one chart for the selected country"""
    pd.plotting.register_matplotlib_converters()
    country_name = (df['Country'] == country_name_charts)
    country = df.loc[country_name]

    groupedmonths = country.groupby(country['dateRep'].dt.to_period('M')).sum()
    groupedmonths = groupedmonths.resample('M').asfreq().fillna(0)
    groupedmonths['dateRep'] = groupedmonths.index

    fig, ax1 = plt.subplots(figsize=(10, 8))

    global_cases = sns.barplot(x='dateRep', y='cases', palette='CMRmap_r', data=groupedmonths, ax=ax1)

    for p in global_cases.patches:
        global_cases.annotate(format(p.get_height(), '1.0f'),
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center',
                               xytext=(0, 5),
                               size=8,
                               textcoords='offset points')

    ax1.ticklabel_format(style='plain', axis='y')
    ax1.xaxis.set_tick_params(rotation=45,)
    ax1.set_xlabel('Date', size=14)
    ax1.set_ylabel('Number of cases', size=14, color='gray')
    ax1.grid(axis="y",linestyle='dashed', color='w')
    ax1.set_title(f"The total number of cases and deaths in {country_name_charts}", size=16)

    ax2 = ax1.twinx()
    color = 'tab:red'

    ax2 = sns.lineplot(x=groupedmonths['dateRep'].dt.to_timestamp('s').dt.strftime('%Y-%m'), y='deaths',
                       data=groupedmonths, sort=False, color=color,  marker='o', ax=ax2)
    ax2.set_ylabel('Number of deaths ', fontsize=14, color=color)
    ax2.tick_params(axis='y', color=color)
    plt.show()


def last_14_days(country_name_charts):
    """Total number of cases and deaths for the selected country in the last 14 days"""
    pd.plotting.register_matplotlib_converters()
    country_name = (df['Country'] == country_name_charts)
    country = df.loc[country_name]

    groupeddays = country.groupby(country['dateRep'].dt.to_period('D')).sum()
    groupeddays = groupeddays.resample('D').asfreq().fillna(0)
    groupeddays['dateRep'] = groupeddays.index
    days_14 = datetime.datetime.now() - pd.to_timedelta("14day")
    result = groupeddays[groupeddays.dateRep > days_14.strftime('%d/%m/%y')]

    fig, axs = plt.subplots(ncols=2, figsize=(10, 8))
    global_cases = sns.barplot(x='cases', y='dateRep', palette='YlOrRd', data=result, ax=axs[0])

    for p in global_cases.patches:
        width = p.get_width()  # get bar length
        global_cases.text(width + 1,  # set the text at 1 unit right of the bar
                p.get_y() + p.get_height() / 2,  # get Y coordinate + X coordinate / 2
                '{:1.0f}'.format(width),  # set variable to display, 2 decimals
                ha='left',  # horizontal alignment
                va='center') # vertical alignment

    axs[0].set_xlabel('Number of cases', size=14)
    axs[0].set_ylabel('', size=14)
    axs[0].grid(axis="x", linestyle='dashed', color='w')
    axs[0].set_title(f"The total number of cases in {country_name_charts} in the last 14 days", size=10)

    global_deaths = sns.barplot(x='deaths', y='dateRep', palette='PuBuGn', data=result, ax=axs[1])

    for p in global_deaths.patches:
        width = p.get_width()  # get bar length
        global_deaths.text(width + 1,  # set the text at 1 unit right of the bar
                p.get_y() + p.get_height() / 2,  # get Y coordinate + X coordinate / 2
                '{:1.0f}'.format(width),  # set variable to display, 2 decimals
                ha='left',  # horizontal alignment
                va='center') # vertical alignment

    axs[1].set_xlabel('Number of deaths', size=14)
    axs[1].set_ylabel('', size=14)
    axs[1].grid(axis="x", linestyle='dashed', color='w')
    axs[1].set_title(f"The total number of deaths in {country_name_charts} in the last 14 days", size=10)

    for label in axs[0].get_xmajorticklabels() + axs[1].get_xmajorticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")

    plt.tight_layout()
    plt.show()

################################################################
