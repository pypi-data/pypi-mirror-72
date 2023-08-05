[![N|Solid](https://faspay.co.id/docs/sendme/images/sendMe-new.png)](https://faspay.co.id/docs/index-sendme.html#faspay-sendme) 
## Welcome To Faspay SendMe

This package provides Faspay SendMe 1.4 support for the Python Language.

## Requirements

The following versions of Python are supported.

* Python 3 or latest

To use this package, it will be necessary to have a credential. These are referred to as 
* virtual_account
* faspay_key
* faspay_secret
* app_key
* app_secret
* client_key
* client_secret
* iv

in your root project, include config file "SendMeConfig.ini".
You can download file inside "tests" directory.

Please contact Administrator Faspay to create the required credentials.

## Installation
To install in your project use this command:
```sh
pip install FaspaySendme
```
Install Dependencies package
```sh
pip install requests
pip install pycryptodome
```

## Upgrade Latest Version
To upgrade use this command:
```sh
pip install --upgrade FaspaySendme
```

## Usage
### Register Flow
```python
from FaspaySendme import Api

response = Api.Services.register(Api.Services, {
    "virtual_account"           : "9920015307",
    "beneficiary_account"       : "10000005",
    "beneficiary_account_name" 	: "Faspay Dev 5",
    "beneficiary_va_name"       : "Faspay Lib Tst",
    "beneficiary_bank_code" 	: "008",
    "beneficiary_bank_branch" 	: "KCP Pasar Baru",
    "beneficiary_region_code" 	: "0102",
    "beneficiary_country_code" 	: "ID",
    "beneficiary_purpose_code" 	: "1"
})
```

### Mutasi Flow
```python
from FaspaySendme import Api

response = Api.Services.mutasi(Api.Services, {
    "virtual_account"   : "9920015307",
    "start_date"        : "2019-02-01",
    "end_date" 	        : "2019-02-18"
})
```

the parameter refer to Faspay SendMe [Documentation](https://faspay.co.id/docs/index-en-sendme.html#faspay-sendme).

### Environment Production
To use environment production must be call this method like as :
```python
from FaspaySendme import Api

Api.Services.enableProd(Api.Services)
```

#### Available Methods

The `Faspay SendMe` provide has the following [method]:

- 'register()' to use register your customer bank account
- 'confirm()' to use confirm your customer bank account after register method
- 'transfer()' to use transfer balance to customer bank account registered
- 'balance_inquiry()' to use check your balance 
- 'inquiry_name()' to use check your customer bank account detail
- 'mutasi()' to use get your transaction history
- 'inquiry_status()' to use check the latest status transfer.