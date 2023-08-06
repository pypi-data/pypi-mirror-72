import base64
import hashlib
import hmac

SIGNATURE_ORDER = {
    'auth': [
        'tid',
        'shopID',
        'shopUserRef',
        'shopUserName',
        'shopUserIP',
        'trType',
        'amount',
        'currencyCode',
        'callbackURL',
        'pan',
        'payInstrToken',
        'cvv2',
        'expireMonth',
        'expireYear',
        'addInfo1',
        'addInfo2',
        'addInfo3',
        'addInfo4',
        'addInfo5'
    ],

    'credit': [
        'tid',
        'shopID',
        'amount',
        'refTranID',
        'addInfo1',
        'addInfo2',
        'addInfo3',
        'addInfo4',
        'addInfo5'
    ],

    'enroll': [
        'tid',
        'shopID',
        'pan',
        'expireMonth',
        'expireYear',
        'addInfo1',
        'addInfo2',
        'addInfo3',
        'addInfo4',
        'addInfo5'
    ],

    'delete': [
        'tid',
        'shopID',
        'payInstrToken',
        'addInfo1',
        'addInfo2',
        'addInfo3',
        'addInfo4',
        'addInfo5'
    ]
}


def make_signature(key, method, payload):
    values = [payload.get(field, '') for field in SIGNATURE_ORDER[method]]
    return base64.b64encode(hmac.new(
        bytes(key, 'utf-8'),
        msg=bytes(''.join(map(str, values)), 'utf-8'),
        digestmod=hashlib.sha256
    ).digest())
