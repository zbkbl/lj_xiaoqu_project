# coding:utf-8
import smtplib
import datetime
from email.mime.text import MIMEText
from lj_project.Exception.readUtils import MysqlConfig


class emailSender(object):

    def __init__(self):
        emailConfig = MysqlConfig.getEmailConfig()
        self.smtp_host = emailConfig['host']
        self.smtp_user = emailConfig['user']
        self.smtp_pwd = emailConfig['pwd']
        self.smtp_port = emailConfig['port']
        self.sender = emailConfig['sender']

    def sendEmail(self, toLst, subject, body, spider):
        """
        发送邮件
        :param toLst: 收件人的邮箱列表["465482631@qq.com", "77789713@qq.com"]
        :param subject: 邮件标题
        :param body: 邮件内容
        :return:
        """
        message = MIMEText(body, 'plain', 'utf-8')
        message['From'] = self.sender
        message['To'] = ','.join(toLst)
        message['Subject'] = subject
        try:
            # 实例化一个SMTP_SSL对象
            smtpSSLClient = smtplib.SMTP()
            smtpSSLClient.connect(self.smtp_host)
            # 登录smtp服务器
            loginRes = smtpSSLClient.login(self.smtp_user, self.smtp_pwd)
            # loginRes = (235, b'Authentication successful')
            spider.logger.info(u"邮箱登录结果：loginRes = {"+ str(loginRes) +"}")
            if loginRes and loginRes[0] == 235:
                spider.logger.info(u"登录成功，code = {" + str(loginRes[0]) + "}")
                smtpSSLClient.sendmail(self.sender, toLst, message.as_string())
                spider.logger.info("mail has been send successfully. message:" + message.as_string())
                smtpSSLClient.quit()

            else:
                spider.logger.info(u"登陆失败，code = {" + str(loginRes[0]) + "}")

        except Exception as e:
            spider.logger.info(e.message)

if __name__=="__main__":
    emailSenderClient = emailSender()
    toSendEmailLst = ['542463713@qq.com']
    finishTime = datetime.datetime.now()
    subject = "爬虫结束状态汇报：name = baidu, reason = {reason}, finishedTime = {finishTime}"
    body = "细节：reason = {reason}, successs! at:{finishTime}"
    emailSenderClient.sendEmail(toSendEmailLst, subject, body)