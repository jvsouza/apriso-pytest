# Pytest on DELMIA APriso

## Main goal
> Use pytest as a unit testing tool in DELMIA Apriso

## Prerequisites
- [Pip](https://pypi.org/project/pip)
- [Python 3+](https://www.python.org)
- [Vitrualenv](https://virtualenv.pypa.io/)

## Installation
1. [Clone](https://github.com/jvsouza/unit_test_delmia_apriso.git) or [download](https://github.com/jvsouza/unit_test_delmia_apriso/archive/refs/heads/main.zip) the repository;
2. Create virtual environment ( virtualenv venv );
3. Install the list of packages using `requirements.txt` ( pip install -r requirements.txt ).

## Folder summary and file structure
```texto
unit_test
├── .gitignore
├── config.ini
├── main.py
├── README.md
├── requirements.txt
└── test_operation.py
```

## Instructions
Configure webservice parameters for unit tests in config.ini.
<pre lang="ini">
[basic]
    debug = true
    protocol = http
    ws_path_rest = Apriso/httpServices/operations
    ws_path_soap = Apriso/WebServices/Public

[server]
    host = TCSVL1D125

[webservice]
    ws_type = REST
    ws_name = unitTestREST
</pre>

Validate the availability of the webservice resource for unit testing.
If the webservice is unavailable, unit testing will not be possible.
Webservice validation can be done in the webservice tester available in the DELMIA Apriso webservices manager.

Prepare your unit test.
You will need know name operation.
You will need know input external required by operation
And you will need know outputs extenal if exist, by other verfication

## Test 
Run just pytest in the project root to execute all files initing with test_:
```bash
$ pytest
```
Or run pytest test_something, to run only the specific file.
```bash
$ pytest test_something
```

## Test the webservice from POSTMan
> using REST, the `content-type` parameter must be `application/json`
```json
{
    "Inputs": {
        "EncodedParameters": "{ 'EmployeeNo': 'jonas' }",
        "OperationName": "TEST_PY"
    }
}
```

> using SOAP, the `content-type` parameter must be `application/soap+xml`
```xml
<soap:Envelope  xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
                xmlns:del="http://www.apriso.com/DELMIAAPriso"
                xmlns:flex="http://schemas.datacontract.org/2004/07/FlexNet.WebServices">
    <soap:Header xmlns:wsa="http://www.w3.org/2005/08/addressing">
        <wsa:Action>http://www.apriso.com/DELMIAApriso/unitTestSOAP/Invoke</wsa:Action>
        <wsa:To>http://tcsvl1d125/Apriso/WebServices/Public/unitTestSOAP.svc</wsa:To>
    </soap:Header>
    <soap:Body>
        <del:Invoke>
            <del:inputs>
                    <flex:EncodedParameters>"{'EmployeeNo':'jonas'}"</flex:EncodedParameters>
                    <flex:OperationName>TEST_PY</flex:OperationName>
            </del:inputs>
        </del:Invoke>
    </soap:Body>
</soap:Envelope>
```
