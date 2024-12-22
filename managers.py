from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
import logging


# Organization list
ORGANIZATION = (
    ('', '[Select an organization]'),
    ('AMFB', 'Alert MFB'),
    ('ABL', 'AutoBucks')
)


# Role list
ROLE = (
    ('', '[Assign a role]'), ('Upload Officer', 'Upload Officer'), ('HOP', 'HOP'),
    ('Credit', 'Credit'), ('IT', 'IT'), ('Others', 'Others')
)


# Branch list
BRANCH = (
    ('', '[Select a branch]'), ('Head Office', 'Head Office'),
    ('Ebute Metta', 'Ebute Metta'), ('Idumagbo', 'Idumagbo'),
    ('Idumota', 'Idumota'), ('Sango', 'Sango'), ('Ikeja', 'Ikeja'),
    ('Agege', 'Agege'), ('Ikorodu', 'Ikorodu'), ('Mushin', 'Mushin'),
    ('Trade Fair', 'Trade Fair'), ('Ikotun', 'Ikotun'),
    ('Abeokuta', 'Abeokuta'), ('Ibandan', 'Ibandan')
)


def acct_file_size(value):
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 5mb.")


def loan_file_size(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 10mb.")


def zip_file_size(value):
    limit = 20 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File too large. Size should not exceed 20mb.")


# Get the email logger
email_logger = logging.getLogger('email_logger')

# Asynchronous email sending
def send_async_email(subject, message, from_email, recipient_list):
    try:
        email = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        email.send()
    except Exception as e:
        email_logger.error(f"Error sending email: {e}")
