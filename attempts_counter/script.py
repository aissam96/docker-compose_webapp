from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import smtplib
import time
from threading import Timer

# change with sender gmail username and make sure to disable multi factor authentication
gmail_address = "errsendtest@gmail.com"
# change with sender gmail password
gmail_password = "passtest"
# change with receiver email address
receiver_e_address = "erradouane.aissam96@gmail.com"


# setting up the email template and the sender id and password 
def send_email(designed_users):

    # the message template
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = receiver_e_address
    msg['Subject'] = "web_app authentifications"
    body = "Hello \n The following users attempted to access the website with the wrong password for more than 10 times : \n"
    # getting the access attempts
    user = get_user_attempts()
    for n in range(len(designed_users)) :
        body += " user " + "' " + designed_users[n] + " '" + " : " + str(user[designed_users[n]]) + " times \n"
    body += "Thank you"
    msg.attach(MIMEText(body, 'plain'))
    # connecting to gmail server and sending the email notification
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    # the sender username and password
    server.login(gmail_address, gmail_password)
    text = msg.as_string()
    server.sendmail(gmail_address ,receiver_e_address , text)
    server.quit()

# collecting all the access attemts from the error log file
def get_user_attempts():
    users={}
    # open the log file and process each line to export the errors
    with open("/var/error_log/error.log","r") as f:
        for line in f:    
            user_name=""
            condition=False
            for l in line:
                if l=='"' and not condition :
                    condition=True
                elif l=='"' and condition :
                    condition=False
                    if user_name in users.keys():
                        users[user_name]+=1
                    # avoid mistaking the log line with the fav icon error message
                    elif user_name != "/usr/share/nginx/html/favicon.ico" :
                        users[user_name]=1                
                    user_name=""
                    break
                elif condition :
                    user_name+=l
    f.close()
    return users

# filtring the users who have tried a wrong password for more than 10 times
def get_designed_users(users):
    designed_users=[]
    for user in users.keys():
        if users[user]>=10:
            designed_users.append(user)
    return designed_users

# sending an email every 10 minutes
while True :
    # number of minutes to repeat the service
    for i in range(10):
        time.sleep(60)
    designed_users = get_designed_users(get_user_attempts())
    if len(designed_users) >= 1 :
        users = ""
        for user in designed_users :
            users = users + user + ", "
        # print("the following users attempted to access the website for more than 10 times in the last 10 minutes: " + users + " Thank you")
        # sending the email
        send_email(designed_users)
        # wiping the error log file after sending the email
        f=open("/var/error_log/error.log","r+")
        f.truncate(0)
        f.close()