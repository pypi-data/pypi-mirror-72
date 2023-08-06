import requests
import CLASSES
import re


def GetHubs(token):
    url = "https://developer.api.autodesk.com/project/v1/hubs"

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    hubs = []
    for hub in response.json()['data']:
        newHub = CLASSES.MapHub(hub['attributes']['name'], hub['id'])
        hubs.append(newHub)
    
    return hubs


def GetProjects(token, hubId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/{0}/projects".format(hubId)

    headers = {
    'authorization': "Bearer " + token
    }

    response = requests.request("GET", url, headers=headers)
    projetos = []
    for pjt in response.json()['data']:
        newPjt = CLASSES.Projeto(pjt['attributes']['name'], pjt['id'], hubId, pjt['relationships']['issues']['data']['id'])
        projetos.append(newPjt)
    
    return projetos

def GetProjectTopFolders(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/{0}/projects/{1}/topFolders".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    topfolders = []
    
    for folder in response.json()['data']:
        if re.match("Project Files", folder['attributes']['name']) or re.match("Arquivos do projeto", folder['attributes']['name']):
            topfolder = CLASSES.Conteudo(folder['attributes']['name'], folder['id'], pjtId)
            topfolder.tipo = CLASSES.Tipo.PASTA
            topfolders.append(topfolder)
    
    return topfolders

def GetFolderContents(token, Folder):
    url = "https://developer.api.autodesk.com/data/v1/projects/{0}/folders/{1}/contents".format(Folder.pjtId, Folder.conteudoId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    for content in response.json()['data']:
        try:
            conteudo = CLASSES.Conteudo("Noname", content['id'], Folder.pjtId)
            if content['type'] == 'folders':
                conteudo.nome = content['attributes']['name']
                conteudo.tipo = Conteudo.Tipo.PASTA
            else:
                conteudo.nome = content['attributes']['displayName']
                conteudo.tipo = Conteudo.Tipo.ARQUIVO
            Folder.items.append(conteudo)
        except:
            pass
    
    return Folder.items

def GetIssuesContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['issues']['data']['id']

def GetSubmittalsContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['submittals']['data']['id']

def GetRfisContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['rfis']['data']['id']

def GetMarkupsContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['markups']['data']['id']

def GetChecklistsContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['checklists']['data']['id']

def GetCostContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['cost']['data']['id']

def GetLocationsContainer(token, hubId, pjtId):
    url = "https://developer.api.autodesk.com/project/v1/hubs/b.{0}/projects/b.{1}".format(hubId, pjtId)

    headers = {
    'authorization': "Bearer "+token
    }

    response = requests.request("GET", url, headers=headers)
    
    return response.json()['data']['relationships']['locations']['data']['id']