import json
import asyncio
import aiohttp
import os
import ssl
from enum import Enum

class ProtocalType(Enum):
    HTTP = 0
    HTTPS_DISABLE = 1
    HTTPS_ENABLE = 2

class SideeXWebServiceClientAPI():
    def __init__(self, baseURL, protocalType=ProtocalType.HTTP, caFilePath=None):
        self.baseURL = baseURL
        self.protocalType = protocalType
        self.caFilePath = caFilePath
        self.sslContext = None

        if self.baseURL[-1] != '/':
            self.baseURL = self.baseURL + "/"

        if self.protocalType == ProtocalType.HTTPS_DISABLE:
            self.sslContext = False
        elif self.protocalType == ProtocalType.HTTPS_ENABLE:
            self.sslContext = ssl.create_default_context(cafile=self.caFilePath)

    async def runTestSuite(self, file):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            data = aiohttp.FormData()
            data.add_field('file', file, filename=os.path.basename(file.name), content_type='application/x-www-form-urlencoded')
            async with session.post(self.baseURL+"sideex-webservice", data = data) as resp:
                return await resp.text()
    
    async def getState(self, token):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            data = aiohttp.FormData()
            data.add_field('token', token, content_type='application/x-www-form-urlencoded')

            async with session.get(self.baseURL+"sideex-webservice-state", data = data) as resp:
                return await resp.text()

    async def download(self, formData, filePath, option):
        tempURL = self.baseURL
        if option == 0:
            tempURL = tempURL + "sideex-webservice-reports"
        else:
            tempURL = tempURL + "sideex-webservice-logs"

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            async with session.get(tempURL, data = formData) as resp:
                test = await resp.read()
                with open(filePath, "wb") as f:
                    f.write(test)
    
    async def deleteReport(self, token):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.sslContext)) as session:
            data = aiohttp.FormData()
            data.add_field('token', token, content_type='application/x-www-form-urlencoded')

            async with session.post(self.baseURL+"sideex-webservice-delete", data = data) as resp:
                return await resp.text()