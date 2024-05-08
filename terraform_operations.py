import os
import sys
import subprocess
import logging
from base64 import b64decode

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%d-%m-%YT%H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run_command(cmd, *args, **kwargs):
    return subprocess.check_output(
        cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True
    )

def terraform_init(directory):
    os.chdir(directory)
    return run_command("terraform init")
    

def terraform_plan(directory):
    os.chdir(directory)
    return run_command("terraform plan -out=tfplan")
    

def process():
    for dir, subdirs, files in os.walk("."):
        if ".terraform" in dir:
            os.removedirs(".terraform")
        logger.info(f"Processing terraform files from dir {dir}")
        terraform_init(dir)
        terraform_plan(dir)


if __name__ == "__main__":
    process(os.getcwd())
