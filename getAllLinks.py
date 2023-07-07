import requests
from bs4 import BeautifulSoup
import re
import pyperclip

def get_links():
    url = "https://www.therapievermittlung.ch/therapeutinnen-suche/members-search/suche"
    url = "https://www.therapievermittlung.ch/therapeutinnen-suche/members-search/suche/list/"

    # The form data to be submitted$
    auswahl = 12
    auswahl = input("Bitte die Nr. eingeben für den Suchort, 12 = Züri 0 = Alle: ")
    form_data = {
        "tx_members_search[region]": auswahl,
    }

    # Submit the form and fetch the results page
    response = requests.post(url, data=form_data)

    # simulate pressing the search button
    #response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    office_detail_divs = soup.find_all("div", class_="officeDetail")
    links = []

    for div in office_detail_divs:
        url = div["data-url"]
        link = f"https://www.therapievermittlung.ch{url}"
        links.append(link)

    return links

def get_emails2(urls):
    email_pattern = r'href="\s*mailto:(.*?)\s*"'
    email_addresses = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        email_links = soup.find_all("a", href=re.compile(r"mailto:"))

        for link in email_links:
            email = re.search(email_pattern, str(link)).group(1)
            email_addresses.append(email)

    return email_addresses

def get_emails(links):
    email_pattern = r'mailto:(\S+)'
    emails = []
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        email_links = soup.find_all("a", href=re.compile(r"mailto:"))
        for link in email_links:
            email_match = re.search(email_pattern, str(link))
            if email_match:
                email = email_match.group(1)
                email = email.replace('\\"', "")
                email = email.replace("'", "")
                emails.append(email)
    return emails


links = get_links()
print(len(links))
emails = get_emails(links)

for email in emails:
    print(email)
    email_string = '\n'.join(emails)
pyperclip.copy(email_string)
print("Email addresses copied to clipboard /zwischenablage.")
input("Press Enter to exit...")