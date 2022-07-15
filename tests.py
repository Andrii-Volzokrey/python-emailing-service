from presets.example import example_mail_preset
from main.utils import send_many

emails = [example_mail_preset('testmail@mail.com', '', {}) for _ in range(5)]
send_many(emails)
