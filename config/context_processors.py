from django.conf import settings


def export_vars(request):
    data = {}
    data['PRODUCT_NAME'] = settings.PRODUCT_NAME
    data['COMPANY_NAME'] = settings.COMPANY_NAME
    return data
