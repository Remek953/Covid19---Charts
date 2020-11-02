import requests

file_url = r'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'


def download_file(url):
    print("Downloading newest file. Please wait.")
    r = requests.get(url, allow_redirects=True)
    open('covid.csv', 'wb').write(r.content)
    print("Download Completed.")


download_file(file_url)
