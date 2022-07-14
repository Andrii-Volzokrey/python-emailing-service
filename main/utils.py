import os
import datetime
from jinja2 import Template

from main.auth import create_service


def send_many(mails, ignore_fails=False):
    service = create_service()

    for mail in mails:
        raw_mail = mail.get_raw_mail()
        try:
            service.users().messages().send(userId='me', body={'raw': raw_mail}).execute()
        except Exception as e:
            print(e)

            if not ignore_fails:
                raise Exception(e)


def set_up_template(template, replacements=None):
    if replacements is None:
        replacements = {}

    with open(os.path.join(os.getcwd(), 'main/templates', template)) as tm:
        jinja_tm = Template(tm.read()).render(replacements)

    return jinja_tm


def convert_to_RFC_datetime(year, month, day, hour, minute):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
