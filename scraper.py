import requests
from bs4 import  BeautifulSoup
from fake_headers import Headers
import re

def contate_me(url:str): # contate.me, não precisa verficar se tem o link pra wap pois ele só possui link pro mesmo

    response = requests.get(url, headers=Headers().generate())
    
    if response.status_code == 200:

        doc = BeautifulSoup(response.text, "html.parser")
        number_link = doc.find_all("a", {"title" : "Compartilhe no WhatsApp"})[0].get("href")
        number = re.search("[0-9]{13}", number_link).group(0)
        return number

    else:
        
        return False
    
def linktr_ee(url:str): # linktr.ee

    response = requests.get(url, headers=Headers().generate())

    if response.status_code == 200:

        # verificar se tem link pro whatssap

        if "whatsapp.com" in response.text or "wa.me" in response.text:

            doc = BeautifulSoup(response.text , "html.parser")
            tagsA = doc.find_all("a")
            number = False

            for i in tagsA: 

                if "whatsapp.com" in i.get("href") or "wa.me" in i.get("href"):

                    number_link = i.get("href")
                    number = re.search("[0-9]{13}", number_link)
                    if  number != None: # o link não tem numero pois é de grupo
                        number.group(0)
                        break
            return number
    else:

        return False

def bitly(url:str): # bit.ly

    response = requests.get(url, headers=Headers().generate())

    if response.status_code == 200:

        # verificar se tem link do whatssap

        if  "whatsapp.com" in response.text or "wa.me" in response.text:

            doc = BeautifulSoup(response.text, "html.parser")
            number_link = doc.find_all("a", {"title" : "Compartilhe no WhatsApp"})[0].get("href")
            number = re.search("[0-9]{13}", number_link).group(0)
            return number
            
        else:

            return False

def linkr_bio(url:str): # linkr.bio

    # regex não funcionou nesse site, proxima atualização
    # tenta descobrir como pegar o id do link no documento que o site retorna pra poder lançar uma
    # request pra API https://api.linkr.bio/linkr/page/pub/share_link. NÃO ESQUECE ALOGICA PORQUE EU ACHO QUE É O UNICO JEITO DE PEGAR O NUMERO
    

    response = requests.get(url, headers=Headers().generate())

    if response.status_code == 200:

        rglist = []
        rglist.append(re.search("\d{5}\-\d{4}", response.text)) # xxxxx-xxxx
        rglist.append(re.search("\d{5}\d{4}", response.text)) # xxxxxxxxx
        rglist.append(re.search("[0-9]{13}", response.text)) # xx xx xxxxxxxxx
        rglist.append(re.search("\(?\d{2,}\)?[ -]?\d{4,}[\-\s]?\d{4}", response.text)) # (xx) xxxx - xxxx
        rglist.append(re.search("[0-9]{13}", response.text)) # whatssap API (api.whatsapp.com e wa.me)
         
        for i in rglist:

            if i != None:

                return i.group(0)