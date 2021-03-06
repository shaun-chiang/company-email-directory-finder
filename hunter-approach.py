import csv

import requests

# From http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-whilst-preserving-order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

api_key = 'b718e5712460d4b134952eb9d8c8438ec2a8e641'

email_list = []

with open('test.txt', 'r') as openfile:
    for line in openfile:
        r = requests.get("https://api.hunter.io/v2/domain-search",params={"company":line, "api_key":api_key})
        for d in r.json()["data"]["emails"]:
            email_list.append([d['value'],d['first_name'],d['last_name'],d['position']])

        r = requests.get("https://api.hunter.io/v2/domain-search", params={"company": line + " Singapore", "api_key": api_key})
        for d in r.json()["data"]["emails"]:
            email_list.append([d['value'],d['first_name'],d['last_name'],d['position']])



with open('output.csv', 'w') as writefile:
    csvwriter = csv.writer(writefile, dialect='excel')
    csvwriter.writerow(['Email', 'First Name', "Last Name", "Position"])
    for email in email_list:
        csvwriter.writerow(email)

# Eliminate duplicate rows and cleanup
from more_itertools import unique_everseen

with open('output.csv','r') as f, open('output_clean.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))