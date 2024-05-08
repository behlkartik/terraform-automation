import os
import sys
import subprocess
import logging
from base64 import b64decode
from argparse import ArgumentParser

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%d-%m-%YT%H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run_command(cmd, *args, **kwargs):
    return subprocess.check_output(
        cmd,
        shell=True,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )


def terraform_init(directory):
    os.chdir(directory)
    logger.info(f"Directory {directory}")
    return run_command("terraform init")


def terraform_plan(directory):
    os.chdir(directory)
    logger.info(f"Directory {directory}")
    return run_command("terraform plan -out=tfplan")


def process(directory):
    for dir, subdirs, files in os.walk(directory):
        if ".terraform" in dir:
            run_command("rm -rf .terraform")
        if "main.tf" in files:
            logger.info(f"Processing terraform files from dir {dir}")
            terraform_init(dir)
            terraform_plan(dir)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog=__name__,
        description="Script to initialize terraform providers and get execution plan",
    )
    parser.add_argument("-dir", default=os.path.abspath("./infra"))
    cmd_line_args = parser.parse_args()
    process(os.path.abspath(cmd_line_args.dir))
