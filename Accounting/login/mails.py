import smtplib
from email.mime.text import MIMEText


class SendMails:
    def __init__(self, shost, user, pwd, toaddr, subject, context):
        # 邮箱服务器信息
        self._host = shost
        self._user = user
        self._pwd = pwd
         # 邮件信息
        self._toaddr = toaddr
        self._subject = subject
        self._context = context

    def sendE(self):
        print("开始发送邮....")
        msg=MIMEText(self._context, 'plain', "utf-8")   #内容,格式，编码
        msg['Subject'] = self._subject
        msg['From'] = "{}".format(self._user)  # 格式化
        msg['To'] = self._toaddr    #",".join(self._toaddr)
        try:
            server = smtplib.SMTP_SSL(self._host, 465)
            server.login(self._user, self._pwd)
            server.sendmail(self._user, self._toaddr, msg.as_string())
            print("Send successfully")
            server.quit()
        except smtplib. SMTPException as e:
            print(e)
            server.quit()
            return False
        return True
