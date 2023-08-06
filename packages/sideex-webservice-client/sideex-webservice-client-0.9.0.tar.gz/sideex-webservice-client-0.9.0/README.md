# SideeX WebService API for Python
SideeX WebService Client API primarily handles the transfer of test suites to a hosted [SideeX WebService](https://hackmd.io/@sideex/webservice) server and returns the test reports.

> Prerequisite:
> - pip install asyncio
> - pip install aiohttp

# Download
Download the [SideeX WebService Client API for Python](https://pypi.org/project/sideex-webservice-client/)

# The API for Python
### `SideeXWebserviceClientAPI(baseURL)`
- Description: The constructor to create a Client API object
-  `baseURL`: Base URL of the SideeX WebService server

### `runTestSuite(file)`
- Description: Uses the API to run test cases
- `file`: The file that contains test cases
- Return:
    ```
    {
        "token": "xxxx"
    }
    ```

### `getState(token)`
- Description: Gets the current test case execution state
- `token`: The token returned from the *sideex-webservice* Web API
    - If the token is invalid, the response will be
        ```
        { 
            "ok": false, 
            "errorMessage": "invalid_token" 
        }
        ```
    - If the token is `valid` and the state is `running`, the response will be
        ```
        {
            "ok": true, 
            "webserviceState": {
                "state": "running"
            }
        }
        ```
    - If the token is `valid` and the state is `complete`, the response will be
        ```
        {
            "ok": true,
            "webserviceState": {
                "state": "complete"
            },
            "reports": {
                "url": "http://{publicURL_in_serviceconfig}/sideex-webservice-reports?token=xxxx",
                "passed": true,
                "summarry": [
                    {
                        "Suites": ["Test_Suite_1"],
                        "SideeXVersion": [3,3,7],
                        "Browser": "chrome 81.0.4044.138",
                        "Platform": "windows",
                        "Language": "(default)",
                        "StartTime": 1589867469846,
                        "EndTime": 1589867472874,
                        "PassedSuite": 1,
                        "TotalSuite": 1,
                        "PassedCase": 1,
                        "TotalPassedCase": 1
                    }
                ]
            },
            "logs": {
                "url": "http://{publicURL_in_serviceconfig}/sideex-webservice-logs?token=xxxx"
            }
        }
        ```
### `download(fromData, filePath, option)`
- Description: Download HTML test reports or logs
- `fromData`: A JSON object containing
    - `token`: The token returned from the *sideex-webservice* Web API
    - `file`: This parameter is optional. If set `file` to `"reports.zip"`, the API will return a zip file containing  all HTML reports, otherwise, it will return an HTML index webpage.
- `filePath`: Set your download file path. e.g.: "./reports"
- `option`: If option is set to `0`, the API will download reports. If set to `1`, it will download logs.

### `deleteReport(token)`
- Description: Delete the test case and the test reports on SideeX WebService server
- `token`: The token returned from the *sideex-webservice* Web API
    - If success, the response will be
        ```
        { 
            "ok": true, "state": "delete_complete" 
        }
        ```
    - If the token is invalid, the response will be 
        ```
        { 
            "ok": false, "errorMessage": "invalid_token" 
        }
        ```
    - If the test case is running, the response will be
        ```
        { 
            "ok": false, "errorMessage": "testcase_is_running" 
        }
        ```


# How to use

### Send a test case file to a SideeX WebService server 
```python=
import asyncio
import aiohttp
import json
#Include the lib of the SideeX WebService Client API
from SideeXWebserviceClientAPI import SideeXWebserviceClientAPI

#Create a Client API object connecting to a SideeX 
ws_client = SideeXWebserviceClientAPI('http://127.0.0.1:50000')

#Prepare a test case file
file = open('testcase.zip','rb')

#Send the test case file to the server and get a token 
print(asyncio.run(ws_client.runTestSuite(file)))
```

### Get the current test execution state from the server
```python=
#Get the current state
token = "xxxx"
print(asyncio.run(ws_client.getState(token)))
```
### Download the test reports and logs
```python=
#Download the test reports as an HTML index webpage
token = "xxxx"
froamData = aiohttp.FormData()
froamData.add_field('token', token, content_type='multipart/form-data')
asyncio.run(ws_client.download( froamData, "./index.html", 0))

#Download the logs as a zip file
token = "xxxx"
froamData = aiohttp.FormData()
froamData.add_field('token', token, content_type='multipart/form-data')
froamData.add_field('file', "reports.zip", content_type='multipart/form-data')
asyncio.run(ws_client.download( froamData, "./reports.zip", 0))

# if you want download the logs
token = "xxxx"
froamData = aiohttp.FormData()
froamData.add_field('token', token, content_type='multipart/form-data')
froamData.add_field('file', "reports.zip", content_type='multipart/form-data')
asyncio.run(ws_client.download( froamData, "./logs.zip", 1))
```

### Delete the test case and the reports from the server
```python=
#Delete the test case and reports
token = "xxxx"
print(asyncio.run(ws_client.deleteReport(token)))
```


A complete  example:
```python=
#Include the Client API lib
import asyncio
import aiohttp
import json
# from test2-sideex-webservice-client import SideeXWebServiceClientAPI
SideeXWebServiceClientAPI = __import__("sideex-webservice-client").SideeXWebServiceClientAPI
ProtocalType = __import__("sideex-webservice-client").ProtocalType

async def delay(time):
    await asyncio.sleep(time)

if __name__=="__main__":
    #Connect to a SideeX WebService server
    print(SideeXWebServiceClientAPI)
    ws_client = SideeXWebServiceClientAPI('http://127.0.0.1:50000', ProtocalType.HTTP)
    file = open('testcase.zip','rb')
    
    token = json.loads(asyncio.run(ws_client.runTestSuite(file)))['token']# get the token
    flag = False

    #Check the execution state every 2 seconds
    while not flag:

        #Get the current state
        state = json.loads(asyncio.run(ws_client.getState(token)))['webservice']['state']# get the WebService current state
        if (state != "complete" and state != "error"):
            print(state)
            asyncio.run(delay(2))
        #If test is error
        elif state == "error":
            flag = True
        #If test is complete
        else:
            print(state)
            froamData = aiohttp.FormData()
            froamData.add_field('token', token, content_type='application/x-www-form-urlencoded')
            froamData.add_field('file', "reports.zip", content_type='application/x-www-form-urlencoded')
            #download the test report to the target file path
            asyncio.run(ws_client.download( froamData, "./reports.zip", 0))

            #Download the logs
            froamData = aiohttp.FormData()
            froamData.add_field('token', token, content_type='application/x-www-form-urlencoded')
            asyncio.run(ws_client.download( froamData, "./logs.zip", 1))

            #Delete the test case and report from the server
            print(asyncio.run(ws_client.deleteReport(token)))

            flag = True
```

