import re
from stdnum import verhoeff
from stdnum.util import clean
from django.core.exceptions import ValidationError


def validate_name(value):
    """ Validates name of any entity """
    if not value.replace(" ", "").isalpha():
        raise ValidationError(
            '%(value)s is not a valid name. It should contain only alphabets.',
            params={'value': value},
        )


def validate_username(value):
    """ Validates phone number - 10 digit Indian Phone Number """
    pattern = re.compile("(0/91)?[5-9][0-9]{9}")
    if not pattern.match(value):
        raise ValidationError(
            '%(value)s is not a valid contact number. It should be in similar to 91XXXXXXXXXX.',
            params={'value': value},
        )


def validate_amount(value):
    """ Validates the amount (of transaction/balance/investment) """
    if value < 0:
        raise ValidationError(
            '%(value)s is not a valid amount. It cannot be negative.',
            params={'value': value},
        )


def validate_balance_type_of_transaction(value):
    """ Validates the transaction type (D/C) """
    if value not in ('D', 'C'):
        raise ValidationError(
            '%(value)s is not a valid transaction type. It should either be Debit or Credit.',
            params={'value': value},
        )


def validate_investment_type_of_transaction(value):
    """ Validates the investment transaction type (D/I) """
    if value not in ('D', 'I'):
        raise ValidationError(
            '%(value)s is not a valid transaction type. It should either be Dis-Invest or Invest.',
            params={'value': value},
        )


def validate_support_ticket_type_of_ticket(value):
    """ Validates the investment ticket type (F/A) """
    if value not in ('F', 'A'):
        raise ValidationError(
            '%(value)s is not a valid ticket type. It should either be Finance or Application.',
            params={'value': value},
        )


def validate_message(value):
    """ Validates any alphanumeric message """
    if not value.replace(" ", "").replace(".", "").replace(",", "").isalnum():
        raise ValidationError(
            '%(value)s is not a valid message. It should contain only alphabets, digits and characters like "," or "."',
            params={'value': value},
        )


def validate_number(value):
    """ Validates if the value is a number """
    if not str(value).isnumeric():
        raise ValidationError(
            '%(value)s is not a valid number.',
            params={'value': value},
        )


def validate_pool_size(value):
    """ Validates if the value is a number """
    validate_number(value)
    if int(value) > 24:
        raise ValidationError(
            '%(value)s is not a valid Size for pool (Maximum is 24).',
            params={'value': value},
        )


def validate_investment(value, decided_amount=10000):
    """ Validates if the investment amount if multiple of decided amount. """
    validate_amount(value)
    if value % decided_amount != 0:
        raise ValidationError(
            '%(value)s is not a valid amount number. It must be in multiples of %(decided_amount)s',
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
            '%(value)s is not a valid Aadhaar Number. It must be 12 digit long!',
            params={'value': value}, )

    if not aadhaar_re.match(number):
        raise ValidationError(
            '%(value)s is not a valid Aadhaar Number. Type the XXXX XXXX XXXX formatted number from your Aadhaar Card! (without spaces)',
            params={'value': value}, )

    try:
        verhoeff.validate(number)
    except Exception:
        raise ValidationError(
            '%(value)s is not your valid Aadhaar Number. Type the XXXX XXXX XXXX formatted number from your Aadhaar Card! (without spaces)',
            params={'value': value}, )


def validate_pan_number(value):
    """ Validates if the PAN number is a valid. """
    # Verify using https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/in_/pan.py

    _card_holder_types = {
        'A': 'Association of Persons (AOP)',
        'B': 'Body of Individuals (BOI)',
        'C': 'Company',
        'F': 'Firm',
        'G': 'Government',
        'H': 'HUF (Hindu Undivided Family)',
        'L': 'Local Authority',
        'J': 'Artificial Juridical Person',
        'P': 'Individual',
        'T': 'Trust (AOP)',
        'K': 'Krish (Trust Krish)',
    }

    """Regular expression used to check syntax of PAN numbers."""
    _pan_re = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')

    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(value, ' -').upper().strip()

    if len(number) != 10:
        raise ValidationError(
            '%(value)s is not a valid PAN Number. It must be 10 digit long!',
            params={'value': value}, )

    if not _pan_re.match(number):
        raise ValidationError(
            '%(value)s is not a valid PAN Number. Type the XXXXXXXXXX formatted number from your PAN Card! (without spaces)',
            params={'value': value})

    if not _card_holder_types.get(number[3]):
        raise ValidationError(
            '%(value)s is not a valid PAN Number Type. Type the XXXXXXXXXX formatted number from your PAN Card! (without spaces)',
            params={'value': value})


#######################################
# Custom Validators for Business Logics
#######################################
# We are treating the username field of CustomUser as username for allauth
custom_username_validator = [validate_username]
