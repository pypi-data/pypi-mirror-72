import logging

from zeep import Client

from .signature import make_signature

_log = logging.getLogger('pyaxepta')

TEST_ENDPOINT = 'https://merchant.s2stest.bnlpositivity.it/BNL_CG_SERVICES/services/'
PROD_ENDPOINT = 'https://merchant.s2stest.bnlpositivity.it/BNL_CG_SERVICES/services/'

AXEPTA_DEFAULT_CURRENCY = 'EUR'


class Axepta:
    def __init__(self, tid, ksig, test=False, debug=False):
        self.tid = tid
        self.ksig = ksig
        self.debug = debug

        endpoint = TEST_ENDPOINT if test else PROD_ENDPOINT
        self.client = Client(endpoint + 'PaymentTranGatewayPort?wsdl')
        self.tokenizer_client = Client(endpoint + 'TokenizerGatewayPort?wsdl')

    def _prepare_request(self):
        data = {}
        data['tid'] = self.tid
        return data

    def request(self, client, method, data):
        try:
            data['signature'] = make_signature(self.ksig, method, data)
            response = client.service[method](data)
        except Exception as e:
            response = {
                'rc': '-1',
                'error': True,
                'errorDesc': 'System error: ({})'.format(e),
            }

        if self.debug:
            _log.info('AXEPTA: Response {}'.format(method))
            _log.info(response)

        return response

    #######################################################
    # Public API
    #######################################################

    def card_transaction(self, amount, transaction_id, card_number, exp_month, exp_year, currency=AXEPTA_DEFAULT_CURRENCY, **kwargs):
        data = self._prepare_request()
        data['shopID'] = transaction_id
        data['trType'] = 'PURCHASE'
        data['amount'] = amount
        data['currencyCode'] = currency
        data['pan'] = card_number
        # data['cvv2'] = kwargs['cvv2']
        data['expireMonth'] = exp_month
        data['expireYear'] = exp_year

        for key, value in kwargs.items():
            data[key] = value

        if self.debug:
            _log.info('AXEPTA: Card Transaction')
            _log.info(data)

        return self.request(self.client, 'auth', data)

    def token_transaction(self, amount, transaction_id, token, currency=AXEPTA_DEFAULT_CURRENCY, **kwargs):
        data = self._prepare_request()
        data['shopID'] = transaction_id
        data['trType'] = 'PURCHASE'
        data['amount'] = amount
        data['currencyCode'] = currency
        data['payInstrToken'] = token

        for key, value in kwargs.items():
            data[key] = value

        if self.debug:
            _log.info('AXEPTA: Token Transaction')
            _log.info(data)

        return self.request(self.client, 'auth', data)

    def refund_transaction(self, amount, transaction_id, bank_transaction_id, **kwargs):
        data = self._prepare_request()
        data['shopID'] = transaction_id
        data['amount'] = amount
        data['refTranID'] = bank_transaction_id

        for key, value in kwargs.items():
            data[key] = value

        if self.debug:
            _log.info('AXEPTA: Refund Transaction')
            _log.info(data)

        return self.request(self.client, 'credit', data)

    def request_token(self, transaction_id, card_number, exp_month, exp_year, **kwargs):
        data = self._prepare_request()
        data['shopID'] = transaction_id
        data['pan'] = card_number
        data['expireMonth'] = exp_month
        data['expireYear'] = exp_year

        for key, value in kwargs.items():
            data[key] = value

        if self.debug:
            _log.info('AXEPTA: Request Token')
            _log.info(data)

        return self.request(self.tokenizer_client, 'enroll', data)

    def update_token(self, transaction_id, token, exp_month, exp_year, **kwargs):
        raise NotImplementedError

    def delete_token(self, transaction_id, token, **kwargs):
        data = self._prepare_request()
        data['shopID'] = transaction_id
        data['payInstrToken'] = token

        for key, value in kwargs.items():
            data[key] = value

        if self.debug:
            _log.info('AXEPTA: Delete Token')
            _log.info(data)

        return self.request(self.tokenizer_client, 'delete', data)
