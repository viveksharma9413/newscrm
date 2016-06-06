import requests

'''
Function to use mailgun api to send mails to client
'''

def send_mail(to,subject,mail):
    print to+'\n'+subject+'\n'+mail
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc2d89dcd454e441ebf71b771bfcab99c.mailgun.org/messages",
        auth=("api", "key-798e41d3e7e6ec7cfcecf69960bc5fc2"),
        data={"from": "Daily news<mailgun@sandboxc2d89dcd454e441ebf71b771bfcab99c.mailgun.org>",
              "to": to,
              "subject": subject,
              "text": "Your Daily Dose of News",
              "html": mail})

# send_mail("viveksharma9413@gmail.com","hello","<a href  = 'google.com'>testing<a>")