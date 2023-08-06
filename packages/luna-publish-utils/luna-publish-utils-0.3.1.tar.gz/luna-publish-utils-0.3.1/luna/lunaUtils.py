from abc import ABCMeta, abstractmethod
from luna.azuremlLunaUtils import AzureMLLunaUtils
from luna.mlflowLunaUtils import MLflowLunaUtils
from luna.localLunaUtils import LocalLunaUtils

import yaml
import io
import argparse
import json

class LunaUtils(object):
    
    __metaclass__ = ABCMeta

    def ParseArguments(self):
        return self._args, self._userInput

    def Init(self, luna_config, run_mode, args, userInput):
        self._luna_config = luna_config
        self._run_mode = run_mode
        self._args= args
        self._userInput = userInput

    @property
    def luna_config(self):
        return self._luna_config

    @property
    def run_mode(self):
        return self.run_mode

    @property
    def args(self):
        return self._args

    @property
    def userInput(self):
        return self._userInput

    @abstractmethod
    def RegisterModel(self, model_path, description, luna_python_model=None):
        """
        register model
        """

    @abstractmethod
    def GetModelPath(self, context):
        """
        get model path
        """

    @abstractmethod
    def DeployModel(self):
        """
        deploy model
        """

    @abstractmethod
    def DownloadModel(self, model_path):
        """
        download model
        """

    @staticmethod
    def Create(luna_config_file='luna_config.yml', run_mode='default', run_type='default', parameters={}):
        with open(luna_config_file) as file:
            luna_config = yaml.full_load(file)
        
        if run_type != 'default':
            args, userInput = LunaUtils.ParseArgument(run_type)
        else:
            args = parameters
            userInput = {}
        
        if run_mode == 'default':
            run_mode = luna_config['run_mode']

        if run_mode == 'azureml':
            utils = AzureMLLunaUtils()
        elif run_mode == 'mlflow':
            utils = MLflowLunaUtils()
        elif run_mode == 'local':
            utils = LocalLunaUtils()

        utils.Init(luna_config, run_mode, args, userInput)
        return utils

    @staticmethod
    def ParseArgument(run_type):
        
        parser = argparse.ArgumentParser(run_type)

        parser.add_argument("--runMode", type=str, help="run mode")
        parser.add_argument("--userInput", type=str, help="input data")
        parser.add_argument("--modelId", type=str, help="model key")

        if run_type == 'inference' or run_type == 'batchinference':
            parser.add_argument("--operationId", type=str, help="run id")
        elif run_type == 'training' or run_type == 'train':
            parser.add_argument("--userId", type=str, help="user id")
            parser.add_argument("--productName", type=str, help="product name")
            parser.add_argument("--deploymentName", type=str, help="deployment name")
            parser.add_argument("--apiVersion", type=str, help="api version")
            parser.add_argument("--subscriptionId", type=str, help="subscription id")
        elif run_type == 'deployment' or run_type == 'deploy':
            parser.add_argument("--userId", type=str, help="user id")
            parser.add_argument("--productName", type=str, help="product name")
            parser.add_argument("--deploymentName", type=str, help="deployment name")
            parser.add_argument("--apiVersion", type=str, help="api version")
            parser.add_argument("--subscriptionId", type=str, help="subscription id")
            parser.add_argument("--endpointId", type=str, help="endpoint id")

        args = parser.parse_args()
        userInput = json.loads(args.userInput)
        return args, userInput