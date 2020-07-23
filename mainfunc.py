import re
import os
import csv
import email
import smtplib
import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
from email.mime.text import MIMEText
from email.message import EmailMessage





# With this function I replace *|FNAME|* with the name I have in the .csv file
def rep_data(name, date, file_html):

    with open(file_html, 'r') as f:
        webpage = f.read()

    soup = BeautifulSoup(webpage, "html.parser")
    target = soup.find_all(text = re.compile(r'FNAME'))

    for v in target:

        v.replace_with(v.replace('*|FNAME|*', name))
        # Replace html_file.html with the  html file
        html_file= open("html_file.html","w")
        html_file.write(soup.prettify())
        html_file.close()


# Function for sendin the email
def send_email(to, file, sub):
    # The message
    message = EmailMessage()
    # Email subject
    message['subject'] = sub
    # Who have send the email
    # Replace ........@gmail.com with the email your email address
    # If you don't use gmail, you have to replace the smtp and the port below
    message['from'] = os.environ.get('........@gmail.com')
    # Who recive the mail
    message['to'] = to
    # Content of email
    message.set_content(' ')
    # Open read and attached the html file to the email
    html_message = open(file).read()
    message.add_alternative(html_message,subtype='html')
    # Send email
    # Replace smtp.gmail.com and the port (465) if you havent a gmail account
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        # Login to the mail service
        # Insert your email and password for login
        smtp.login('.....@gmail.com','Password')
        # Send message
        smtp.send_message(message)
        smtp.quit()





# Counters
tot_mail = 0
mail_counter = 0
mail_not_send = 0

# Replace with the csv file containing the names and addresses of the people to be contacted.
# A copy of the file is present in the directori to show the position in which to insert them
with open('Csv_file_name.csv', 'r') as csvfile:

    #Extract data from .csv
    reader = csv.reader(csvfile, delimiter=";")
    next(reader)

    for index in reader:

        name = str(index[0])
        surname = str(index[1])
        mail_index = str(index[2])

        try:
            # This creates the file to be forwarded called azzamov contains the name of the person who replaces the writing *|FNAME|*
            # that you have inserted in the html files where you want the person's name to be put, and replaces the date
            # indicated by you in the point with *|DATE|* with the date you entered
            rep_data(name, "25-05-2020", "Comunicazioni urgenti.html")

            # Chouse the mail object you want
            send_email(mail_index, "html_file.html", "Mail object")
            mail_counter += 1
            tot_mail += 1
            print("Mail send to: " + str(surname) + " " + str(name) + " mail N: " + str(tot_mail))
        except:
            mail_not_send += 1
            tot_mail += 1
            print()
            print()
            print()
            print("MAIL NOT SEND TO: " + str(surname) + " " + str(name) + " MAIL N: " + str(tot_mail))
            print()
            print()
            print()

print()
print("I have send " + str(mail_counter) + " mail")
print("I haven't send " + str(mail_not_send) + " mail")
