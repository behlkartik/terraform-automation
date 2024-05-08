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


def perform_operations():
    tf_exist = run_command("terraform -version")
    for dir, subdirs, files in os.walk("."):
        if ".terraform" not in dir:
            logger.info(f"Processing terraform files from dir {dir}")
            for file in files:
                if "main.tf" in file:
                    try:
                        init_call = run_command(f"cd {dir} && terraform init && cd -")
                    except subprocess.CalledProcessError as ex:
                        logger.exception(
                            "Failed to download and install required providers"
                        )
                    try:
                        plan_call = run_command(
                            f"cd {dir} && terraform plan -out {dir}/tfplan && cd -"
                        )
                    except subprocess.CalledProcessError as ex:
                        logger.exception("Terraform plan failed")


if __name__ == "__main__":
    perform_operations()
