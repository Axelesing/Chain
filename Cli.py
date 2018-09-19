import cmd
import rsa
import os
import json
import blockchain
import AuthorizationKeyMethods
import DBAdapter
import Network



def getPrivateKeyFromFile(fname):
    try:
        fname = os.path.abspath(fname)                                                                                 
        f = open(fname, 'r')                                                                                           
        l = f.readlines()                                                                                              
        n = int(l[0][:-1])                                                                                              
        e = int(l[1][:-1])
        d = int(l[2][:-1])
        p = int(l[3][:-1])
        q = int(l[4][:-1])
        PrivateKey = rsa.PrivateKey(n, e, d, p, q)                                                                     
        return PrivateKey
    except Exception as e:
        print('Not valid key or wrong unknown file, try again')
        return False

class Cli(cmd.Cmd):

    Network = None
    DBAdapter = None
    AuthorizationKeyMethods = None
    isAuthorized = False

    def __init__(self):
        cmd.Cmd.__init__(self, '\f')
        self.DBA = DBAdapter.DBAdapter()
        self.AuthKeyMeth = AuthorizationKeyMethods.AuthorizationKeyMethods()
        self.Cblockchain = blockchain.Blockchain()
        self.CNetwork = Network.Network(blockchain)

        self.intro = 'Welcome to system. Please, Authorization.'
        self.prompt = 'Not auth==>'
        self.doc_header = 'Введите help для более подробной информации'

    def default(self, line):
        '''
        При вводе несуществующей команды, выдаёт ошибку
        :param line:
        :return:
        '''
        print('Неверная команда. Введите help для более подробной информации. \n')                                    
        
    def do_login(self, args):
        '''
        Команда для авторизации пользователя в сети
        :param args:
        :return:
        '''
        var = True
        while(var == True):
            pathPrivateKey = input('Please, enter way to private key:\n')                                               
            PrivateKey = self.getPrivateKeyFromFile(pathPrivateKey)                                                     
            if (PrivateKey):
                if (self.AuthKeyMeth.authorization(PrivateKey)):
                    self.intro = 'Welcome to system. Type help to list commands.\n'
                    self.prompt = '====>'
                    self.doc_header = 'Введите help для более подробной информации'
                    self.isAuthorized = True
                    PublicKey = str(self.AuthKeyMeth.PrivateKeyToPublic(PrivateKey))
                    name = self.DBA.GetUserByPublicKey(PublicKey)['FIO']
                    return print('Hello', name)
                else:
                    print('InvalidKey, try again')
            else:
                exit(0)

    def do_logout(self, args):
        '''
        Команда для выхода из сети
        :param args:
        :return:
        '''
        self.prompt = 'Not auth==>'
        self.doc_header = 'You out of network'
        self.isAuthorized = False

    def GeneratePrivateKey(self):
        '''
        Генерирование закрытого ключа
        :return:
        '''
        PrivateKey = self.AuthKeyMeth.generateKey()
        s = 0
        stat = True
        while stat:
            if not os.path.exists('keys\PrivateKey_' + str(s)):
                f = open('keys\PrivateKey_' + str(s), 'w')
                print()
            else:
                s = s + 1
            f.write(str(PrivateKey.n + '\n'))
            f.write(str(PrivateKey.e + '\n'))
            f.write(str(PrivateKey.d + '\n'))
            f.write(str(PrivateKey.p + '\n'))
            f.write(str(PrivateKey.q + '\n'))
            print(self, 'Attention, key was generated, save him')
            AbsolutePathToFile = os.path.abspath('keys\PrivateKey_' + str(s))
            return AbsolutePathToFile

    def do_CreateUser(self, argv):
        '''
        Команда для создания нового пользователя (только для ЦУУ)
        :param argv:
        :return:
        '''
        if (self.isAuthorized):                                                                                         
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                           
                Transact = {}
                datadict = {}
                Type = input('Enter type user: \n open\closed \n')                                                      
                if (Type == 'open') or (Type == 1) or (Type == 'Open'):                                                 
                    datadict['FIO'] = input('Please enter full name: \n ')                                              

                    print (' 1) Student \n 2) Aspirant \n 3) PPSinUSU \n 4) PPSnotInUSU \n 5) Auditors \n')
                    Num = ['Student', 'Aspirant', 'PPSinUSU', 'PPSnotInUSU', 'Auditors']                                
                    datadict['Role'] = input('Select role:\n')                                                          

                    Num2 = [1, 0]                                                                                       
                    C = input('You consists at IK? \n Y/N \n')
                    if (C == 'Y') or (C == 'y') or (C == 'да') or (C == 'Да') or (C == 'ДА'):                           
                        datadict['isIK'] = Num2[0]
                    else:
                        datadict['isIK'] = Num2[1]

                    Transact['data'] = datadict                                                                         
                    Transact['Type'] = 0                                                                                
                    path = self.GeneratePrivateKey()
                    PrivateKey = self.getPrivateKeyFromFile(path)
                    Transact['publicKey'] = self.AuthKeyMeth.PublicKeyToString(PrivateKey)
                    string = json.dumps(Transact, sort_keys=True)
                    signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                    Transact['signature'] = signature
                if (Type == 'closed') or (Type == 2):                                                                   
                    datadict['FIO'] = input('Please enter full name: \n ')                                              

                    print(' 1) Student \n 2) Aspirant \n 3) PPSUSU \n 4) PPSnotInUSU \n 5) Auditors \n 6) Admin')
                    Num = ['Student', 'Aspirant', 'PPSUSU', 'PPSnotUSU', 'Auditors', 'Admin']                          
                    datadict['Role'] = input('Select role:\n',)                                                         

                    Num2 = [1, 0]                                                                                      
                    C = print ('You consists at IK? \n Y/N \n')
                    if (C == 'Y') or (C == 'y') or (C == 'да') or (C == 'Да') or (C == 'ДА'):                         
                        datadict['isIK'] = Num2[0]
                    else:
                        datadict['isIK'] = Num2[1]
                    path = self.GeneratePrivateKey()
                    PrivateKey = self.getPrivateKeyFromFile(path)
                    Transact['data'] = datadict                                                                       
                    Transact['Type'] = 1                                                                               
                    Transact['publicKey'] = self.AuthKeyMeth.PublicKeyToString(PrivateKey)
                    string = json.dumps(Transact, sort_keys=True)
                    signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                    Transact['signature'] = signature
            else:
                print('Insufficiently rights access')                                                                
        else:
            print('Please, authorized')                                                                               

    def getPrivateKeyFromFile(self, fname):
        try:
            fname = os.path.abspath(fname)                                                                          
            f = open(fname, 'r')                                                                                      
            l = f.readlines()                                                                                          
            n = int(l[0][:-1])                                                                                        
            e = int(l[1][:-1])
            d = int(l[2][:-1])
            p = int(l[3][:-1])
            q = int(l[4][:-1])
            PrivateKey = rsa.PrivateKey(n, e, d, p, q)                                                                
            return PrivateKey
        except Exception as e:
            print('Invalid Key, try again')
            return False

    def do_CreateOpenVoting(self, args):
        '''
        Команда для создания открытого голосования (только для ИК)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                       
            if (self.AuthKeyMeth.account['IsIk'] == "1"):                                                             
                Transact = {}
                datadict = {}
                datadict['Vote'] = input('Please, enter question voting: \n')                                          
                Num3 = input('Please, enter time of voting: \n')                                                      
                if (Num3 == 1) or (Num3 == 2) or (Num3 == 3) or (Num3 == 4):                                            
                    datadict['time'] = Num3
                else:
                    print('Incorrect time \n')
                datadict['Role'] = input('Please, enter role, who can vote: \n')
                Transact['data'] = datadict                                                    
                Transact['Type'] = 2                                                                                 
                PrivateKey = self.AuthKeyMeth.account['PrivateKey']
                Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                                   
            else:
                print('Insufficiently rights access')
        else:
            print('Please, authorized')                                                                               

    def do_CreateCloseVoting(self, args):
        '''
        Команда для создания закрытого голосования (только для ИК)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                     
            if (self.AuthKeyMeth.account['IsIk'] == "1"):                                                          
                Transact = {}
                datadict = {}
                datadict['Content'] = input('Please, enter question voting: \n')                                  
                Num4 = input('Please, enter time of voting: \n')                                                
                if (Num4 == 1) or (Num4 == 2) or (Num4 == 3) or (Num4 == 4):                                           
                    datadict['time'] = Num4
                else:
                    print('Incorrect time \n')
                datadict['Role'] = input('Please, enter role, who can vote: \n')                                      
                Transact['data'] = datadict                                                                         
                Transact['Type'] = 3                                                                             
                PrivateKey = self.AuthKeyMeth.account['PrivateKey']
                Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                                  
            else:
                print('Insufficiently rights access')
        else:
            print('Please, authorized')                                                                               

    def do_UpRole(self, args):
        '''
        Команда для повышения роли (только для ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                              
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                    

                Transact = {}
                datadict = {}
                Transact['data'] = datadict                                                                          
                Transact['Type'] = 5                                                                               
                PrivateKey = self.AuthKeyMeth.account['PrivateKey']
                Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                                      

            else:
                print('Insufficiently rights access')                                                                 
        else:
            print('Please, authorized')                                                                                 

    def do_DownRole(self, args):
        '''
        Команда для понижения роли (только для ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                      
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                       
                Transact = {}
                datadict = {}
                Transact['data'] = datadict                                                                          
                Transact['Type'] = 6                                                                                    
                PrivateKey = self.AuthKeyMeth.account['PrivateKey']
                Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                               
            else:
                print('Insufficiently rights access')                                                           
        else:
            print('Please, authorized')                                                                                 

    def do_InquiryVoting(self, args):
        '''
        Подать запрос для голосования
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                    
            if (self.AuthKeyMeth.account['Role'] == "Student") \
                    or (self.AuthKeyMeth.account['Role'] == "Aspirant"):                                           
                Transact = {}
                datadict = {}
                datadict['voting'] = input('Choice type voting: \n open\closed')                                      
                datadict['vote'] = input('Please, specify inquiry:\n 1) Become member IK \n 2) Withdraw member IK')    
                if (datadict['vote'] == 1):                                                                            
                    datadict['FIO'] = input('Enter your name from inquiry: \n')                                      
                    Transact['data'] = datadict                                                                       
                    Transact['Type'] = 7                                                                            

                if (datadict['vote'] == 2):                                                                           
                    datadict['FIO'] = input('Enter FIO member, whom you want to withdraw: \n')                     
                    Transact['data'] = datadict                                                                       
                    Transact['Type'] = 8                                                                       
                PrivateKey = self.AuthorizationKeyMethods.account.get['PrivateKey']
                Transact['publicKey'] = self.AuthorizationKeyMethods.account.get['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = AuthorizationKeyMethods.AuthorizationKeyMethods.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                              

            if (self.AuthKeyMeth.account['Role'] == "PPSUSU") \
                    or (self.AuthKeyMeth.account['Role'] == "PPSnotUSU"):                                         
                Transact = {}
                datadict = {}
                datadict['voting'] = input('Choice type voting: \n open\closed')                                     
                datadict['vote'] = input('Please, specify inquiry:\n 1) Become member IK \n 2) Withdraw member IK')  
                if (datadict['vote'] == 1):                                                                            
                    datadict['FIO'] = input('Enter your name from inquiry: \n')                                       
                    Transact['data'] = datadict                                                                      
                    Transact['Type'] = 7                                                                               

                if (datadict['vote'] == 2):                                                                            
                    datadict['FIO'] = input('Enter FIO member, whom you want to withdraw: \n')                        
                    Transact['data'] = datadict                                                                      
                    Transact['Type'] = 8                                                                            
                PrivateKey = self.AuthKeyMeth.account['PrivateKey']
                Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                                 
        else:
            print('Please, authorized')                                                                                

    def do_vote(self, args):
        '''
        Команда для голосования
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                       
            Transact = {}
            datadict = {}

            datadict['voting'] = input('Please choice voting:\n')

            datadict['vote'] = input('Please vote:\n')

            Transact['data'] = datadict                                                                                
            Transact['Type'] = 4                                                                                     
            PrivateKey = self.AuthKeyMeth.account['PrivateKey']
            Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
            string = json.dumps(Transact, sort_keys=True)
            signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
            Transact['signature'] = signature                                                                       
        else:
            print('Please, authorized')                                                                                 

    def do_help(self, args):
        '''
        Команда для вызова помощи
        :param args:
        :return:
        '''
        print('login - Команда для авторизации пользователя в сети \nlogout - Команда для выхода из сети\n'           
              'CreateUser - Команда для создания нового пользователя (только ЦУУ)\n'
              'CreateOpenVoting - Команда для создания открытого голосования (только ИК)\n'
              'CreateCloseVoting - Команда для создания закрытого голосования (только ИК)\n'
              'UpRole - Команда для повышения роли (только ЦУУ) \nDownRole - Команда для понижения роли (только ЦУУ)\n'
              'vote - Команда для голосования\n'
              'ChangeInIKUser - Команда для изменения положения пользователя в избирательной комиссии\n'
              'DeleteUser - Команда для удаления пользователя (только ЦУУ)\n'
              'InquiryResultsVoting - Команда для запроса результатов по всем прошедшим голосованиям\n'
              'InquiryAvailableVoting - Команда для запроса доступных голосований\n'
              'CountVote - Команда для подсчета голосов (только ИК и аудиторы)\n'
              'InquiryVoting - Команда для подачи запроса на голосования\n'
              'InspectionVotes - Команда для проверки голосов (только ИК и аудиторы)\n'
              'EditingProfile - Команда для редактирования профиля\n'
              'TaxInquiryRecoveryKeys - Команда подачи запроса для восстановления ключей доступа к системе\n'
              'RecoveryKeys - Команда для восстановления ключей для доступа к системе (только ЦУУ)\n'
              'FindUser - Команда для поиска пользователя в цепочке блоков(для проверки анонимности)(только аудиторы)\n'
              'AppointAuditor - Команда для назначения случайного аудитора (только ЦУУ)\n'
              'AppointUserIK - Команда для назначения случайного члена избирательной комиссии (только ЦУУ)\n'
              'exit - Команда для выхода из системы')

    def do_ChangeInIKUser(self, args):
        '''
        Команда для изменения положения пользователя
        в избирательной комиссии (только для ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                        
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                         
                Transact = {}
                datadict = {}
                Transact['data'] = datadict                                                                         
                Transact['Type'] = 7                                                                                    
                PrivateKey = self.AuthKeyMeth.account['PrivateKey']
                Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
                string = json.dumps(Transact, sort_keys=True)
                signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
                Transact['signature'] = signature                                                                      
            else:
                print('Insufficiently rights access')                                                                 
        else:
            print('Please, authorized')                                                                              

    def do_DeleteUser(self, args):
        '''
        Команда для удаления пользователя (только ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                     
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                      
                PublicKey = self.AuthKeyMeth.PublicKeyToString()                                                  
                info = self.DBA.DeleteUser(PublicKey)                                                                 
                exec(info)                                                                                              
            else:
                print('Insufficiently rights access')                                                              
        else:
            print('Please, authorized')                                                                                 

    def do_InquiryResultsVoting(self, args):
        '''
        Команда для запроса результатов по всем прошедшим голосованиям
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                   
            result = self.DBA.GetPublicVotesList()                                                                 
            print(result)                                                                                        
        else:
            print('Please, authorized')                                                                               


    def do_InquiryAvailableVoting(self, args):
        '''
        Команда для запроса доступных голосований
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                      
            print()

        else:
            print('Please, authorized')                                                                                 

    def do_CountVote(self, args):
        '''
        Команда для подсчета голосов (только ИК и аудиторы)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                       
            if (self.AuthKeyMeth.account['Role'] == "Auditor") or \
                    (self.AuthKeyMeth.account['ikIK'] == "1"):                                                        
                d = input('Choice what vote: \n open\closed')                                                      
                if (d == 'open') or (d == 'Open'):                                                                   
                    a = self.DBA.GetPublicVotesList()                                                                   
                    print(a)                                                                                            
                if (d == 'closed') or (d == 'Closed'):                                                              
                    a = self.DBA.GetPrivateVotesList()                                                                
                    print(a)                                                                                          
            else:
                print('Insufficiently rights access')                                                                 
        else:
            print('Please, authorized')                                                                               

    def do_InspectionVotes(self, args):
        '''
        Проверка голосов (ИК и аудиторs)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                     
            if (self.AuthKeyMeth.account['Role'] == "Auditor"):                                                         
                print()

            else:
                print('Insufficiently rights access')                                                              
        else:
            print('Please, authorized')                                                                                

    def do_EditingProfile(self, args):
        '''
        Команда для редактирования профиля
        :param args:
        :return:
        '''
        Transact = {}
        datadict = {}
        datadict['FIO'] = input('Please enter new name \n')                                                             
        Transact['data'] = datadict                                                                                  
        Transact['Type'] = 9                                                                                        
        PrivateKey = self.AuthKeyMeth.account.get['PrivateKey']
        Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
        string = json.dumps(Transact, sort_keys=True)
        signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
        Transact['signature'] = signature                                                                         

    def do_TaxInquiryRecoveryKeys(self, args):
        '''
        Команда подачи запроса для восстановления ключей доступа к системе
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                       
            Transact = {}
            datadict = {}
            datadict['FIO'] = input('Please, enter your name: \n')                                       
            Transact['data'] = datadict                                                                               
            PrivateKey = self.AuthKeyMeth.account.get['PrivateKey']
            Transact['publicKey'] = self.AuthKeyMeth.account['PublicKey']
            string = json.dumps(Transact, sort_keys=True)
            signature = self.AuthKeyMeth.CreateSignature(string, PrivateKey)
            Transact['signature'] = signature                                                                       

    def do_RecoveryKeys(self, args):
        '''
        Команда для восстановления ключей для доступа к системе (только для ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                 
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                       
                print()

            else:
                print('Insufficiently rights access')                                                                   
        else:
            print('Please, authorized')                                                                                 


    def do_FindUser(self, args):
        '''
        Команда для поиска пользователя в цепочке блоков (для проверки анонимности) только аудиторы
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                      
            if (self.AuthKeyMeth.account['Role'] == "Auditor"):                                                       
                print()
                search = input('Enter IDUser:\n')
                info = self.DBA.GetPrivateVoteByID(search)                                                             
                print(info)
            else:
                print('Insufficiently rights access')                                                                
        else:
            print('Please, authorized')                                                                                 

    def do_AppointAuditor(self, args):
        '''
        Команда для назначения случайного аудитора (только ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                       
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                                                    
                print()

            else:
                print('Insufficiently rights access')                                                                  
        else:
            print('Please, authorized')                                                                                

    def do_AppointUserIK(self, args):
        '''
        Команда для назначения случайного члена избирательной комиссии (только ЦУУ)
        :param args:
        :return:
        '''
        if (self.isAuthorized):                                                                                    
            if (self.AuthKeyMeth.account['Role'] == "Admin"):                              
                print()

            else:
                print('Insufficiently rights access')                                                                 
        else:
            print('Please, authorized')                                                                                 

    def do_exit(self, line):
        '''
        Команда выхода из системы
        :return:
        '''
        exit(0)

if __name__ == '__main__':
    cli = Cli()
    try:
       cli.cmdloop()
    except KeyboardInterrupt:
        print('Fatal Error')                                                                                          
