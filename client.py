"""
ETSY API client for Python 3.x

This client is part of Zen-Commerce, order management application for online sellers.
https://zencommerce.app/

It's open source, license is GPL v3.0.

Use it at your own fun.
"""

from requests_oauthlib import OAuth1Session


class EtsyClient(object):
    """
    Client class
    """
    uri = ""
    etsy_id = ""

    oauth_token = ""
    oauth_token_secret = ""
    verifier = ""

    ETSY_API_URI = "https://openapi.etsy.com/v2/"
    ETSY_KEYSTRING = ""
    ETSY_SHARED_SECRET = ""

    def __init__(self, key, secret):
        self.ETSY_KEYSTRING = key
        self.ETSY_SHARED_SECRET = secret

    def get_queue(self):
        """
        Returns RQ queue
        """
        return Queue(connection=conn)

    def get_oauth(self):
        """
        Returns OAUTH v1 session
        """
        return OAuth1Session(self.ETSY_KEYSTRING,
            client_secret=self.ETSY_SHARED_SECRET,
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_token_secret)

    def request_etsy_token(self):
        """
        OAUTH v1 Step 1 - get request tokens (temporary)
        https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html
        """

        oauth = OAuth1Session(self.ETSY_KEYSTRING,
            client_secret=self.ETSY_SHARED_SECRET)
        response = oauth.fetch_request_token(
            self.ETSY_API_URI + 'oauth/request_token')

        if not 'login_url' in response:
            raise Exception(str(response))

        self.oauth_token = response['oauth_token']
        self.oauth_token_secret = response['oauth_token_secret']
        self.verifier = ""
        self.save()

        return response

    def store_access_request(self, verifier):
        """
        OAUTH v1 Step 3
        Store permanent tokens from ETSY in DB to use later.
        """

        oauth = OAuth1Session(self.ETSY_KEYSTRING,
            client_secret=self.ETSY_SHARED_SECRET,
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_token_secret,
            verifier=verifier)

        # Fetch non-expiring tokens
        response = oauth.fetch_access_token(
            self.ETSY_API_URI + 'oauth/access_token')

        if 'oauth_token' in response:
            self.oauth_token = response['oauth_token']
            self.oauth_token_secret = response['oauth_token_secret']
            self.verifier = verifier
            self.save()

            response2 = self.get_etsy_response('shops/__SELF__')
            if 'results' in response2.json():
                self.etsy_id = response2.json()['results'][0]['shop_id']
                self.save()

        return True

    def get_etsy_response(self, method):
        """
        Get API response, reference:
        https://www.etsy.com/developers/documentation/getting_started/oauth
        Examples:
         - oauth/scopes
         - users/__SELF__
         - shops/__SELF__

         Please note response.headers['X-RateLimit-Remaining']
        """
        return self.get_oauth().get(settings.ETSY_API_URI + method)
