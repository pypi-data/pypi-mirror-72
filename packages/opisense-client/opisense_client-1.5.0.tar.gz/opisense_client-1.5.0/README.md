# opisense_client
Python package providing some functions to interact with the Opisense API.  
More info about Opisense here: https://www.opinum.com/   
Opisense API is described here: https://docs.opinum.com/restapi/index.html 

## Getting started
These instructions will guide you through the process of getting you ready to use the opisense_client package

### Prerequisites
#### 1. Get an Opisense account.
Contact info@opinum.com or see www.opinum.com to get an account

#### 2. Get Opisense API credentials.
Contact support@opinum.com to get an API secret and API key

#### 3. Install opisense_client package
You can install opisense_client by typing `pip install opisense-client` in your terminal.

### Configuration
#### Credentials file
Although you can define a dictonary containing your credentials in you script, it is more secure to store them in a separate file.  
The file should be a .JSON format and the expected format is the following :  
```json
{  
  "user": {
    "username": "xxxxxxx",
    "password": "xxxxxxx"
  },
  "api": {
    "client_secret": "xxxxxx",
    "client_id": "xxxxxx",
    "scope":"opisense-api push-data"
  }
}
```
The `xxxxxx` should be replaced by your own credentials (see Prerequisites 1. and 2.)

The following code will read the file and store data in a Python dictionary :  
```python
import json
with open('path/to/your/file/credentials.JSON', encoding='utf-8') as file:  
    credentials = json.load(file)  
user_credentials = credentials['user']  
api_credentials = credentials['api']  
```
`path/to/your/file/` is the local path to your credentials file and `credentials.JSON` is the filename. 

### Functionalities
#### root  
* **change_urls**:   
This function adapts the API URLs.  
The optional *api_url* sets a new API URL
The optional *authorization_url* sets a new AUTHORIZATION URL
The optional *standard_push_data_url* sets a new STANDARD PUSH DATA URL
  

#### objects  
* **ApiFilter**:  
This object contains the API path and a dictionary containing all the filters names and values used to querry Opisense database via an http call to the API. This call is described under [http](#http) section.  
This is only used is input for the `http.GET()` method.
See [Opisense API documentation](https://docs.opinum.com/restapi/index.html) for details on the path and filters availables for each type of Opisense Entities.  
The `__add__` method of this class allows adding filters names and values to the existing ApiFilter object. 

* **DataPoints**:
This object contains pairs of datapoints datetimes and values to be used in the [StandardData](#StandardData) object construction.   
The `__add__` method of this class allows adding datapoints datetimes and values to the existing ApiFilter object.

* **StandardData**:
This object contains a [DataPoints](DataPoints) object and the relevant parameters to identify strictly one Opisense Variable that will store the datapoints. 
A combinaison of these optionals parameters can be used to identify the variable : *sourceId, sourceSerialNumber, meterNumber, sourceEan, mappingConfig*. An other option is to use the internal id of the Opisense variable: *variableId*.  
The `POST` method of this class takes a bearer token as argument and uploads the StandardData object to Opisense API, using the http POST method.  

* **OpisenseObject**:
This object is a generic Opisense Object taking a type string and a dictionary containing all the Opisense parameters related to this kind of object. See [Opisense API documentation](https://docs.opinum.com/restapi/index.html) for more details on Opisense Objects.  
The `POST`, `PUT` and `DELETE` methods of this class take a bearer token as argument and uploads the StandardData object to Opisense API, using the appropriate http method.  
The `json` method of this function returns the object contain, serialized in JSON, using the built-in [json](https://docs.python.org/3/library/json.html) method.

#### http
* **authorize**:   
This function takes user credentials and api credentials dictionaries as input and returns the OAuth2 bearer token required to interract with Opisense API.  
The optional *feedback* argument returns in the console the Opisense account name and ID for which you got a token.
  
* **GET**:   
This function takes a bearer token and an ApiFilter object as inputs, perform an http call using GET method to Opisense API to get every element matching the filter and returns the response from the server.  
The optionnal *json_output* argument changes the output to the json content of the server response.  
The optional *feedback* argument returns the server response code in the console.
The optionnal *opisense_object* argument changes the output to a list of Opisense Objects created from the json response.
  
* **POST**:  
This function takes a bearer token and an OpisenseObject as inputs, creates the elements in Opisense database using the API POST method and returns the response from the server.  
The *parent_id* argument is necessary to create some type of OpisenseObjects. See [Opisense API documentation](https://docs.opinum.com/restapi/index.html) for details.  
The optional *feedback* argument returns the server response code in the console.  
The optional *path* argument allows to change the default path appended to the url in the POST call.
The optional *force_path* argument allows to use a path not in the default list.
  
* **PUT**:  
This function takes a bearer token and an OpisenseObject as inputs, updates the elements in Opisense database using the API PUT method and returns the response from the server.  
The *parent_id* argument is necessary to update some type of OpisenseObjects. See [Opisense API documentation](https://docs.opinum.com/restapi/index.html) for details.  
The optional *feedback* argument returns the server response code in the console.
The optional *path* argument allows to change the default path appended to the url in the POST call.
The optional *force_path* argument allows to use a path not in the default list. 
 
* **DELETE**:  
This function takes a bearer token and an OpisenseObject as inputs, deletes the elements in Opisense database using the API DELETE method and returns the response from the server.  
The optional *feedback* argument returns the server response code in the console.  
The optional *path* argument allows to change the default path appended to the url in the POST call.
The optional *force_path* argument allows to use a path not in the default list.

### Objects and Methods description
Every object and method is described with docstrings. You can easily access it by running `help(method)`

## Tests
The tests are located in `.\opisense_client\tests\tests.py`. To run the tets, do the following: 
1. Install pytest: `pip install pytest`
2. From the root folder of this repos, run `pytest .\opisense_client\tests\tests.py -vv`


## Changelog
### 1.5.0:
#### Features:
- Allow to use other URLs than default ones

### 1.4.0:
#### Fixes:
- Remove the header "X-Opisense-Api-Version": "1.1" from http calls, to allow using the last version of the Opisense API.
- Remove the `path` argument added in v1.3.0 as it was leading to some new errors. `force_path` from `PUT()`,`POST()` and `DELETE()` functions now accepts strings overriding default path.  

#### Features:
- Add getter and setter to OpisenseObjects to allows getting and setting objects attributes by dot notation. (i.e.: source.siteId give the same result as source.content['siteId'])
- Make `opisense_object` optional for `POST` and `DELETE` functions. Add `id` argument to `DELETE` function to enter the Opisense internal Id to delete.

### 1.3.0:
#### Fixes:  
- Add a rule to allow `from` and `to` filters in `ApiFilter` without interfering with python `from` reserved word. The arguments `date_from` and `date_to` are automatically converted to `from` and `to` filters in the object initialization.  
- Add a `path` argument and update the `force_path` argument to `PUT()`,`POST()` and `DELETE()` functions, to allow the usage of non-standard paths. 

### 1.2.1:
#### Fixes:  
Fix import problem

### 1.2.0:
#### Features:  
Add `opisense_object` option to `http.GET()` function. This option  changes the output to a list of Opisense Objects created from the json response. 

### 1.1.2:
#### Fixes:  
Fix StandardData object bug, using mapping_config instead of variableId to build the object.   


### 1.1.0: 
#### Features:  
Add datapoints_list as optional input for DataPoints Objects. Allows to create a DataPoints object from a list of dictionaries `[{'date':datetime,'value':float}]`

### 1.0.2: 
#### Fix auth bug linked to oauth lib library update
set `auth = None` in `oauth.fetch_token()` in http.py to avoid getting an 'invalid_client' error

### 1.0.0: 
#### First stable version
#### StandardData
Added variableId as unique identifier option

#### Documentation
Updated README.MD and documented every object and method

### 0.3:
#### force_path 
Added force_path optional parameter to http.POST and http.PUT. 
Overwrites the default OpisenseObject.api_path in the http call.

#### json_output
Added json_output optional parameter to http.GET
If True, Returns the JSON object from the http response if available.
