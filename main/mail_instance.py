import os
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from main.auth import create_service
from settings import DEFAULT_FROM


class Mail:

    def __init__(self, from_mail, to_mail, subject, template):
        if from_mail is None:
            from_mail = DEFAULT_FROM

        self.from_mail = from_mail
        self.to_mail = to_mail
        self.subject = subject
        self.template = template
        self.mail = MIMEMultipart()

    def attach_image(self, image_path, cid=None):
        with open(image_path, 'rb') as img:
            img_data = img.read()

        image = MIMEImage(img_data, name=os.path.basename(image_path))

        if cid:
            image.add_header('Content-ID', f'<{cid}>')

        self.mail.attach(image)

    def send(self, ignore_fall=False):
        raw_mail = self.get_raw_mail()
        service = create_service()

        try:
            service.users().messages().send(userId='me', body={'raw': raw_mail}).execute()
        except Exception as e:
            print(e)

            if not ignore_fall:
                raise Exception(e)

    def get_raw_mail(self):
        if type(self.to_mail) is list:
            self.to_mail = ', '.join(self.to_mail)

        self._set_up_mail()

        return base64.urlsafe_b64encode(self.mail.as_bytes()).decode()

    def _set_up_mail(self):
        self.mail['from'] = self.from_mail
        self.mail['to'] = self.to_mail
        self.mail['subject'] = self.subject
        self.mail.attach(MIMEText(self.template, 'html'))
