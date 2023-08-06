#! /usr/bin/python3
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import List


class PGPUtilConfigurationError(Exception):
    def __init__(self, message):
        super().__init__(message)


PGP_UTILS_HOME: Path = os.getenv("PGP_UTILS_HOME")

if not PGP_UTILS_HOME:
    PGP_UTILS_HOME = Path.home() / ".config" / "pgp-utils"
else:
    PGP_UTILS_HOME = Path(PGP_UTILS_HOME)

CONFIG = None
try:
    config_file: Path = PGP_UTILS_HOME / "config.json"
    if not config_file.exists():
        raise PGPUtilConfigurationError(
            "Config file not found, ensure you have set PGP_UTILS_HOME correctly if the config is not in the default location."
        )
    if not config_file.is_file():
        raise PGPUtilConfigurationError("Detected config is not a file.")
    CONFIG = json.loads(config_file.read_text())
except json.JSONDecodeError:
    raise PGPUtilConfigurationError("The provided config file is not valid json.")


def validate_config(config):
    if not config:
        raise PGPUtilConfigurationError(
            "Configuration file successfully loaded, but value is `None`."
        )
    if "key_id" not in config:
        raise PGPUtilConfigurationError(
            "Configuration does not contain the required value `key_id`."
        )
    return


def _run_command(command):
    subprocess.Popen(command, shell=True)


def switch_yubikey(args):
    _run_command('gpg-connect-agent "scd serialno" "learn --force" /bye')


def encrypt(args):
    recipients = " ".join(f"--recipient {r}" for r in args.recipients)
    _run_command(
        f"cat {args.file} | gpg --encrypt --armor {recipients} -o {args.file}.encrypted"
    )


def decrypt(args):
    _run_command(f"gpg --decrypt --armor {args.file}")


def sign(args):
    _run_command(f"cat {args.file} | gpg --armor --clearsign > {args.file}.signed")


def verify(args):
    _run_command(f"gpg --verify {args.file}")


def main():
    validate_config(CONFIG)
    key_id = CONFIG.get("key_id")
    parser = argparse.ArgumentParser(
        description="A wrapper for common pgp/yubikey tasks."
    )
    subparsers = parser.add_subparsers(dest="task")

    switch_parser = subparsers.add_parser("switch")
    switch_parser.set_defaults(func=switch_yubikey)

    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("file")
    encrypt_parser.add_argument("-r", "--recipients", nargs="+", default=(key_id,))
    encrypt_parser.set_defaults(func=encrypt)

    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("file")
    decrypt_parser.set_defaults(func=decrypt)

    sign_parser = subparsers.add_parser("sign")
    sign_parser.add_argument("file")
    sign_parser.set_defaults(func=sign)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("file")
    verify_parser.set_defaults(func=verify)

    args = parser.parse_args()
    args.func(args)

