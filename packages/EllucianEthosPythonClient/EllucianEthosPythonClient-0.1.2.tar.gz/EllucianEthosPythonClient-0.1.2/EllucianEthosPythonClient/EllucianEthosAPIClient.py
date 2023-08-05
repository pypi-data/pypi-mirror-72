from .APIClients import APIClientBase
from .EthosLoginSession import EthosLoginSessionBasedOnAPIKey
from .ResourceWrappers import getResourceWrapper
from .ResourceIterator import ResourceIterator
import json

class EllucianEthosAPIClient(APIClientBase):
  refreshAuthTokenIfRequired = None

  def __init__(self, baseURL, mock=None):
    super().__init__(baseURL=baseURL, mock=mock)

  def getLoginSessionFromAPIKey(self, apiKey):
    return EthosLoginSessionBasedOnAPIKey(APIClient=self, apikey=apiKey)

  #Doc list https://xedocs.ellucian.com/xe-banner-api/ethos_apis/foundation/persons/person_get_guid_v6.html
  def getResource(self, loginSession, resourceName, resourceID, version=None):
    def injectHeaderFN(headers):
      if version is not None:
        headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"

    result = self.sendGetRequest(
      url="/api/" + resourceName + "/" + resourceID,
      loginSession=loginSession,
      injectHeadersFn=injectHeaderFN
    )
    if result.status_code == 404:
      return None
    if result.status_code != 200:
      self.raiseResponseException(result)

    versionReturned = self.getVersionIntFromHeader(result.headers["x-hedtech-media-type"])

    return getResourceWrapper(clientAPIInstance=self, dict=json.loads(result.content), version=versionReturned, resourseName=resourceName)

  def getResourceIterator(self, loginSession, resourceName, version=None, pageSize=25):
    return ResourceIterator(self, loginSession, resourceName, version, pageSize)

  def getVersionIntFromHeader(self, meaidTypeHeaderValue):
    #example: application/vnd.hedtech.integration.v6+json
    requiredStart = "application/vnd.hedtech.integration.v"
    requiredEnd = "+json"
    if not meaidTypeHeaderValue.startswith(requiredStart):
      raise Exception("Could not determine resource version")
    meaidTypeHeaderValue = meaidTypeHeaderValue[len(requiredStart):]
    if not meaidTypeHeaderValue.endswith(requiredEnd):
      raise Exception("Could not determine resource version - header didn't end with " + requiredEnd)
    meaidTypeHeaderValue = meaidTypeHeaderValue[:-len(requiredEnd)]
    return meaidTypeHeaderValue

  def createResource(
    self,
    loginSession,
    resourceName,
    resourceDict,
    version=None
  ):
    if version is None:
      raise Exception("Must supply version when creating resource")
    def injectHeaderFN(headers):
        headers["Accept"] = "application/vnd.hedtech.integration.v" + version + "+json"
        headers["Content-Type"] = "application/vnd.hedtech.integration.v" + version + "+json"

    result = self.sendPostRequest(
      url="/api/" + resourceName,
      loginSession=loginSession,
      injectHeadersFn=injectHeaderFN,
      data=json.dumps(resourceDict)
    )
    if result.status_code != 201:
      self.raiseResponseException(result)

    versionReturned = self.getVersionIntFromHeader(result.headers["x-hedtech-media-type"])

    return getResourceWrapper(clientAPIInstance=self, dict=json.loads(result.content), version=versionReturned, resourseName=resourceName)

  def deleteResource(
    self,
    loginSession,
    resourceName,
    resourceID
  ):
    url = "/api/" + resourceName + "/" + resourceID

    result = self.sendDeleteRequest(
      url=url,
      loginSession=loginSession,
      injectHeadersFn=None
    )
    if result.status_code != 200:
      self.raiseResponseException(result)
