import os
import pathlib
from urllib.parse import urlparse, parse_qs
import requests
import json
import re
import logging as lg

# Regex to ensure one-time code is formatted correctly
UUID4HEX = re.compile("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)

# Setup logging module
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.INFO)
LOG = lg.getLogger("geodatahub.Auth")

class GeodatahubAuth():
    def __init__(self):
        # Tokens
        self.access_token = None
        self.id_token = None
        self.refresh_token = None

        # Load existing authentication information
        self._redirect_url, self._app_id, self._base_url, self.auth_url = self.get_login_settings()
        self.get_stored_token()

    def get_login_settings(self, profile_name = "cli"):
        """Contact the API to get login settings

        Get login settings directly from the URL.

        Parameters
        -----------
        profile_name: str
            Name of the profile to get settings for

        Returns
        -------
        redirect_url: str
           Url to redirect to once login is complete
        app_id: str
            Unique ID for app
        base_url: str
            URL used to login
        auth_url: str
            The full URL used to sign in
        """
        # Login constants
        try:
            login_resp = requests.get("https://api-dev.geodatahub.dk/login")
            login_settings = login_resp.json()["message"][profile_name]#["settings"]
            print(login_settings)
        except KeyError:
            LOG.error(f"The profile {profile_name} does not exist")
            return None, None, None, None
        except Exception as err:
            LOG.error(f"Failed to get login settings from API. Error was {str(err)}")
            return None, None, None, None
        else:
            response_type = login_settings["response_type"]
            redirect_url  = login_settings["redirection_url"]
            app_id        = login_settings["app_id"]
            base_url      = login_settings["url"]

            auth_url = "{base_url}/login?response_type={resp_type}&client_id={app_id}&redirect_uri={redirect_url}".format(app_id = app_id,
                                                                                                                          redirect_url = redirect_url,
                                                                                                                          base_url = base_url,
                                                                                                                          resp_type = response_type)
            return redirect_url, app_id, base_url, auth_url

    def get_stored_token(self, token_path = None):
        """Load a previously stored token

        The token is first read from the environmental variables
        GDH_REFRESH_TOKEN. If not found then the .gdh folder in
        the users home directory is attempted.

        If no token is found is will be None.

        Parameters
        -----------
        token_path: str
            Absolute path to the access token

        Returns
        ---------
        token (str): The stored refresh token or None
        """
        if self.refresh_token is not None:
            # Get token from class if it exists
            return self.refresh_token

        token = os.getenv("GDH_REFRESH_TOKEN")
        if token is not None:
            # Get token from environmental variable if set
            self.refresh_token = token
            return token

        if token_path is None:
            token_path = os.path.join(pathlib.Path.home(), ".gdh/authentication")

        # Load token from file system
        if os.path.exists(token_path):
            with open(token_path) as f:
                try:
                    # Last attempt is to get the token from disk
                    auth_config = json.load(f)
                    self.refresh_token = auth_config["refresh_token"]
                    return self.refresh_token
                except KeyError:
                    # The key did not exist
                    pass

        # If no token was found
        return None

    def store_token(self, token = None, location = None):
        """Save authentication tokens for later use

        The tokens are stored in environmental variables
        GDH_REFRESH_TOKEN and the .gdh folder in
        the users home directory (if the user has
        not set a custom path).

        Parameters
        -----------
        token: str, Optional
            Token to store. Default is the current active refresh token.
        location: str, Optional
            Only store token in a specifc location (envvar or disk).
            Default both,
        """
        if token is None and self.refresh_token is None:
            # No token exists to store
            LOG.warning("No token exists to store. Please login and try again.")
        elif token is None:
            # Use token from class
            token = self.refresh_token

        if location == "envvar" or location is None:
            os.environ["GDH_REFRESH_TOKEN"] = token

        if location == "disk" or location is None:
            # Store a test token in the file
            conf_path = os.path.join(pathlib.Path.home(), ".gdh")

            # Create folder if it does not exist
            try:
                pathlib.Path(conf_path).mkdir()
            except FileExistsError:
                pass

            with open(os.path.join(conf_path, "authentication"), 'w') as f:
                json.dump({"refresh_token":token}, f)

    def get_access_token(self):
        """Load or acquire an access token

        Returns
        --------
        access_token: str
            Valid access token
        """
        # The token is already aquired
        if self.id_token is not None:
            return self.id_token

        # Ensure the user has logged in
        if self.get_stored_token() is None:
            # Force the user to login
            raise RuntimeError("No user logged in. Cannot continue.")

        # Get a fresh token from the backend
        token, _, _ = self.refresh_auth()
        return token

    def login(self, code = None):
        """Authenticate using one-time code

        Users are expected to retrieve an one-time code
        by visiting www.geodatahub.dk/login in their browser
        and going though the login process.

        Parameters
        ------------
        code: str
          One-time code from a OAuth2 authorization code flow

        Returns
        ---------
        access_token: str
          Token that contains claims about the authenticated user
        refresh_token: str
          Token used to reauthenticate the user without password
        id_token: str
          Token that contains claims about the identify of the user

        Raises
        -------
        RuntimeError:
          If the authentication response did not contain the expected
          parameters.
        """
        if UUID4HEX.match(code) is None:
            # The one-time did not have the required format
            # Reset all tokens to be sure the user does not end in an authentication loop
            self.refresh_token, self.id_token, self.access_token = None, None, None
            raise RuntimeWarning(f"The one-time code is not formatted correctly. Code was {code}")

        # Trade code for token
        payload = {
            'grant_type':'authorization_code',
            'client_id':self._app_id,
            'code':code,
            'redirect_uri': self._redirect_url
        }

        auth_url = "{base_url}/oauth2/token".format(base_url = self._base_url)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        resp = requests.post(auth_url, data=payload, headers=headers)

        jresp = resp.json()
        try:
            self.access_token = jresp["access_token"]
            self.refresh_token = jresp["refresh_token"]
            self.id_token = jresp["id_token"]
        except KeyError:
            msg = "The login did not succeeded"
            if "error" in jresp:
                if jresp["error"] == "invalid_grant":
                    msg = f"""The one-time code {code} has already been used. \
                    Please obtain a new code."""
                elif jresp["error"] == "unauthorized_client":
                    msg = f"""The one-time code {code} is not authorized at this endpoint. \
                    Please ensure you are not using the development environment."""
                elif jresp["error"] == "invalid_client":
                    msg = f"""You cannot login to that domain with id {self._app_id}. Please contact support@geodatahub.dk."""

            self.refresh_token, self.id_token, self.access_token = None, None, None
            LOG.error(msg)
            LOG.debug('POST to ' + auth_url +
                      ' was not successfull ' +
                      '(HTTP status code: ' + str(resp.status_code) +
                      ')\n\nHeader was:\n' + json.dumps(headers) +
                      ')\n\nPayload was:\n' + json.dumps(payload) +
                      ')\n\nServer response:\n' + json.dumps(jresp))
            raise RuntimeError()

        return self.access_token, self.refresh_token, self.id_token

    def refresh_auth(self, refresh_token = None):
        """Re-authenticate with backend

        Parameters
        -----------
        refresh_token: str, optional
          Token from a previous authentication. If no token is given the
          class refresh token will be used if it exists.

        Returns
        ---------
        access_token: str
          Token that contains claims about the authenticated user
        refresh_token: str
          Token used to reauthenticate the user without password
        id_token: str
          Token that contains claims about the identify of the user

        Raises
        --------
        RuntimeError:
          If a non-recoverable event happened. This would be an unexpected
          response from the authentication step.
        """
        if refresh_token is None:
            refresh_token = self.get_stored_token()
        if refresh_token is None:
            raise RuntimeError("You must first login before you can call the API")

        # The request should be sent directly to this URL
        auth_url = "https://cognito-idp.eu-west-1.amazonaws.com/"
        headers = {
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "Content-Type": "application/x-amz-json-1.1",
        }
        payload = {
            "ClientId": self._app_id,
            "AuthFlow": "REFRESH_TOKEN_AUTH",
            "AuthParameters": {
                "REFRESH_TOKEN": refresh_token
            }
        }

        resp = requests.post(auth_url, json=payload, headers=headers)
        jresp = resp.json()

        try:
            self.access_token = jresp["AuthenticationResult"]["AccessToken"]
            self.id_token = jresp["AuthenticationResult"]["IdToken"]
        except KeyError:
            msg = f"""\n
            Re-authentication failed with response,

            Status code: {resp.status_code}
            endpoint: {auth_url}
            Type: POST
            Payload: {payload}
            Headers: {headers}
            respose: {resp.text}
            """
            LOG.error(msg)
            # mark all tokens as invalid
            self.refresh_token, self.id_token, self.access_token = None, None, None

        # Parse along exist refresh token to keep interface consistent
        return self.access_token, self.refresh_token, self.id_token

    def _sign_with_sig4(self, method, path):
        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        # Create a date for headers and the credential string
        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

        # Step 1 is to define the verb (GET, POST, etc.)--already done.
#        method = "GET"

        # Step 2: Create canonical URI--the part of the URI from domain to query 
        # string (use '/' if no path)
        canonical_uri = path
        
        # Step 3: Create the canonical query string. In this example (a GET request),
        # request parameters are in the query string. Query string values must
        # be URL-encoded (space=%20). The parameters must be sorted by name.
        # For this example, the query string is pre-formatted in the request_parameters variable.
        canonical_querystring = ""#request_parameters
        
        # Step 4: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note that there is a trailing \n.
        canonical_headers = 'host:' + self._host + '\n' + 'x-amz-date:' + amzdate + '\n'
        
        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the 
        # hash of the request. "Host" and "x-amz-date" are always required.
        signed_headers = 'host;x-amz-date'
        
        # Step 6: Create payload hash (hash of the request body content). For GET
        # requests, the payload is an empty string ("").
        payload_hash = hashlib.sha256(('{}').encode('utf-8')).hexdigest()
        
        # Step 7: Combine elements to create canonical request
        canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use, either SHA-1 or
        # SHA-256 (recommended)
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' + self._region + '/' + self._service + '/' + 'aws4_request'
        string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        
        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = getSignatureKey(self._access_key, datestamp, self._region, self._service)
        
        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # The signing information can be either in a query string value or in 
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        authorization_header = algorithm + ' ' + 'Credential=' + self._access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
        
        # The request can include any headers, but MUST include "host", "x-amz-date", 
        # and (for this scenario) "Authorization". "host" and "x-amz-date" must
        # be included in the canonical_headers and signed_headers, as noted
        # earlier. Order here is not significant.
        # Python note: The 'host' header is added automatically by the Python 'requests' library.
        auth_headers = {'x-amz-date':amzdate,
                        'Authorization':authorization_header}

        return auth_headers

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning
