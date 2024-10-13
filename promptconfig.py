import yaml
import os


class Config:
    _instance = None

    def __new__(cls, file_path=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize(file_path)
        return cls._instance

    def _initialize(self, file_path):
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
            self.system_message = config["persona"]["system_message"]
            self.retriever_prompt = config["retriever"]["query_retriever"]
            self.evaluator_prompt = config["evaluation"]["evaluator_prompt"]
            self.stage2_eval_prompt = config["evaluation"]["evaluator_prompt_stage2"]
            self.yamal_prompt = config["yaml"]["yaml_format_prompt"]
            self.yamal_prompt = config["perplexity"]["search_prompt"]
            self.yamal_prompt = config["anthropic"]["search_prompt"]


# Function to get the global configuration instance
promptlib = ""


def setprompt_config(file_path="prompt.yaml"):
    global promptlib
    promptlib = Config(file_path)
    return promptlib


# Initialize the global configuration instance
def getprompts():
    global promptlib
    promptfile = os.environ.get("MASTERPROMPT","prompt.yaml")
    if promptlib == "":
        promptlib = setprompt_config(promptfile)
    return promptlib
