import smtplib
import urllib3
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

frommail = 'hej.dave.develop@gmail.com'
password = 'Asdasd123'
recipients = ['hej.dave.develop@gmail.com', 'hej.dave@gmail.com']
http = urllib3.PoolManager()
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'sv-SE,sv;q=0.8,en-US;q=0.6,en;q=0.4',
           'Connection': 'keep-alive',
           'Cookie': '__cfduid=de02aaad661dc10deb5e705bc3524cd8c1485026156; PVPNET_LANG=en_US; PVPNET_REGION=na; play_splash_count=1; ping_session_id=df671e2e-9627-4050-af65-91e3d31a6127; _dc_gtm_UA-5859958-1=1; _ga=GA1.2.615614854.1485026157',
           'Host': 'euw.leagueoflegends.com',
           'Referer': 'http://euw.leagueoflegends.com/en/tag/patch-notes',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
currentPatchNumber = 71

def isNewPatch():
    global currentPatchNumber
    response = http.request('GET', 'http://euw.leagueoflegends.com/en/news/game-updates/patch/patch-'+str(currentPatchNumber+1)+'-notes', headers=headers)
    if response.status != 404:
        currentPatchNumber += 1
        return True
    return False


def getmailcontent():
    response = http.request('GET', 'http://euw.leagueoflegends.com/en/news/game-updates/patch/patch-'+str(currentPatchNumber)+'-notes', headers=headers)
    return response.data


def sendmail(msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(frommail, password)
    server.sendmail(frommail, recipients, msg.as_string())
    server.quit()

if __name__ == "__main__":
    while True:
        if isNewPatch():
            msg = MIMEMultipart('alternative')
            msg.attach(MIMEText(getmailcontent(), 'html'))
            msg['Subject'] = "New LOL Patch nr "+str(currentPatchNumber)
            sendmail(msg)
        time.sleep(86400)

