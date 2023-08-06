from luna.lunaUtils import LunaUtils
import os

class LocalLunaUtils(LunaUtils):
    def RegisterModel(self, model_path, description, luna_python_model=None):
        # do nothing
        return
    
    def GetModelPath(self, context):
        return os.getcwd()

    
    def DeployModel(self):
        return
        
    def DownloadModel(self, model_path="models"):
        return os.path.join(os.getcwd(), model_path)