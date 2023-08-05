import json
import datetime
import requests
from opisense_client.http import *
from .inputs import STANDARD_PUSH_DATA_URL


class ApiFilter:
    def __init__(self, path: str, **filters):
        """
        Builds a filter object used to set the parameters to request data from Opisense API. To use date filters 'from' and 'to', use 'date_from' and 'date_to'
        :param path: API path
        :param filters: filters to be applied to the GET request
        """
        self.path = path
        if 'date_from' in filters.keys():
            filters['from'] = filters.pop('date_from')
        if 'date_to' in filters.keys():
            filters['to'] = filters.pop('date_to')

        _ = {}
        for filter in filters:
            _[filter] = filters[filter]
        self.filters = _

    def __add__(self, **filters):
        """
        Add parameters to the API filter. To add date filters 'from' and 'to', use 'date_from' and 'date_to'
        :param filters: parameters to add
        """
        if 'date_from' in filters.keys():
            filters['from'] = filters.pop('date_from')
        if 'date_to' in filters.keys():
            filters['to'] = filters.pop('date_to')

        for filter in filters:
            self.filters[filter] = filters[filter]


class DataPoints:
    def __init__(self, date: datetime = None, value: float = None, datapoints_list=None):
        """
        Builds a standard datapoint list to build a StandardData object
        :param date: datetime object
        :param value: floating point value
        :param datapoints_list: *args [{date : datetime, value : float}] to initialize the object based on a list of dict
        """
        if not date and not value and not datapoints_list:
            raise ValueError('date and value or datapoints_list must be defined')

        if date and value:
            date = date.strftime('%Y-%m-%dT%H:%M:%S%z')
            self.list = [{'date': date, 'value': value}]
        else:
            self.list = []
        if datapoints_list:
            for datapoint in datapoints_list:
                date = datapoint['date'].strftime('%Y-%m-%dT%H:%M:%S%z')
                self.list.append({'date': date, 'value': datapoint['value']})

    def __add__(self, date: datetime = None, value: float = None, datapoints_list=None):
        """
        Add datapoints to
        :param date: datetime object
        :param value: floating point value
        :param datapoints_list: *args [{date : datetime, value : float}] to initialize the object based on a list of dict
        """
        if not date and not value and not datapoints_list:
            raise ValueError('date and value or datapoints_list must be defined')

        if date and value:
            date = date.strftime('%Y-%m-%dT%H:%M:%S%z')
            self.list.append({'date': date, 'value': value})

        if datapoints_list:
            for datapoint in datapoints_list:
                date = datapoint['date'].strftime('%Y-%m-%dT%H:%M:%S%z')
                self.list.append({'date': date, 'value': datapoint['value']})

    def to_json(self):
        """
        Convert the datapoints list to JSON
        :return: JSON
        """
        return json.dumps(self.list)


class StandardData:
    def __init__(self, datapoints: DataPoints, sourceId=None, sourceSerialNumber=None, meterNumber=None,
                 sourceEan=None, mappingConfig=None, variableId=None):
        """
        Builds a StandardData object to be pushed to Opisense API.
        At least one of the optionals args must be present.
        :param datapoints: DataPoint object
        :param sourceId: optional : Opisense Source internal identifier
        :param sourceSerialNumber: optional : Opisense Source Serial Number
        :param meterNumber: optional : Opisense Source Meter Number
        :param sourceEan: optional : Opisense Source EAN Number
        :param mappingConfig: optional : Opisense Variable Mapping
        :
        """
        if sourceId or sourceSerialNumber or sourceEan or meterNumber and mappingConfig:
            args = {}
            args['sourceId'] = sourceId
            args['sourceSerialNumber'] = sourceSerialNumber
            args['meterNumber'] = meterNumber
            args['sourceEan'] = sourceEan
            args['mappingConfig'] = mappingConfig
            args['data'] = datapoints.list
            self.list = [args]
            self.json = json.dumps(self.list)
        elif variableId:
            args = {}
            args['variableId'] = variableId
            args['data'] = datapoints.list
            self.list = [args]
            self.json = json.dumps(self.list)

        else:
            raise ValueError(
                'At least one of the optional source parameters + mapping config or just the variableId is mandatory')

    def POST(self, opisense_token: str, feedback=False):
        """
        POST the StandardData object to the Opisense API
        :param opisense_token: Opisense Bearer token
        :param feedback: if feedback = True, returns the http response code
        :return:
        """
        result = requests.post(STANDARD_PUSH_DATA_URL,
                               data=self.json,
                               headers={"Authorization": opisense_token,
                                        "Content-Type": "application/json"})
        if feedback == True:
            print('Response: ' + str(result.status_code))
        return result


class OpisenseObject:
    def __init__(self, type: str, opisense_object: dict, id=None):
        """
        Creates an Opisense Object
        :param type: Opisense object type (site, gateway, source, variable, form,...)
        :param opisense_object: dictionary containing the Opisense structure for this object type
        :param id:optional : Opisense internal object ID
        """
        super().__setattr__('id', id)
        super().__setattr__('content', opisense_object)
        super().__setattr__('type', type.lower())
        super().__setattr__('api_path', self.type + 's')
        # self.id = id
        # self.type = type.lower()
        # self.content = opisense_object
        # self.api_path = self.type + 's'

    def __getattr__(self, item):
        return self.content.get(item)

    def __setattr__(self, key, value):
        if key not in ['id','content','type','api_path']:
            self.content[key] = value

        else:
            super().__setattr__(key,value)

    POST = POST
    PUT = PUT
    DELETE = DELETE

    def json(self):
        """
        Serialize the object in JSON
        :return: JSON
        """
        return json.dumps(self.content)
