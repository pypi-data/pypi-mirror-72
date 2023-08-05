
# Simple Zuora Client
## Version 0.1.5

It works with Zuora® API v1.

*Currently supported features*

* Basic get, post, put, delete
* Authentication session
* Multi entity support
* AQuA batch queries (ZOQL)
* query jobs (OWL queries)
* get accounting periods
* get sequence sets 
* delete a sequence set
* get invoice by invoice number
* update account
* update credit memo
* cancel credit memo
* update invoice

*Requirements*

* requests_oauthlib
* oauthlib.oauth2
* requests

*Example*

```python
from simple_zuora_client import ZuoraClient
entity = 'your_zuora_entity_id_if_using_multi_entities'
client_id= r'your_zuora_client_id'
client_secret= r'your_zuora_client_secret'

with ZuoraClient(client_id=client_id,
                 client_secret=client_secret,
                 entity=entity,
                 base_url='https://rest.sandbox.eu.zuora.com',
                 query_retry_timeout=3) as z_client:
    print(z_client.get_accounting_periods())
```
