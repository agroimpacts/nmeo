from base64 import b64encode
import requests

class ArableClient(object):
    """ A client for connecting to Arable and making data queries.

        >>> from arable.client import ArableClient
        >>> client = ArableClient()
        >>> client.connect(email='user@loremipsum.com', password='#@#SS')

    """
    _base_url = "https://api-user.arable.cloud/api/v2"

    def __init__(self):
        self.token = None
        self.user_id = None
        self.tenants = None
        self.apikey = None
        self.basic = None
        self.status = None
        self.message = None

    def _login(self, email=None, password=None):
        # First, see if this is a legit user.  
        url = "{0}/auth/token".format(ArableClient._base_url)
        basic = b64encode("{0}:{1}".format(email, password).encode('utf-8')).decode('utf-8')
        headers = {"Authorization": "Basic " + basic}
        data = {"email": email, "password": password}

        r = requests.post(url, data=data)
        if r.status_code == 200:
            user_id = r.json()['user_id']
            token = r.json()['token']
        else:
            message = r.json()['message']
            status = r.status_code
            response = {'message': message, 'status': status}
            return response
            
        print('logged in')
        # You are more than welcome to find out their name and other stats (currently not used)
        url = "{0}/users/email/{1}".format(ArableClient._base_url, email)
        headers = {"Authorization": "Basic " + basic}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            pass
        else:
            message = r.json()['message']
            status = r.status_code
            response = {'message': message, 'status': status}
            return response


        # Next, find out what tenants this user is authorized to see
        url = "{0}/users/{1}/orgs".format(ArableClient._base_url, user_id)
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            tenants = [tenant['tenant'] for tenant in r.json()]
        else:
            message = r.json()['message']
            status = r.status_code
            response = {'message': message, 'status': status}
            return response


        # Finally, get the apikey
        url = "{0}/apikeys".format(ArableClient._base_url)
        headers = {"Authorization": "Basic " + basic}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            apikeys = r.json()
        else:
            message = r.json()['message']
            status = r.status_code
            response = {'message': message, 'status': status}
            return response

           
        # make an apikey if it doesn't exist
        if len(apikeys) == 0:
            url = "{0}/apikeys".format(ArableClient._base_url)
            headers = {"Authorization": "Basic " + basic}
            data = {
                    "scopes": ["data:read"],
                    "name": "data apikey",
                    "exp": "2020-12-31T23:59:59Z"
                  }

            r = requests.post(url, headers=headers, json=data)
            print(r.status_code, r.json())
            if r.status_code == 200:
                apikeys = r.json()
            else:
                r.raise_for_status()

        apikey = ''
        for i in range(len(apikeys)):
            if apikeys[i]['name'] == 'data apikey':
                apikey = apikeys[i]['apikey']            
            
        response = {'token': token, 'user_id': user_id, 'tenants': tenants, 'apikey': apikey, 'basic': basic, 'status': 200, 'message':''}
        return response

    def connect(self, email=None, password=None):
        """ Logs the client in to the API.

            :param email: user email address
            :param password: user password
            :param tenant: user's tenant name

            >>> client.connect(email='test@loremipsum.com', password='$#$!%')

        """
        if not all([email, password]):
            raise Exception("Missing parameter; connect requires email and password")
        try:
            response = self._login(email=email, password=password)
            self.status = response['status']
            self.message = response['message']
            if self.status == 200:
                self.user_id = response['user_id']
                self.tenants = response['tenants']
                self.apikey = response['apikey']
                self.token = response['token']
                self.basic = response['basic']
        except Exception as e:
            print("Failed to connect:\n{}".format(str(e)))
            raise Exception("Failed to connect:\n{}".format(str(e)))
