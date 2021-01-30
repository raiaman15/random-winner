import re
from stdnum import verhoeff
from stdnum.exceptions import *
from stdnum.util import clean
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
            _('%(value)s is not a valid Aadhaar Number. It must be in valid format XXXX XXXX XXXX!'),
            params={'value': value},)

    try:
        verhoeff.validate(number)
    except:
        raise ValidationError(
            _('%(value)s is not a valid Aadhaar Number. Please confirm it from your Aadhaar Card!'),
            params={'value': value},)
