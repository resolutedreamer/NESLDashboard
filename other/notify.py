import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "localhost"

class Notification(object):
    def __init__(self, email, condition, msg):
        self.email = email
        self.condition = condition
        self.msg = msg

    def notify(self):
        subject = "Energy Dashboard Notification"
        from_addr = "noreply@enerdash.com"
        mimetext = MIMEText(self.msg)
        mimetext["Subject"] = subject
        mimetext["From"] = from_addr
        mimetext["To"] = self.email

        server = smtplib.SMTP(SMTP_SERVER)
        print "sending:"
        print mimetext.as_string()
        server.sendmail(from_addr, [self.email], mimetext.as_string())
        server.quit()

cell_service_domain = {
        "att": "txt.att.net",
        "verizon": "vtext.com",
        "tmobile": "tmomail.net",
        "sprint": "messaging.sprintpcs.com",
        "virgin": "vmobl.com",
        "uscellular": "email.uscc.net",
        "nextel": "messaging.nextel.com",
        "boost": "myboostmobile.com",
        "alltel": "message.alltel.com"
}

class TxtNotification(Notification):
    def __init__(self, number, service, condition, msg):
        email = str(number) + "@" + cell_service_domain[service]
        super(TxtNotification, self).__init__(email, condition, msg)

class NotificationManager:
    def add_notification(self, notification):
        pass 

if __name__ == "__main__":
    txtnot = TxtNotification("7606224651", "verizon",  None, "hello")
    txtnot.notify()
    #notif = Notification("jhaugen2004@gmail.com", None, "hello")
    #notif.notify()

