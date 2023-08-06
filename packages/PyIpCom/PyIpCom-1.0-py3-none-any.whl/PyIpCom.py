from github import Github
import random
import json
import urllib.parse

def create_server(username, password,repo=str("Repo_PyIPCom_"+str(int(str(random.random()).replace(".","")))),file="File_PyIPCom_"+str(int(str(random.random()).replace(".","")))+".json"):              
    g = Github(username, password)
    user = g.get_user()
    _repo = user.create_repo(repo)
    _repo = g.get_repo(username+"/"+repo)
    _repo.create_file(file, "Python_Internet_Protocol_Communication", "Python_Internet_Protocol_Communication")
    print("Server Has Been Created")
    print("User     *  "+username)
    print("Password *  "+password)
    print("Repo     *  "+repo)
    print("File     *  "+file),
    return username, password, repo, file
    
class server:
    
    def __init__(self, username, password, repo, file):                
        self.username = username
        self.password = password
        self.repo = repo
        self.file = file
        self.g = Github(username,password)
        user = self.g.get_repo(str(str(username)+"/"+str(repo)))
        contents = user.get_contents(file)
        res=json.loads(contents.decoded_content.decode('ascii'))
        self.check = res["check"]
        
    def send(self,data):
        user = self.g.get_repo(str(str(self.username)+"/"+str(self.repo)))
        check = ((random.random()*random.random())+(random.random()/(random.random()-random.random())))
        contents = user.get_contents(str(self.file))
        config = '{"data":"'+str(urllib.parse.quote(data, safe=''))+'" , "check":"'+str(check)+'"}'
        user.update_file(contents.path, __name__, config, contents.sha)      
        
    def recive(self):
        user = self.g.get_repo(str(str(self.username)+"/"+str(self.repo)))
        contents = user.get_contents(str(self.file))
        res=json.loads(contents.decoded_content.decode('ascii'))
        _check = res["check"]
        if(_check != self.check):
            data = urllib.parse.unquote(res["data"])
            self.check = _check
            return True,data
        return False,None