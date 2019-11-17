# -*-coding:utf-8-*-
import random
import smtplib
import dns.resolver

from flask import Flask
from flask import request


def fetch_mx(host):
    answers = dns.resolver.query(host, 'MX')
    res = [str(rdata.exchange)[:-1] for rdata in answers]
    return res


def verify_istrue(email):
    try:
        name, host = email.split('@')

        host = random.choice(fetch_mx(host))
        s = smtplib.SMTP(host, timeout=10)
        s.docmd('HELO chacuo.net')

        s.docmd('MAIL FROM:<3121113@chacuo.net>')
        send_from = s.docmd('RCPT TO:<%s>' % email)
        if send_from[0] == 250 or send_from[0] == 451:
            final = True  # 存在
        elif send_from[0] == 550:
            final = False  # 不存在
        else:
            final = None  # 未知

        s.close()
        return final
    except:
        return False


class EmailVerifyApi(object):
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/email_verify')
        def verify():
            email = request.args.get('email')
            if verify_istrue(email):
                return '1'
            else:
                return '0'

    def run(self):
        self.app.run('0.0.0.0', port=8101)

    @classmethod
    def start(cls):
        verify = EmailVerifyApi()
        verify.run()

if __name__ == '__main__':
    EmailVerifyApi.start()