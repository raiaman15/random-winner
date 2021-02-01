import re
from stdnum import verhoeff
from stdnum.exceptions import *
from stdnum.util import clean
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(value):
    """ Validates name of any entity """
    if not value.replace(" ", "").isalpha():
        raise ValidationError(
            _('%(value)s is not a valid name. It should contain only alphabets.'),
            params={'value': value},
        )


def validate_conatct_number(value):
    """ Validates phone number - 10 digit Indian Phone Number """
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}")
    if not Pattern.match(value):
        raise ValidationError(
            _('%(value)s is not a valid contact number. It should be in similar to 91XXXXXXXXXX.'),
            params={'value': value},
        )


def validate_otp(value):
    """ Validates OTP 6 digit number """
    if value < 100000 or value > 999999:
        raise ValidationError(
            _('The OTP is not valid. It must be 6 digit number.'))


def validate_amount(value):
    """ Validates the amount (of transaction/balance/investment) """
    if value < 0:
        raise ValidationError(
            _('%(value)s is not a valid amount. It cannot be negative.'),
            params={'value': value},
        )


def validate_balance_transaction_type(value):
    """ Validates the transaction type (D/C) """
    if value not in ('D', 'C'):
        raise ValidationError(
            _('%(value)s is not a valid transaction type. It should either be Debit or Credit.'),
            params={'value': value},
        )


def validate_investment_transaction_type(value):
    """ Validates the investment transaction type (D/I) """
    if value not in ('D', 'I'):
        raise ValidationError(
            _('%(value)s is not a valid transaction type. It should either be Dis-Invest or Invest.'),
            params={'value': value},
        )


def validate_number(value):
    """ Validates if the value is a number """
    if not str(value).isnumeric():
        raise ValidationError(
            _('%(value)s is not a valid number.'),
            params={'value': value},
        )


def validate_investment(value, decided_amount=10000):
    """ Validates if the investment amount if multiple of decided amount. """
    if value % decided_amount != 0:
        raise ValidationError(
            _('%(value)s is not a valid amount number. It must be in multiples of %(decided_amount)s'),
            params={'value': value, 'decided_amount': decided_amount},
        )


def validate_aadhaar_number(value):
    """ Validates if the aadhaar number is a valid (Verhoeff Algorithm's). """
    # Verify using https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/in_/aadhaar.py

    """Regular expression used to check syntax of Aadhaar numbers."""
    aadhaar_re = re.compile(r'^[2-9][0-9]{11}$')

    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(value, ' -').strip()

    if len(number) != 12:
        raise ValidationError(
            _('%(value)s is not a valid Aadhaar Number. It must be 12 digit long!'),
            params={'value': value},)

    if not aadhaar_re.match(number):
        raise ValidationError(
            _('%(value)s is not a valid Aadhaar Number. Type the XXXX XXXX XXXX formatted number from your Aadhaar Card! (without spaces)'),
            params={'value': value},)

    try:
        verhoeff.validate(number)
    except:
        raise ValidationError(
            _('%(value)s is not your valid Aadhaar Number. Type the XXXX XXXX XXXX formatted number from your Aadhaar Card! (without spaces)'),
            params={'value': value},)


#######################################
# Custom Validators for Business Logics
#######################################
