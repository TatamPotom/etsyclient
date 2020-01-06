# ETSY client

ETSY API client for Python 3.x

This client is part of Zen-Commerce, order management application for online sellers.

https://zencommerce.app/

It's open source, license is GPL v3.0.

## Obtaining Etsy API keys

In order to use client and API you need to register on https://www.etsy.com/developers/documentation/getting_started/register

This gives you your API key and allows you to start working on your application. When your application is created, it starts with Provisional Access to our production systems to use during development.

Etsy will provide you with a Keystring and Shared secret to use with API.


    from client import EtsyClient
    client = EtsyClient(key=ETSY_KEYSTRING, secret=ETSY_SHARED_SECRET)

