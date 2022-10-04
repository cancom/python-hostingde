# Hosting.de Client-Library 
[![codecov](https://codecov.io/gh/cancom/python-hostingde/branch/main/graph/badge.svg?token=C5SXI4B7PV)](https://codecov.io/gh/cancom/python-hostingde) [![Supported Versions](https://img.shields.io/pypi/pyversions/python-hostingde.svg)](https://pypi.org/project/python-hostingde) [![hosting.de API](https://github.com/hosting-de/awesome-hosting.de/raw/master/assets/hostingde-api.svg)](https://github.com/topics/hostingde)


An unofficial client library for the [hosting.de API](https://hosting.de/api/).

- API Version: v1

## Requirements

The package requires Python 3.6+. It is currently only tested with Python 3.8, but should work for Python 3.6.

## Installation & Usage

Install with pip:

```bash
pip install python-hostingde
```

## Getting Started

Please follow the [installation procedure](#installation--usage).  To login with the client, you need your endpoint
url, and an API token. To authenticate:

```python
from hostingde import api
from hostingde.client import HostingDeClient

client: HostingDeClient = api.login('<your endpoint url>', '<your token>')
```

Your endpoint should look like this: `https://<your_domain>/api` (do not forget the `/api` while providing the endpoint).

The client is modularized into the different service types, for example `client.dns` refers to the DNS service API.

For example, to fetch all zones, you can use:

```python
from hostingde import api
from hostingde.client import HostingDeClient

client: HostingDeClient = api.login('<your endpoint url>', '<your token>')

for zone in client.dns.list_zones():
  print(zone)
```

All implemented endpoints are fully documented and typed. You will get corresponding hints in your IDE of choice. 

### Filtering and Sorting API

In order to use filter and sort APIs, we simplified the usage of the API. For example, to search for a specific zone:

```python
from hostingde import api
from hostingde.client import HostingDeClient
from hostingde.model.filter import FilterCondition

client: HostingDeClient = api.login('<your endpoint url>', '<your token>')

zone_filter = FilterCondition('zoneName').eq('example.com')

for zone in client.dns.list_zones(filter=zone_filter):
  print(zone)
```

This will automatically build the corresponding filter expression in the background

```json
{
  "field": "domainName",
  "value": "example.com",
  "relation": "equal"
}
```

Apart from `FilterCondition.eq`, the condition supports all relations currently defined in the API:

| Relation     | Operation                  | Description                                                                                                    |
|--------------|----------------------------|----------------------------------------------------------------------------------------------------------------|
| equal        | FilterCondition.eq         | `field` must match value exactly                                                                                 |
| unequal      | FilterCondition.ne         | `field` must not be the same as value                                                                            |
| greater      | FilterCondition.gt         | `field` must be greater than value. This might apply to e.g. an integer value, a date or a date time             |
| less         | FilterCondition.lt         | `field` must be less than value. This might apply to e.g. an integer value, a date or a date time                |
| greaterEqual | FilterCondition.ge         | `field` must be greater than or equal to value. This might apply to e.g. an integer value, a date or a date time |
| lessEqual    | FilterCondition.le         | `field` must be less than or equal to value. This might apply to e.g. an integer value, a date or a date time    |
|              | FilterCondition.startswith | Corresponds to the `field` method. However, uses wildcard to simplify the usage --> `field*`                     |

Chaining filters is easily supported as well:

```python
from hostingde import api
from hostingde.client import HostingDeClient
from hostingde.model.filter import FilterCondition

client: HostingDeClient = api.login('<your endpoint url>', '<your token>')

zone_filter = (FilterCondition('zoneName').startswith('example') | FilterCondition('zoneName').startswith(
  'demo')) & FilterCondition('zoneName').ne('*.com')

for zone in client.dns.list_zones(filter=zone_filter):
  print(zone)
```

This automatically builds the equivalent filter expression for the API:

```json
{
  "subFilterConnective": "AND",
  "subFilter": [
    {
      "subFilterConnective": "OR",
      "subFilter": [
        {
          "field": "zoneName",
          "value": "example*",
          "relation": "equal"
        },
        {
          "field": "zoneName",
          "value": "demo*",
          "relation": "equal"
        }
      ]
    },
    {
      "field": "zoneName",
      "value": "*.com",
      "relation": "unequal"
    }
  ]
}
```

which is less verbose and more readable.

### Error Handling

If the request returns an error, the error is wrapped inside a `api.client.exceptions.APIException` with all
details included. You can easily catch them and react to them accordingly.

## Current status

Currently, we support the following endpoints for the following services:

* DNS
    * [x] list_zones 100%
    * [x] list_zone_configs 100%
    * [x] list_records 100%
    * [x] delete_zone 100%
    * [ ] jobs_find 50% - missing official documentation, functionality cannot be guaranteed
    * [x] update_zone 100%
    * [x] get_default_nameserver 100%
* Domain
    * [x] list_domains 100%
    * [x] register_domain 100%
    * [x] jobs_find 100%
    * [x] list_contacts 100%
    * [ ] create_contact 0%
    * [ ] update_contact 0%
* Account
    * [ ] list_accounts 50% - missing official documentation, functionality cannot be guaranteed
    * [ ] get_own_account 50% - missing official documentation, functionality only implemented as far as required

We plan to add more endpoints in the future, for example for SSL and Domain services.

The implemented endpoints do not contain any logic to catch asynchronous behaviour yet. We plan to add a `sync: bool`
property to the corresponding endpoints in the future as soon as the jobs API is properly defined.

## Developing

Make sure that you satisfy the [requirements](#requirements). Checkout the project, then run

```shell
pip install -r requirements.txt 
pip install -r requirements-test.txt 
```

preferably in a virtual environment.

This will install all dependencies for the main project, as well as the dependencies used for testing.

### Testing

Run

```shell
pytest -vv --cov-report term-missing:skip-covered --cov=api --cov=utils --cov-report xml --html=test-results/report.html --cov-report html:test-results/cov
```

in order to test the code.

## Contributing

You can contribute to the project and add new endpoints that you need. However, in order to merge, we require:

* All implemented methods **MUST** be documented using reStructuredText notation.
* All implemented methods **MUST** be typed properly
* We require a test coverage of at least 90%, and your additions must not decrease the overall coverage of the codebase.
* We appreciate if you use [this](https://github.com/angular/angular/blob/master/CONTRIBUTING.md) commit message format.
