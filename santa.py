import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import random
import copy
import getpass

gmail_address = input("please provide your gmail address: ")
gmail_password = getpass.getpass("please provide your gmail password: ")

def isValid(pairings):
    for pair in pairings:
        if pair[0] == pair[1]:
            return False
        elif (pair[1]['name'] in pair[0]['exclude']):
            return False
    return True

def generateList(user_list):

    pairings = []

    gifter_list = copy.deepcopy(user_list)
    giftee_list = copy.deepcopy(user_list)

    random.shuffle(gifter_list)
    random.shuffle(giftee_list)
    
    while(len(giftee_list) > 0):
        gifter = gifter_list.pop()
        giftee = giftee_list.pop()
            
        pairings.append([gifter,giftee])
    return pairings            

def readInParticipants():
  with open('participants.json','r') as participants:
    data = (json.load(participants))
    return data

def email_handling(pair):
    gifter = pair[0]
    giftee = pair[1]
    
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()

    # Authentication
    s.login(gmail_address, gmail_password)
    
    
    # message to be sent 
    msg = MIMEMultipart('alternative')

    html = f"""
    <html>
    <head></head>
    <body>
        <h1>Merry Christmas %s!</h1>
        This year, your secret santa is %s!
        </p>
    </body>
    </html>""" % (giftee['name'],gifter['name'])


    part2 = MIMEText(html, 'html')
    msg['Subject'] = "Your Secret Santa"
    msg.attach(part2)
    # sending the mail
    s.sendmail(gmail_address, giftee['email'], msg.as_string())

    # terminating the session
    s.quit()

def main():
    json_data = readInParticipants()
    pairings = generateList(json_data)
    
    valid = isValid(pairings)
    while valid == False:
        pairings = generateList(json_data)
        
        valid = isValid(pairings)

    for pair in pairings:
        email_handling(pair)
    print("emails sent!!")


main()