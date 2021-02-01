"""
Various utilities including:
1. Send Text SMS with textlocal
"""

import urllib.request
import urllib.parse
from decimal import *
from django.conf import settings

key = 'x9Wv/NxkW+M-PIYn7TIxcaB2meS9QAG'
sender = 'Infroid Shiksha API'


def sendSMS(apikey, numbers, sender, message):
    """ #TODO-URGENT: Send the OPT to contact number via SMS """

    if settings.DEBUG:
        print(message)

    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return fr


def send_otp(number, first_name, last_name, otp):
    """
    response = send_otp('7007488735', 'Aman', 'Rai', 132435)

    Dynamically formats the SMS body to meet the template conditions.
    Constraints:
    1. According the ISO IEC 7813 the cardholder name length must be 2 to 26 
    characters including first name, last name and spaces.
    2. OTP length is 6 characters
    3. Newline character is defined by '%n' and takes 1 character length
    """

    name_long = f'{first_name.title()} {last_name.title()}'
    name_short = f'{first_name.title()} {last_name[0].upper()}.'

    name = name_long if len(name_long) <= 26 else name_short[:26]

    lines = []
    lines.append(f'Welcome {name},')
    lines.append(f'OTP is {otp}')
    lines.append(
        f'Hope you enjoy our platform and praise our effort in making affordable solution for Educational Institution!'
    )

    message = '%n'.join(lines)
    response = sendSMS(key, number, sender, message)
    print(response)
