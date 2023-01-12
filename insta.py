from instagrapi import Client
from tkinter import messagebox
import time
import re
import os
from pathlib import Path
import scraper
import openpyxl
from random import randint
import sqlite3
import tempfile
from threading import Thread

class Instagram:

   def __init__(self, user, output, grams, log_entry, text_total, window, canvas):
      
      self.user = user
      self.output = output
      self.grams = grams
      self.log_entry = log_entry
      self.gram = None
      self.intervalo = 10 # o melhor pra não levar block é 30 mas o default aqui é 10
      self.numbers = []
      self.total_de_seguidores = 0
      self.conut = 1
      self.lines_conut = 0
      self.new_count = 0
      self.analise_control = 0
      self.text_total = text_total
      self.window = window
      self.canvas = canvas
      self.block = False
      self.xlsxpath = None

      # banco de dados temporario para perfis analisados e para lista de seguidores
      self.conn = sqlite3.connect(tempfile.TemporaryFile(suffix=".db", delete=True).name, check_same_thread=False)
      self.cursor = self.conn.cursor()
   
   def writeLog(self,message):

         self.log_entry.configure(state="normal")
         self.log_entry.insert("end", f"{message}\n".upper())
         self.log_entry.see("end")
         self.log_entry.configure(state="disabled")
   
   def tiraremoji(self, text):

      try:
         regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F" 
            u"\U0001F300-\U0001F5FF" 
            u"\U0001F680-\U0001F6FF"  
            u"\U0001F1E0-\U0001F1FF" 
                                 "]+", flags = re.UNICODE)
         return regrex_pattern.sub(r'',text).encode("utf-8")
      except:

         return text

   def criarxlsx(self):

      self.writeLog("criando arquivo xlsx")
      # criar no diretorio que o usuario escolheu

      if os.path.exists(self.output):

         # criar o arquivo
   
         pathfile = Path(self.output).absolute()

         # criar o arquivo e pegar a primeira pagina
         self.book = openpyxl.Workbook()
         self.sheet = self.book["Sheet"]
         # renomear a pagina
         self.sheet.title = "dados"
         # a primeira linha de um documento xlsx é sempre o nome da coluna

         self.sheet.append(["usuario", "nome", "email" , "telefone"])
         #  configurar folha
         
         self.sheet.column_dimensions["A"].width = 22
         self.sheet.column_dimensions["B"].width = 22
         self.sheet.column_dimensions["C"].width = 22
         self.sheet.column_dimensions["D"].width = 22
         self.sheet.column_dimensions["E"].width = 22
         self.sheet.column_dimensions["F"].width = 22
         self.sheet.column_dimensions["G"].width = 22
         self.sheet.column_dimensions["H"].width = 22
         self.sheet.column_dimensions["I"].width = 22
         self.sheet["A1"].font = self.sheet["A1"].font.copy(bold=True)
         self.sheet["B1"].font = self.sheet["B1"].font.copy(bold=True)
         self.sheet["C1"].font = self.sheet["C1"].font.copy(bold=True)
         self.sheet["D1"].font = self.sheet["D1"].font.copy(bold=True)
         self.sheet["E1"].font = self.sheet["E1"].font.copy(bold=True)
         self.xlsxpath = pathfile
         return pathfile


      # usuario não escolheu um diretorio existente, criar xlsx na mesma pasta do programa

      else:

         pathfile = Path(os.getcwd()).absolute()
         # criar o arquivo e pegar a primeira pagina
         self.book = openpyxl.Workbook()
         self.sheet = self.book["Sheet"]
         # renomear a pagina
         self.sheet.title = "dados"
         # a primeira linha de um documento xlsx é sempre o nome da coluna
         self.sheet.append(["usuario", "nome", "email" , "telefone"])

         # configurar folha
         
         self.sheet.column_dimensions["A"].width = 22
         self.sheet.column_dimensions["B"].width = 22
         self.sheet.column_dimensions["C"].width = 22
         self.sheet.column_dimensions["D"].width = 22
         self.sheet.column_dimensions["E"].width = 22
         self.sheet.column_dimensions["F"].width = 22
         self.sheet.column_dimensions["G"].width = 22
         self.sheet.column_dimensions["H"].width = 22
         self.sheet.column_dimensions["I"].width = 22
         self.sheet["A1"].font = self.sheet["A1"].font.copy(bold=True)
         self.sheet["B1"].font = self.sheet["B1"].font.copy(bold=True)
         self.sheet["C1"].font = self.sheet["C1"].font.copy(bold=True)
         self.sheet["D1"].font = self.sheet["D1"].font.copy(bold=True)
         self.sheet["E1"].font = self.sheet["E1"].font.copy(bold=True)
         
         self.xlsxpath = pathfile
         return pathfile

   def add_gram(self):
      """adiconar novas contas durante execução"""

      ex_result = None

      try:

         usuario = input("\n[+] digite seu usuario: ")
         senha = input("\n[+] digite sua senha: ")
         gram = Client()
         gram.login(usuario, senha)
         self.grams.append({"gram":gram, "username": gram.account_info().username})
         self.writeLog("novo perfil adcionado")
         ex_result = True

      except Exception as e:

         messagebox.showerror("erro ao adicionar nova conta", f"mesage: {e}")
         print("\n[!] erro ao adicionar conta, o programa será encerrado.")
         ex_result = False

      return ex_result

   

   def gerenciarcontas(self, method=None,  user_id=None, amount=None, xlsxpath=None):
      """ esta função tem o unico objetivo de fazer todas a solicitações ao instagram e tratar erros
      de sessão expiada (login_requiered) e contas bloqueadas (challange_requiered) """

      while True: # loop com a quantidade de contas, se o loop acabar e não tiver nenhum resultado significa que todas as contas tomou block

         index = randint(0, len(self.grams) -1)

         try:

            # o programa precisa da lista de seguidores
            if method == "followers": result = self.grams[index]["gram"].user_followers(user_id=user_id, amount=amount)
            # o programa precisa dos dados de um perfil
            else: result = self.grams[index]["gram"].user_info(user_id=user_id)
            break

         except Exception as e : # tratar o erro

            # alertar o usuario que aconteceu alguma coisa com a conta
            self.writeLog(f"""o perfil {self.grams[index]["username"]} foi bloqueado""")
            # verificar se só tem uma conta rodando
            if len(self.grams) == 1:

               self.block = True
               usuario_adicionou_nova_conta = self.add_gram()

               if usuario_adicionou_nova_conta:

                  self.grams.pop(index)
                  self.block = False
                  result = None
               
               else:

                  self.writeLog("você só tinha essa conta rodando, parando o programa.")
                  self.book.save(rf"{xlsxpath}/{self.user}.xlsx")
                  result = None
                  quit()
            
            # o usuario adicionou mais de um perfil

            elif len(self.grams) > 1 : 

               self.writeLog("removendo perfil da lista")
               self.grams.pop(index)
               result = None

            else: # então todas as contas foram bloqueadas

               usuario_adicionou_nova_conta = self.add_gram()

               if usuario_adicionou_nova_conta:

                  result = None
               
               else:
   
                  self.writeLog("todas suas contas foram bloqueadas, parando programa.")
                  self.book.save(rf"{xlsxpath}/{self.user}.xlsx")
                  result = None
                  quit()
         
      # tudo correu bem, retorna os resultados para o programa continuar a execução

      if result != None: return result
         
   def analisarbio(self, user_now):
      
      self.writeLog("bucando numero na bio")

      try:

         rglist = []
         number = []
         if user_now.external_url == None or user_now.external_url == "": external_url = ""
         else: external_url = user_now.external_url
         rglist.append(re.search("\d{5}\-\d{4}", user_now.biography)) # xxxxx-xxxx
         rglist.append(re.search("\d{5}\d{4}", user_now.biography)) # xxxxxxxxx
         rglist.append(re.search("[0-9]{13}", user_now.biography)) # xx xx xxxxxxxxx
         rglist.append(re.search("\(?\d{2,}\)?[ -]?\d{4,}[\-\s]?\d{4}", user_now.biography)) # (xx) xxxx - xxxx
         rglist.append(re.search("[0-9]{13}", external_url)) # whatssap API (api.whatsapp.com e wa.me)
         
         # numero via links externos

         if "bit.ly" in external_url.lower():

            self.writeLog("analisando bit.ly link")
            try: 

               num = scraper.bitly(external_url)
               if num != False and num != None:

                  if len(num) >= 9: 
                     self.writeLog("numero encontrado!")
                     num = num.replace(")", "").replace("(", "").replace("-","").replace("+", "")
               
               else: self.writeLog("nenhum numero encontrado no link")
            except Exception as e: print(e) ; self.writeLog("nenhum numero encontrado no link")

         
         elif "linktr.ee" in external_url.lower():

            self.writeLog("analisando linktr.ee link")
            try:

               num = scraper.linktr_ee(external_url)
               if num != False and num != None:

                   if len(num) >= 9: 
                     self.writeLog("numero encontrado!")
                     num = num.replace(")", "").replace("(", "").replace("-","").replace("+", "")
                     number.append(num) 
               
            
               else:  self.writeLog("nenhum numero encontrado no link")
            except Exception as e: print(e) ;self.writeLog("nenhum numero encontrado no link")
         
         elif "contate.me" in external_url.lower():

            self.writeLog("analisando contate.me link")
            try:

               num = scraper.contate_me(external_url)
               if num != False and num != None:

                  if len(num) >= 9: 
                     self.writeLog("numero encontrado!")
                     num = num.replace(")", "").replace("(", "").replace("-","").replace("+", "")
                     number.append(num) 
                  
               else: self.writeLog("nenhum numero encontrado no link")
            
            except Exception as e: print(e) ; self.writeLog("nenhum numero encontrado no link")


         elif "linkr.bio" in external_url.lower():

            self.writeLog("um linkr.bio foi encontrado")

         # numeros pela bio ou link externo direto pra wa.me ou whatssap API

         for i in rglist:

            if i != None:

               if len(i.group(0)) >= 9:
                  self.writeLog("numero encontrado!")
                  number.append(i.group(0).replace(")", "").replace("(", "").replace("-","").replace("+", ""))
            
         if number == []:

            return [""]
         
         else:

            return number

      except Exception as e:
         
         print(e)
         return [""]
   
   def analisar(self,user_now, xlsxpath):

      self.writeLog(f"buscando contato de {user_now[0][1]}")
      user_now = self.gerenciarcontas(method="info", user_id=user_now[0][0], xlsxpath=xlsxpath)
      number = []
      number.append(user_now.contact_phone_number)
      email = user_now.public_email

      if number[0] == None or number[0] == "":

         number = self.analisarbio(user_now)
      
      else:

         self.writeLog("numero foi encontrado!")

      # salvar no arquivo xlsx

      self.writeLog("salvando consulta no arquivo xlsx")
      result_for_file =    [ 
         self.tiraremoji(user_now.username),
         self.tiraremoji(user_now.full_name),
         email] + number

      self.sheet.append(result_for_file)
      self.conut += 1
      self.canvas.itemconfig(self.text_total, text=f"{self.conut} analisados de {self.userdata.follower_count} seguidores:")
   
   def obterseguidores(self):

      try:

         self.writeLog(f"buscando informações de : {self.user}")
         self.userdata = self.grams[0]["gram"].user_info_by_username(self.user)
         self.total_de_seguidores = self.userdata.follower_count
         self.cursor.execute(""" CREATE TABLE IF NOT EXISTS analisados(userid TEXT)""")
         self.cursor.execute(""" CREATE TABLE IF NOT EXISTS analisar(userid TEXT, username TEXT)""")
         self.conn.commit()
         xlsxpath = self.criarxlsx()
         self.writeLog("pegando id de 1000 seguidores...")
         self.followers =  self.gerenciarcontas(method="followers" , user_id=self.userdata.pk, amount=1000, xlsxpath=xlsxpath)
         # primeira coleta de usersIDS
         self.writeLog("copiando lista de ID'S")


         for user_id in self.followers.keys():

            user = self.followers[user_id]
            self.cursor.execute(""" INSERT INTO analisar (userid, username) VALUES(?,?)""", (str(user.pk), str(user.username),))
            self.conn.commit()
         self.writeLog("buscando por numeros")
         
         while self.conut != self.total_de_seguidores:

            analisando = True

            while analisando:

               for user_id in self.cursor.execute("""SELECT userid FROM analisar """).fetchall():
                  
                  user_id = user_id[0]
                  if self.cursor.execute(""" SELECT * FROM analisados WHERE userid = (?)""",(str(user_id),)).fetchall()  != []:

                        pass
                  
                  else:
                        
                     user_now = self.cursor.execute("""SELECT * FROM analisar WHERE userid = (?) """, (str(user_id),)).fetchall()
                     analisando = False
                     break
               
               
               else:
                  self.writeLog("nenhum perfil pra analisar, se você saiu de sua conta no instagram\nfaça login novamente e reinicie o programa.\n"); self.book.save(rf"{xlsxpath}/{self.user}.xlsx");quit()

            try:

               self.analise_control += 1
               if self.analise_control == 2:

                  time.sleep(self.intervalo)
                  self.analise_control = 0
               
               elif self.block == False:

                  self.cursor.execute(""" INSERT INTO analisados (userid) VALUES (?)""", (user_now[0][0],) )
                  self.conn.commit()
                  Thread(target=self.analisar , args=(user_now,xlsxpath,), daemon=True).start()
                  self.new_count += 1

               # segunda coleta de id
               if self.new_count == 1000:

                  self.writeLog(f"pegando id de mais 1000 seguidores...")
                  total = len(self.cursor.execute(""" SELECT userid FROM analisar""").fetchall())
                  self.followers =  self.gerenciarcontas(method="followers" , user_id=self.userdata.pk, amount=total + 1000 , xlsxpath=xlsxpath)
                  self.writeLog("copiando lista de ID'S")

                  for user_id in self.followers.keys():

                     user = self.followers[user_id]
                     self.cursor.execute(""" INSERT INTO analisar (userid, username) VALUES(?,?)""", (str(user.pk), str(user.username),))
                     self.conn.commit()
                  self.new_count = 0

            except Exception as e:

               print(e)
               self.book.save(rf"{xlsxpath}/{self.user}.xlsx")
               self.writeLog("erro desconhecido ao pegar numero")
               messagebox.showerror(title="erro ao extrair seguidores", message=f"message: {e}")
               break;

         self.writeLog("coleta concluida")
         self.book.save(rf"{xlsxpath}/{self.user}.xlsx")       
         self.writeLog("o arquivo xlsx foi criado em:")
         self.writeLog(xlsxpath)
         quit()

      except Exception as e:

         self.book.save(rf"{xlsxpath}/{self.user}.xlsx")
         print(e)
         self.writeLog("erro ao extrair seguidores")
         messagebox.showerror(title="erro ao extrair seguidores", message=f"message: {e}")
         quit()
