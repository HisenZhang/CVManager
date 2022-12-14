import os


class DeployerFactory:
    def __init__(self, profile):
        self.profile = profile
        pass

    def createDeployers(self, dest):
        if dest is None:
            return None
        deployers = dict()
        if 'GoogleDrive' in dest:
            from deployer import GoogleDriveDeployer
            deployers['GoogleDrive'] = GoogleDriveDeployer(self.profile)
        return deployers


class BaseDeployer:
    def __init__(self, profile):
        self.profile = profile
        pass

    def deploy(self):
        pass


class GoogleDriveDeployer(BaseDeployer):
    def __init__(self, profile):
        super().__init__(profile)
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive

        self.gauth = GoogleAuth()
        cred_file = 'google_drive_secrets.json'
        if os.path.exists(cred_file):
            self.gauth.LoadCredentialsFile(cred_file)
        else:
            self.gauth.LocalWebserverAuth()
            self.gauth.SaveCredentialsFile(cred_file)
        self.drive = GoogleDrive(self.gauth)

    def trashOldFiles(self, folder, filenamePattern):
        query = '\'{}\' in parents and title contains \'{}\' and trashed=false'.format(
            folder, filenamePattern)
        obsoleteFiles = self.drive.ListFile({'q': query}).GetList()
        for file in obsoleteFiles:
            file.Trash()

    def deploy(self, profile, type_path):

        files = [type_path[t] for t in profile['deploy.GoogleDrive.type']]
        if self.profile['input.privatekey']:
            files += [type_path[t] +
                      '.sig' for t in profile['deploy.GoogleDrive.type']]
        for filepath in files:
            filename = os.path.basename(filepath)
            f = self.drive.CreateFile({'title': filename,
                                       'parents': [{'id': profile['deploy.GoogleDrive.folder']}]})
            # Read file and set it as the content of this instance.
            f.SetContentFile(filepath)
            f.Upload()
        return super().deploy()
