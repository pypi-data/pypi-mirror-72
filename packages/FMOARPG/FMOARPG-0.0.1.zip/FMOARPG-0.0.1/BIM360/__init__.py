import requests
import BIM360
import CLASSES
import DATAMANAGEMENT
import Utils
from datetime import date


def getToken(client_id, client_secret, credentials):
    """Obtain Forge token given a client id & secret"""
    req = { 'client_id' : client_id, 'client_secret': client_secret, 'grant_type' : 'client_credentials','scope': credentials}
    resp = requests.post('https://developer.api.autodesk.com/authentication/v1/authenticate', req).json()
    #return resp['token_type'] + " " + resp['access_token']
    #return resp['access_token']
    token = CLASSES.Token(resp['access_token'], resp['token_type'], resp['expires_in'], date.today())
    return token


def getAccountUsers(token, hubId):
    url = "https://developer.api.autodesk.com/hq/v1/accounts/{0}/users".format(hubId)

    payload = ""
    headers = {
    'authorization': "Bearer {0}".format(token)
    }

    response = requests.request("GET", url, data=payload, headers=headers)
    
    usuarios = []
    
    for user in response.json():
        usuario = CLASSES.User(user['id'], user['email'], user['name'], "NA", "NA")
        usuarios.append(usuario)
    
    return usuarios

def getProjectUsers(token, pjtId, offset):
    url = "https://developer.api.autodesk.com/bim360/admin/v1/projects/{0}/users".format(pjtId)

    querystring = {"limit":"200", "offset":str(offset)}


    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    usuarios = []
    
    for user in response.json()['results']:
        usuario = CLASSES.User(user['id'], user['email'],user['name'], user['jobTitle'], user['roleIds'])
        usuarios.append(usuario)
        
    return [[response.json()['pagination']['limit'], response.json()['pagination']['offset'], response.json()['pagination']['totalResults']], usuarios]

def getBIM360Projects(token, hubId, offset):
    url = "https://developer.api.autodesk.com/hq/v1/accounts/{0}/projects".format(hubId)

    querystring = {"limit":"100","sort":"name", "offset":str(offset)}

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    projetos = []
    
    for project in response.json():
        projeto = CLASSES.Projeto(project['name'], project['id'], hubId, "")
        projeto.city = project['city']
        projeto.construction_type = project['construction_type']
        projeto.country = project['country']
        projeto.end_date = project['end_date']
        projeto.start_date = project['start_date']
        projeto.state_or_province = project['state_or_province']
        projeto.project_type = project['project_type']
        projeto.status = project['status']
        projetos.append(projeto)
    
    return projetos

def getCustomAttribute(token, urnas, pjtId):
    url = "https://developer.api.autodesk.com/bim360/docs/v1/projects/{0}/versions:batch-get".format(pjtId)

    #payload = "{\"urns\": [\"urn:adsk.wipprod:dm.lineage:XLhFbCdgQvKG6x9W6oA5fg\",\"urn:adsk.wipprod:dm.lineage:OhEGeSv8SFOkvK-bFQZEQQ\"]}"
    payload = "{\"urns\": "+Utils.ListToJsonString(urnas)+"}"
    headers = {
    'content-type': "application/json",
    'authorization': "Bearer "+token
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    
    atributos = []
    
    for attributes in response.json()['results']:
        for attribute in attributes['customAttributes']:
            atributo = CLASSES.CustomAttribute(attribute['name'], attribute['value'])
            atributos.append(atributo)
    
    return atributos

def getReviewActivity(token, pjtId):
    url = "https://developer.api.autodesk.com/bim360/admin/v1/projects/{0}/activities".format(pjtId)

    querystring = {"limit":"100"}

    headers = {
    'accept-language': "pt-BR",
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    atividades = []
    
    for atividade in response.json()["streamItems"]:
        if atividade['activity']['verb']=="initiate-review-process" or atividade['activity']['verb']=="claim-review-task" or atividade['activity']['verb']=="submit-review":
            novaAtividade = CLASSES.Atividade(atividade['activity']['published'], atividade['activity']['generator'], atividade['activity']['actor']['displayName'], atividade['activity']['verb'], atividade['activity']['object']['displayName'], atividade['activity']['object']['id'], atividade['activity']['object']['project']['id'], atividade['activity']['object']['project']['displayName'])
            atividades.append(novaAtividade)
            print("nova atividade "+novaAtividade.objeto_displayName)
    
    
    return [response.json()['nextToken'], atividades]

def getReviewActivityToken(token, pjtId, pageToken):
    url = "https://developer.api.autodesk.com/bim360/admin/v1/projects/{0}/activities".format(pjtId)

    querystring = {"limit":"100","token":pageToken}

    headers = {
    'accept-language': "pt-BR",
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    atividades = []
    
    for atividade in response.json()["streamItems"]:
        if atividade['activity']['verb']=="initiate-review-process" or atividade['activity']['verb']=="claim-review-task" or atividade['activity']['verb']=="submit-review":
            novaAtividade = CLASSES.Atividade(atividade['activity']['published'], atividade['activity']['generator'], atividade['activity']['actor']['displayName'], atividade['activity']['verb'], atividade['activity']['object']['displayName'], atividade['activity']['object']['id'], atividade['activity']['object']['project']['id'], atividade['activity']['object']['project']['displayName'])
            atividades.append(novaAtividade)
    
    nextToken = ""
    try:
        nextToken = response.json()['nextToken']
    except:
        pass
    
    return [nextToken, atividades]