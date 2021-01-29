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
    # TODO-NORMAL: Verify using https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/in_/aadhaar.py
    pass
