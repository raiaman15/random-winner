"""
Various utilities including:
1. Send OTP SMS with textlocal
2. Send platform Invite via SMS
3. Send pool Invite via SMS
4. Send pool Invite via e-mail
5. Send profile Verified SMS
6. Send profile Verified e-mail
7. Send profile Approved PoolMaster SMS
8. Send profile Approved PoolMaster SMS
9. Shorten URL to send via SMS
"""

import ast
import urllib.request
import urllib.parse
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy

key = settings.TXTLCL_KEY
sender = ''  # Leave unless approved by DLT & TXTLCL max 6 alphanumeric


def short_url(url, apikey=key):
    data = urllib.parse.urlencode({'apikey': apikey, 'url': url})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/create_shorturl/")
    f = urllib.request.urlopen(request, data)
    d = ast.literal_eval(f.read().decode('utf-8', 'strict'))
    shorturl = d['shorturl'].replace('\\', '')
    return shorturl


def send_sms(apikey, numbers, sender, message):
    if settings.DEBUG:
        return print(message)

    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


def send_otp(number, otp, first_name='', last_name=''):
    """
    response = send_otp('7007488735', 'Aman', 'Rai', 132435)

    Dynamically formats the SMS body to meet the template conditions.
    Constraints:
    1. According the ISO IEC 7813 the cardholder name length must be 2 to 26 
    characters including first name, last name and spaces.
    2. OTP length is 6 characters
    3. Newline character takes 1 character length
    """

    full_name = ''

    if len(first_name) or len(last_name):
        name_long = f'{first_name.title()} {last_name.title()}'
        name_short = f'{first_name.title()} {last_name[0].upper()}.'

        full_name = name_long if len(name_long) <= 26 else name_short[:26]

    lines = []
    lines.append(f'Welcome {full_name},')
    lines.append(f'OTP is {otp}')
    lines.append(
        f'Hope you enjoy our platform and praise our effort in making affordable solution for Educational Institution!'
    )

    message = '\n'.join(lines)
    response = send_sms(key, number, sender, message)
    print(response)


def send_sms_platform_invite(number, username, password, invitee_number):
    """
    response = send_sms_platform_invite('7007488735', '7007488734', '132435')

    Dynamically formats the SMS body to meet the template conditions. Constraints:
    1. According to the platform, username is phone number (12 digit max)
    2. Default password is 16 character long
    3. Newline character takes 1 character length
    """

    url = 'https://bit-boomer.com/accounts/signup/'
    shorturl = short_url(url)

    lines = []
    lines.append(f'Welcome to BitBoomer!')
    lines.append(f'Sign in at {shorturl} with contact number: {username} and password: {password}')
    lines.append(f'Invited by {invitee_number}')

    message = '\n'.join(lines)
    response = send_sms(key, number, sender, message)
    print(response)


def send_sms_pool_invite(number, pool_id, invitee_number):
    """
    response = send_sms_pool_invite('7007488735', '7007488734', '132435')

    Dynamically formats the SMS body to meet the template conditions. Constraints:
    1. According to the platform, username is phone number (12 digit max)
    3. Newline character takes 1 character length
    """

    url = f'https://bit-boomer.com/pools/detail/{pool_id}/'
    shorturl = short_url(url)

    lines = []
    lines.append(f'Hello from BitBoomer!')
    lines.append(f'You have been invited by {invitee_number} to join their pool {shorturl}')

    message = '\n'.join(lines)
    response = send_sms(key, number, sender, message)
    print(response)


def send_email_pool_invite(email_id, pool_id, invitee_number):
    """
    response = send_email_pool_invite('7007488735', '7007488734', '132435')

    Dynamically formats the email body to meet the requirements. Constraints:
    1. Precise Subject
    2. Personalized Touch with Happy Tone
    """

    url = f'https://bit-boomer.com/pools/detail/{pool_id}/'

    lines = []
    lines.append(f'Hello from BitBoomer!')
    lines.append(f'You have been invited by {invitee_number} to join their pool {url}')

    message = '\n'.join(lines)
    try:
        send_mail(
            subject='BitBoomer | Pool Invitation Recieved! ',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_id],
            fail_silently=True,
        )
    except Exception as e:
        print(f'Exception Occurred {e}')


def send_sms_pool_winner(number, pool_id):
    """
    response = send_sms_pool_invite('7007488735', '7007488734', '132435')

    Dynamically formats the SMS body to meet the template conditions. Constraints:
    1. According to the platform, username is phone number (12 digit max)
    3. Newline character takes 1 character length
    """

    url = f'https://bit-boomer.com/pools/detail/{pool_id}/'
    shorturl = short_url(url)

    lines = []
    lines.append(f'Hello from BitBoomer!')
    lines.append(f'Congratulations! You won this month spin for the pool {shorturl}')

    message = '\n'.join(lines)
    response = send_sms(key, number, sender, message)
    print(response)


def send_email_pool_winner(email_id, pool_id):
    """
    response = send_email_pool_invite('7007488735', '7007488734', '132435')

    Dynamically formats the email body to meet the requirements. Constraints:
    1. Precise Subject
    2. Personalized Touch with Happy Tone
    """

    url = f'https://bit-boomer.com/pools/detail/{pool_id}/'
    shorturl = short_url(url)

    lines = []
    lines.append(f'Hello from BitBoomer!')
    lines.append(f'Congratulations! You won this month spin for the pool {shorturl}')
    lines.append(f'Payments will be processed shortly.')

    message = '\n'.join(lines)

    response = send_mail(
        subject='BitBoomer | You Won the Spin! ',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email_id],
        fail_silently=True,
    )

    print(bool(response), message)


def automate_activation():
    return reverse_lazy('automatic_activate_pool')


def automate_spin():
    return reverse_lazy('automatic_spin_pool')
