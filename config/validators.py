from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def validate_investment(value, decided_amount=10000):
    """ Validates if the investment amount if multiple of decided amount. """
    if value % decided_amount != 0:
        raise ValidationError(
            _('%(value)s is not a valid amount number. It must be in multiples of %(decided_amount)s'),
            params={'value': value, 'decided_amount': decided_amount},
        )
