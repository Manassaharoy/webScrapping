from bs4 import BeautifulSoup
import base64
import csv

htmlfilename = input("Whats the HTML file name? (no need to put .html)  ")
saveCSVas = input("CSV file name  ")

with open(f'{htmlfilename}.html', encoding="utf8") as f:
    html = f.read()

# Create BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")
people = []
# Find all the li tags with class "contact-info"
contact_list = soup.find_all("li", class_="ResultList-item")

for contact in contact_list:
    try:
        name = contact.find('h3', {'class': 'Teaser-title'}).text.strip().replace('\n', ' ').strip()

        
        buttons = contact.find('button', {'data-obfuscated': 'true'})
        email_address = base64.b64decode(buttons.get('data-adr-val')).decode('utf-8')

        title = contact.find('div', {'class': 'Teaser-titles'}).text.strip().replace('\n', ' ').strip()
        
        address = contact.find('address', {'class': 'c-address'}).text.strip().replace('\n', ' ').strip()

        # branchPhn = contact.find('span', {'class':'c-phone-number-span'}).text.strip().replace('\n', ' ').strip()
        
        phoneNumberList = contact.find_all("div", class_="Teaser-phone")
        phoneNums = []
        if phoneNumberList:
            for phone in phoneNumberList:
                x = phone.find('span', {'class':'c-phone-number-span'}).text.strip().replace('\n', ' ').strip()
                phoneNums.append(x)
        else:
            phoneNums = None

        # people.append({"fullname":name,"title":title,"email":email_address, "address":address,"branchPhn":phoneNums[0], "directPhn":phoneNums[1]})

        people.append({"fullname":name,"title":title,"email":email_address, "address":address,"branchPhn":phoneNums[0] if phoneNums else None, "directPhn":phoneNums[1] if phoneNums and len(phoneNums) > 1 else None})

    
    except AttributeError:
        print("Error: Skipping current contact due to missing element")
        continue

# print(people)
with open(f'{saveCSVas}.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Full Name", "Title", "Email", "Address", "branch Phone", "Direct Phone"])
    for person in people:
        writer.writerow([person["fullname"], person["title"], person["email"], person["address"], person["directPhn"], person["branchPhn"]])

