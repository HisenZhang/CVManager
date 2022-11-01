import os

class DeployerFactory:
    def __init__(self,profile):
        self.profile=profile
        pass

    def createDeployers(self,dest):
        deployers = dict()        
        if 'GoogleDrive' in dest:
            from deployer import GoogleDriveDeployer
            deployers['GoogleDrive'] = GoogleDriveDeployer(self.profile)                                
        return deployers

class BaseDeployer:
    def __init__(self,profile):
        self.profile=profile
        pass

    def deploy(self):
        pass


class GoogleDriveDeployer(BaseDeployer):
    def __init__(self,profile):
        super().__init__(profile)
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive

        self.gauth = GoogleAuth()
        cred_file = 'google_drive.cred'
        if os.path.exists(cred_file):
            self.gauth.LoadCredentialsFile(cred_file)
        else:
            self.gauth.LocalWebserverAuth()
            self.gauth.SaveCredentialsFile(cred_file)
        self.drive = GoogleDrive(self.gauth)

    def trashOldFiles(self,filenamePattern):
        query = 'title contains \'{}\' and trashed=false'.format(filenamePattern)
        obsoleteFiles = self.drive.ListFile({'q': query}).GetList()
        for file in obsoleteFiles:
            file.Trash()

    def deploy(self, profile, type_path):
       
        files = [type_path[t] for t in profile['deploy.GoogleDrive.type']]

        for filepath in files:
            filename = filepath.split('\\')[-1]
            f = self.drive.CreateFile({'title': filename,
                                       'parents': [{'id': profile['deploy.GoogleDrive.folder']}]})
            # Read file and set it as the content of this instance.
            f.SetContentFile(filepath)
            f.Upload()
        return super().deploy()
