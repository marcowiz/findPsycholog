import requests
import re

base_url = 'https://www.therapievermittlung.ch'
search_url = f'{base_url}/therapeutinnen-suche/members-search/suche/list/'
email_pattern = r'<a target="\_blank" href="mailto:(.*?)">'

response = requests.get(search_url)
response.raise_for_status()

links_pattern = r'<a class="card-image" href="(.*?)">'
links = re.findall(links_pattern, response.text)
print(len(links))
for link in links[:10]:
    full_link = f'{base_url}{link}'
    sub_response = requests.get(full_link)
    sub_response.raise_for_status()
    
    email_match = re.search(email_pattern, sub_response.text)
    if email_match:
        email = email_match.group(1)
        print(email)
    else:
        print(f"No email found for link: {full_link}")
