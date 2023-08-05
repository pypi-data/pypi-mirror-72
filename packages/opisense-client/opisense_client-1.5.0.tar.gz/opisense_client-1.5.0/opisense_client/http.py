from urllib.parse import urlencode
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
import opisense_client as oc
import requests
from .inputs import PATHS_TAGS, AUTHORIZATION_URL, API_URL, headers


def GET(opisense_token: str,
        api_filter,
        json_output=False,
        opisense_objects=False,
        feedback=False):
    """
    Get every Opisense Objects corresponding to the ApiFilter

    :param opisense_token: token needed to authorize the call. See "Authorize function"
    :param api_filter: ApiFilter object
    :param json_output: if True, returns the json object from the response
    :param opisense_objects: if True, returns a list of Opisense objects
    :param feedback: if True, prints HTTP status code in console
    :return:
    """
    headers['Authorization'] = opisense_token
    result = requests.get(API_URL + api_filter.path + '?' + urlencode(api_filter.filters, True), headers=headers)
    if feedback == True:
        print('Response: ' + str(result.status_code))

    if opisense_objects:
        objects = []
        try:
            object_type = PATHS_TAGS['/' + api_filter.path]

        except KeyError:
            raise KeyError('Cannot determine the object type, based on the API path')

        try:
            for object in result.json():
                objects.append(oc.OpisenseObject(object_type, object, id=object['id']))

            return objects

        except:
            raise ValueError('Cannot get output because No JSON is available in the response')

    if json_output:
        try:
            return result.json()
        except:
            raise ValueError('No JSON available in the HTTP response')

    else:
        return result


def POST(opisense_object=None,
         opisense_token: str = None,
         parent_id: int = None,
         force_path: str = None,
         feedback: bool = False) -> requests.Response:
    """
    Creates a new Opisense Object

    :param opisense_object: Opisense Object to create
    :param opisense_token: token needed to authorize the call. See "Authorize function"
    :param parent_id: parent object ID needed to create some objects type
    :param force_path: use a different path from the default one
    :param feedback: if True, prints HTTP response code in console
    :return: Http response
    """
    if not opisense_token:
        raise AttributeError('opisense_token missing')

    if force_path:
        path = force_path

    else:
        path = opisense_object.api_path

    json_object = opisense_object.json()
    headers['Authorization'] = opisense_token

    if opisense_object.type == 'variable':
        if parent_id:
            result = requests.post(API_URL + "variables/source/" + str(parent_id), headers=headers, data=json_object)
        else:
            raise ValueError('The parent sourceId is mandatory to create a variable')
    else:
        result = requests.post(API_URL + path, headers=headers, data=json_object)
    if feedback == True:
        print('Response: ' + str(result.status_code))
    return result


def PUT(opisense_object,
        opisense_token: str = None,
        parent_id: int = None,
        id: int = None,
        force_path: str = None,
        feedback=False) -> requests.Response:
    """
    Updates existing Opisense Object

    :param opisense_object: Opisense Object to update
    :param opisense_token: token needed to authorize the call. See "Authorize function"
    :param parent_id: parent object ID needed to update some objects type
    :param force_path: use a different path from the default one
    :param feedback: if True, prints HTTP response code in console
    :return: Http response
    """
    if not opisense_token:
        raise AttributeError('opisense_token missing')

    if force_path:
        path = force_path

    else:
        path = opisense_object.api_path

    json_object = opisense_object.json()
    headers['Authorization'] = opisense_token

    if opisense_object.id:
        object_id = opisense_object.id

    else:
        object_id = None

    if opisense_object.type == 'variable':
        if parent_id and object_id:
            result = requests.put(API_URL + "sources/" + str(parent_id) + "/variables/" + str(object_id),
                                  headers=headers,
                                  data=json_object)
        else:
            raise ValueError('The variableId and parent sourceId are mandatory to update a variable')
    else:
        if object_id:
            result = requests.put(API_URL + path + "/" + str(object_id), headers=headers,
                                  data=json_object)
        else:
            raise ValueError('The object id is mandatory to update an object')
    if feedback == True:
        print('Response: ' + str(result.status_code))
    return result


def DELETE(opisense_object=None,
           opisense_token: str = None,
           force_path: str = None,
           id: int = None,
           feedback=False) -> requests.Response:
    """
    Deletes existing Opisense Object

    :param opisense_object: Opisense Object to delete
    :param opisense_token: token needed to authorize the call. See "Authorize function"
    :param force_path: use a different path from the default one
    :param id: if opisense_object is not specified, this id will be used as http call parameter
    :param feedback: if True, prints HTTP response code in console
    :return: http response
    """
    if not opisense_token:
        raise AttributeError('opisense_token missing')

    if force_path:
        path = force_path

    else:
        path = opisense_object.api_path

    headers['Authorization'] = opisense_token

    if opisense_object.id:
        object_id = opisense_object.id

    elif id:
        object_id = id

    else:
        raise ValueError('The object id is mandatory to delete an object')

    result = requests.delete(API_URL + path + "/" + str(object_id), headers=headers)

    if feedback == True:
        print('Response: ' + str(result.status_code))
    return result


def authorize(user_credentials: dict, api_credentials: dict, feedback=False) -> str:
    """
    Gets Opisense Token

    :param user_credentials: dict containing 'client_id' , 'client_secret' and 'scope' keys
    :param api_credentials: dict containing 'username' and 'password' keys
    :param feedback: if True, prints HTTP response code in console
    :return: str : Opisense Token
    """
    client_id = api_credentials['client_id']
    client_secret = api_credentials['client_secret']
    scope = api_credentials['scope']
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
    token = oauth.fetch_token(token_url=AUTHORIZATION_URL,
                              scope=scope,
                              username=user_credentials['username'],
                              password=user_credentials['password'],
                              client_id=client_id,
                              client_secret=client_secret,
                              auth=None)
    access_token = 'Bearer ' + token['access_token']
    if feedback == True:
        api_filter = oc.ApiFilter('account')
        account = GET(access_token, api_filter).json()
        print('Got a valid token for the account ' + str(account['id']) + ' - ' + str(account['name']))
    return access_token
