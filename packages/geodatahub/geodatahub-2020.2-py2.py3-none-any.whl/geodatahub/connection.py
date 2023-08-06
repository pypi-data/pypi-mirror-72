#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Required for aws signature
import logging as lg

import requests
import urllib
import json

from .auth import GeodatahubAuth
from .models import Dataset

# Setup logging module
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.INFO)
LOG = lg.getLogger("geodatahub.Connection")


class Connection(object):

    def __init__(self,
                 token=None,
                 api_key=None,
                 backend_url='https://api.geodatahub.dk'):
        """Set up connection properties to GeoDataHub backend.

        Parameters
        ----------
        token: str, Optional
          Token used to provide user authentication against backend
        api_key: str, Optional
          An API key supplied by the backend
        backend_url: str, Optional
          URL to GeoDataHub backend
        """

        # Setup authentization header
        self._auth_headers = {}
        self._auth = GeodatahubAuth()
        self.set_token(token)

        if api_key is not None:
            self._auth_headers["x-api-key"] = api_key

        self._backend_url = backend_url
        self._host = "execute-api.amazonaws.com"
        self._region = "eu-west-1"
        self._service = "execute-api"

    @property
    def login_required(self):
        """Check if the user needs to login

        Returns
        --------
        login_required: bool
          False if the user is logged in else True
        """
        if self._auth.refresh_token is not None:
            return False
        else:
            return True

    def set_token(self, token = None):
        """Set the authentication token

        All communication with the backend needs to
        authenticate the user.

        Parameters
        ------------
        token : string
          Authentication token from the authentication module
        """
        if token is None:
            token = self._auth.get_access_token()

        self._auth_headers["Authorization"] = token

    def _call_endpoint(self, method, path, payload = None, reauth = True,
                       expect_json = True):
        """Call the API with a specific payload

        Parameters
        -----------
        method: str
          HTTP type of operations (GET, POST)
        path: str
          API endpoint to call (/datasets)
        payload: dict, Optional
          Parameters for the endpont
        reauth: bool
          Try to authenticate if request fails on first attempt
        expect_json: bool
          True if JSON is expected in the API response else False

        Returns
        ---------
        response: dict
          JSON reponse from the API or None if call failed
        """

        headers = self._auth_headers
        endpoint = urllib.parse.urljoin(self._backend_url, path)

        try:
            if method == "POST":
                if payload is not None:
                    resp = requests.post(endpoint,
                                         headers=headers,
                                         json=payload)
                else:
                    resp = requests.post(endpoint, headers=headers)
            else:
                resp = requests.get(endpoint, headers=headers)
        except Exception as e:
            # Hide token in header printout
            try:
                headers["Authorization"] = headers["Authorization"][:15] + "*******"
            except KeyError:
                # Ignore if Authorization is not in headers
                pass
            except TypeError:
                # Header was None
                pass

            msg = f"""\n
            The call failed for unknown reasons. The request was, \n
            endpoint: {endpoint}
            Type: {method}
            Payload: {payload}
            Headers: {headers}
            Raw library error: {e}
            """
            LOG.error(msg)
            return None

        if resp.status_code == 401 and \
           reauth:
            # Call was Unauthorized - Try to refresh the access token
            self._auth.refresh_auth()
            self.set_token()

            # Call API again with new tokens
            # Do not attempt reauthentication again
            return self._call_endpoint(method, path, payload,
                                       reauth = False, expect_json = expect_json)

        elif resp.status_code != 200:
            # Handle all errors except 401

            # Hide token in header printout
            try:
                headers["Authorization"] = headers["Authorization"][:15] + "*******"
            except KeyError:
                # Ignore if Authorization is not in headers
                pass
            except TypeError:
                # Header was None
                pass

            msg = f"""\n
            Status code: {resp.status_code}
            endpoint: {endpoint}
            Type: {method}
            Payload: {payload}
            Headers: {headers}
            respose: {resp.text}
            """
            LOG.error(msg)
            return None

        response = None
        if expect_json:
            try:
                response = resp.json()
                json.dump(response, open('/tmp/geolog.json', 'w'))
            except json.decoder.JSONDecodeError:
                LOG.error(f"Unable to decode response. Raw payload was {resp.text}")
                return None
        else:
            response = resp.text

        LOG.debug(f"""\n
        Status code: {resp.status_code}
        endpoint: {endpoint}
        Type: {method}
        Payload: {payload}
        Headers: {headers}
        Respose: {resp.text}
        Exec time: {resp.elapsed.total_seconds()}
        """)

        return response

    def ping(self):
        """Test connection to API

        This method calls the /ping endpoint. If
        the connection was successful True is returned
        otherwise the error message is written to the log
        and False is returned.

        Returns
        ------------
        response: bool
          If the connection was successful
        """
        if self._call_endpoint(method = "GET", path = "ping", expect_json = False) is None:
            return False
        return True

    def uploadDataset(self, dataset):
        """Upload metadata dataset via the API

        This method send the dataset encoded as JSON
        to the /datasets endpoint. If successful the
        newly created unique ID is returned by the API.

        Parameters
        ------------
        dataset: geodatahub.Dataset or list of geodatahub.Dataset
          Dataset object to upload

        Returns
        ----------
        dataset_id: list of str
          Unique identifiers for newly created datasets. On errors the id is None
        """

        # Wrap dataset to ensure the loop works
        # this will not affect lists
        dataset = list(dataset)
        dataset_ids = []

        # Send one dataset per request
        for d in dataset:
            if isinstance(d, dict):
                # Make dict to dataset object
                d = Dataset(**d)

            r = self._call_endpoint("POST", "datasets", payload=d.toJSON())

            try:
                dataset_ids.append(r["id"])
            except KeyError:
                # Response was malformed - None is returned
                dataset_ids.append(None)
        return dataset_ids

    def getDataset(self, uuid):
        """Returns datasets from the GeoDataHub backend by the unique id.

        Parameters
        -----------
        uuid: str
          Unique ID in UUIDv4 format

        Returns
        --------
        dataset: geodatahub.Dataset
          Dataset with matching UUID or None on error
        """

        r = self._call_endpoint(method = "GET", path = 'datasets/%s' % uuid)
        dataset=None
        try:
            dataset = Dataset(**r)
        except TypeError:
            LOG.error("Unable to decode response %s" % r)
        return dataset

    def listDatasets(self):
        """Returns a list of all datasets belonging to the user

        Returns
        --------
        dataset: list of geodatahub.Dataset
          List of Datasets
        """

        r = self._call_endpoint("GET", 'datasets')
        if r is None:
            raise RuntimeError("List was empty")
        elif len(r) == 0:
            return None

        datasets=[]
        try:
            for raw_dataset in r:
                datasets.append(Dataset(**raw_dataset))
        except Exception as err:
            LOG.error(f"""API returned: {r}
                          Raw error was: {err}
            """)
        return datasets

    def searchDataset(self, query = ""):
        """Returns datasets from the GeoDataHub backend by search parameters

        Parameters
        ------------
        query: str
          Search string. Eg. { "parameter": "value" }

        Returns
        --------
        datasets: list of geodatahub.Dataset
          Dataset(s) that matches the search. Empty on malformed response.
        """

        if query == "":
            # An empty search query should list all
            # datasets
            return self.listDatasets()

        # Dump dict to JSON and encode into url
        json_str = json.dumps(query)
        q = 'datasets?%s' % urllib.parse.urlencode({'q': json_str})
        LOG.debug(f"Performing search with query: {query}")
        r = self._call_endpoint("GET", q)
        datasets = []
        try:
            for dset in r:
                datasets.append(Dataset(**dset))
        except Exception as err:
            LOG.error(err)
        return datasets

    def get_schema_options(self, schema, key):
        """

        Parameters
        -----------
        search_filter: str
            Search filter to apply

        Examples
        ---------
        # Get all schemas from USGS
        >>> get_schema("*usgs*")

        # Get all well logs from GEUS
        >>> get_schema("*/well/usgs*")

        /category/type/org/version

        Note:
        ---------
        The schema may or may not contain a full URL.
        """

        if "http" not in schema:
            # Expect the user has typed the relative path without the extension
            schema = "https://schemas.geodatahub.dk/{schema}.json"
        q = 'schemas/autocomplete?schema=%s&key=%s' % (schema, key)
        LOG.debug(f"Performing schema lookup with query: {q}")
        r = self._call_endpoint("GET", q)
        return r
