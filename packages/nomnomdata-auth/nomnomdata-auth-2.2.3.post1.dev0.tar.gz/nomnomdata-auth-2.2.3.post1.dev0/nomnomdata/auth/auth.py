import json
import logging
from os import environ
from urllib.parse import urlparse

import click
from pycognito import Cognito
from requests.auth import AuthBase

from .vars import COGNITO_NETLOC_MAPPING, CREDSTORE_PATH, DEFAULT_PROFILE

_logger = logging.getLogger(__name__)


def get_profiles():
    if CREDSTORE_PATH.exists() and CREDSTORE_PATH.is_file():
        with CREDSTORE_PATH.open() as f:
            return json.load(f)
    else:
        raise Exception(
            "No NND credentials found, please use `nnd login` or set environment variables"
        )


def login(username, password, userpool_id, client_id):
    user = Cognito(
        userpool_id,
        client_id,
        username=username,
        access_key="dummy_not_used",
        secret_key="dummy_not_used",
        user_pool_region="us-east-1",
    )
    try:
        user.authenticate(password=password)
    except user.client.exceptions.UserNotFoundException:
        raise click.ClickException(f"Nom Nom Data username not found {username}")
    except user.client.exceptions.NotAuthorizedException:
        raise click.ClickException(f"Authorization failed {username}")
    except user.client.exceptions.PasswordResetRequiredException:
        raise click.ClickException(f"Password reset required for {username}")
    return user


class NNDAuth(AuthBase):
    def __init__(self, profile=DEFAULT_PROFILE):
        self.profile = DEFAULT_PROFILE
        self.overrides = {}
        if environ.get("NND_USERNAME") and environ.get("NND_PASSWORD"):
            _logger.info("Found environment variables will use those instead")
        else:
            self.creds = get_profiles()

    def __call__(self, request):
        netloc = urlparse(request.url).netloc
        userpool_id = COGNITO_NETLOC_MAPPING[netloc]["userpool-id"]
        client_id = COGNITO_NETLOC_MAPPING[netloc]["client-id"]

        if environ.get("NND_USERNAME") and environ.get("NND_PASSWORD"):
            cognito = login(
                username=environ.get("NND_USERNAME"),
                password=environ.get("NND_PASSWORD"),
                userpool_id=userpool_id,
                client_id=client_id,
            )
        else:
            cognito = Cognito(
                user_pool_id=userpool_id,
                client_id=client_id,
                id_token=self.creds[self.profile][netloc]["id-token"],
                access_token=self.creds[self.profile][netloc]["access-token"],
                refresh_token=self.creds[self.profile][netloc]["refresh-token"],
                access_key="dummy_not_used",
                secret_key="dummy_not_used",
                user_pool_region="us-east-1",
            )
        if cognito.check_token():
            _logger.info("Tokens refreshed")
            self.creds[self.profile][netloc]["access-token"] = cognito.access_token
            self.creds[self.profile][netloc]["refresh-token"] = cognito.refresh_token
            self.creds[self.profile][netloc]["id-token"] = cognito.id_token
            with CREDSTORE_PATH.open("w") as f:
                json.dump(self.creds, f)
            CREDSTORE_PATH.chmod(0o600)

        request.headers["cognito-access-token"] = cognito.access_token
        request.headers["cognito-id-token"] = cognito.id_token
        return request
