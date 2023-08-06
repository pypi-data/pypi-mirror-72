from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient.errors import HttpError


def get_mct_service(adscale_key: str):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        adscale_key, scopes=['https://www.googleapis.com/auth/content'])
    service = discovery.build('content', 'v2', credentials=credentials)
    return service


def get_mct_account_details(merchant_id: int, adscale_key: str):

    try:
        service = get_mct_service(adscale_key)
        # Get account status alerts from MCT
        request_account_statuses = service.accounts().get(merchantId=merchant_id,
                                                          accountId=merchant_id)
        response_account_statuses = request_account_statuses.execute()
    except HttpError as err:
        raise ValueError(f"We cannot access account ({merchant_id}). Are you sure you grant access and give correct ID?)")
    return response_account_statuses['name']


def check_if_multi_client_account(merchant_id: int, adscale_key: str):
    """ Sends an error if the account is a MCA """
    try:
        service = get_mct_service(adscale_key)

        # This API method is only available to sub-accounts, thus it will fail if the merchant id is a MCA
        request_account_products = service.products().list(merchantId=merchant_id)
        response_account_statuses = request_account_products.execute()
    except HttpError as err:
        raise ValueError(f"This merchant id ({merchant_id} is for multi acccounts. You can only link sub-accounts.)")
    return response_account_statuses
