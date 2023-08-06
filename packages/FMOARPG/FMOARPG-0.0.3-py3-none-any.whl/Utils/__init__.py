import DATAMANAGEMENT
import CLASSES

def DividirEmSubListas(lista, maximo):
    retorno = []
    imediato = []
    for elemento in lista:
        if len(imediato) < maximo:
            imediato.append(elemento)
        else:
            apend = imediato
            retorno.append(apend)
            imediato = [elemento]
    if len(imediato)>0:
        retorno.append(imediato)
    return retorno

def ListToJsonString(lista):
    return str("[\""+"\",\"".join(lista)+"\"]")

#Aqui deve ser passado o objeto Pasta
def Subpastas(Token, Pasta):
    items = DATAMANAGEMENT.GetFolderContents(Token, Pasta)
    for item in items:
        if item.tipo == CLASSES.Tipo.PASTA:  
            Subpastas(Token, item)
        else:
            pass
