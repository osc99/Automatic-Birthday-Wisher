from datetime import datetime
import pandas
import random
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.mime.base import MIMEBase
from string import Template

MY_EMAIL = "sender mail id"
MY_PASSWORD = "sender password"

today = datetime.now()
today_tuple = (today.month, today.day)
a = [];
data = pandas.read_csv("birthdays.csv")
birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}
if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    a.append(birthday_person["email"])

path_plot = 'bir.png'


from_mail = MY_EMAIL
from_password = MY_PASSWORD

to_mail = a

smtp_server = "smtp.gmail.com"
smtp_port = 465

def send_email(path_plot, smtp_server, smtp_port, from_mail, from_password, to_mail):
    '''
        Send results via mail
    '''
    msg = MIMEMultipart()
    msg['Subject'] = 'Happy Birthday'+' '+birthday_person["name"]
    msg['From'] = from_mail
    COMMASPACE = ', '
    msg['Bcc'] = COMMASPACE.join(to_mail)
    msg.preamble = 'Happy Birthday'+ birthday_person["name"];

    # Open the files in binary mode and attach to mail
    with open(path_plot, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment')
        img.add_header('X-Attachment-Id', '0')
        img.add_header('Content-ID', '<0>')
        fp.close()
        msg.attach(img)
    
    # Attach HTML body
    code = str(birthday_person["name"])
    msg.attach(MIMEText(
        '''
        <html>
            <body>
                <i style="color: Blue; font-family:'Cursive',Lucida Handwriting;font-size: 1.790em;"><h1>Happy birthday {code}</h1></i>
            
                <p style="font-family:'Cursive',Bradley Hand ITC;font-size: 1.780em;"><b>Wishing you a great birthday, a memorable year and success in all you do. From all of us. 😊</b></p>

                <p>Testing through script please ignore...</p>
                
                <p><img src="cid:0"></p>
                
                <p>Thanks and Regards</p>
                <p>XYZ</p>
            </body>
        </html>'
        '''.format(code=code),
        'html', 'utf-8'))

    # Send mail
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.ehlo()
    server.login(from_mail, from_password)

    server.sendmail(from_mail, to_mail, msg.as_string())
    server.quit()


    
send_email(path_plot, smtp_server, smtp_port, from_mail, from_password, to_mail)#birthday_person["email"]