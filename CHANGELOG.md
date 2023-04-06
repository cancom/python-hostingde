# Changelog

<!--next-version-placeholder-->

## v0.8.0 (2023-04-06)
### Feature
* Adds recordsUpdate endpoint ([#25](https://github.com/cancom/python-hostingde/issues/25)) ([`be922e3`](https://github.com/cancom/python-hostingde/commit/be922e3c82a5d1f72a0338aaa33aef32ce38cf0e))

## v0.7.2 (2023-01-03)
### Fix
* Removes responses from requirements ([#23](https://github.com/cancom/python-hostingde/issues/23)) ([`042ac4e`](https://github.com/cancom/python-hostingde/commit/042ac4e19abf0e254dd45b651bc19f6ca60a33ac))

## v0.7.1 (2022-10-24)
### Fix
* Adds account_id to domains model ([#21](https://github.com/cancom/python-hostingde/issues/21)) ([`8875185`](https://github.com/cancom/python-hostingde/commit/8875185ba06ef6930e951f061221e06e801e0ee1))

## v0.7.0 (2022-10-20)
### Feature
* Adds None as possible chainable target ([#20](https://github.com/cancom/python-hostingde/issues/20)) ([`daf077b`](https://github.com/cancom/python-hostingde/commit/daf077b0cd9e470797dce63938686b3a090265a7))
* Adds ability to paginate using the pages API which was originally hidden to the user ([`318d75c`](https://github.com/cancom/python-hostingde/commit/318d75c9064e83f1bc6e473f5938e5942a0c23c5))

## v0.6.0 (2022-10-17)
### Feature
* Adds check_domain_availability endpoint ([#17](https://github.com/cancom/python-hostingde/issues/17)) ([`76b63cd`](https://github.com/cancom/python-hostingde/commit/76b63cd2fb8153e9eaaf20cc3b215bfeb28858fa))

### Fix
* Fixes issue where wrong model is retrieved from backend ([#18](https://github.com/cancom/python-hostingde/issues/18)) ([`7e5fbbe`](https://github.com/cancom/python-hostingde/commit/7e5fbbe589c8b000e740558aa82402d4bcefbbfe))

## v0.5.0 (2022-10-04)
### Feature
* Adds domain endpoints ([#16](https://github.com/cancom/python-hostingde/issues/16)) ([`afb488b`](https://github.com/cancom/python-hostingde/commit/afb488b076e9c6bb8710e95045aee96d9f641738))

### Documentation
* Installation instruction and badges ([#14](https://github.com/cancom/python-hostingde/issues/14)) ([`575741c`](https://github.com/cancom/python-hostingde/commit/575741c559387478383aa1fa04a0db973ee55fb7))

## v0.4.2 (2022-06-30)
### Fix
* Paginator.fetchone() now returns None instead of a ClientException at the end of the iteration ([#13](https://github.com/cancom/python-hostingde/issues/13)) ([`dc94eee`](https://github.com/cancom/python-hostingde/commit/dc94eee54e765682f87ac631d7ae787253dab19a))

## v0.4.1 (2021-11-21)
### Fix
* Renames zone_id to zone_config_id in Record model ([#11](https://github.com/cancom/python-hostingde/issues/11)) ([`45f4678`](https://github.com/cancom/python-hostingde/commit/45f46781b3070041252cc420552140181f08e784))

## v0.4.0 (2021-11-19)
### Feature
* Adds support for record comments ([#10](https://github.com/cancom/python-hostingde/issues/10)) ([`1dc5eaa`](https://github.com/cancom/python-hostingde/commit/1dc5eaa73b387760c90396b63e187e3f54f880cf))

## v0.3.0 (2021-11-09)
### Feature
* **dns:** Adds support for dnsServerGroupId ([#9](https://github.com/cancom/python-hostingde/issues/9)) ([`aa66e75`](https://github.com/cancom/python-hostingde/commit/aa66e7526bd17c5a13f76780b8f5ff81c89332a6))

## v0.2.1 (2021-11-09)
### Fix
* Use valid pypi classifier ([`25e4d70`](https://github.com/cancom/python-hostingde/commit/25e4d708c6a9eed7b347a53b65b1f80cf7cb8548))

## v0.2.0 (2021-11-09)
### Feature
* Adds client dependency injection to model ([#8](https://github.com/cancom/python-hostingde/issues/8)) ([`07a9d52`](https://github.com/cancom/python-hostingde/commit/07a9d525d6adfa6490a31794adabd20eeafc2a19))

## v0.1.0 (2021-11-07)
### Feature
* Initial release ([`84cd33d`](https://github.com/becelot/python-hostingde/commit/84cd33d3ae0303ae5078c98f1b971c6705462edf))

### Documentation
* Codecov badge ([`3e9f9d1`](https://github.com/becelot/python-hostingde/commit/3e9f9d16389e110b67bc6e64bac80a55bfdd3160))
* Adds readme ([`4680c73`](https://github.com/becelot/python-hostingde/commit/4680c7310a9c67e1005e5a2a8ff64a4c2cb1cca7))
