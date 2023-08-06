import asyncio  # pytype: disable=pyi-error
import os
import shutil
import sys
import yaml

import aiohttp
import click
import dask
from distributed.utils import tmpfile

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """ Coiled command line tool
    """
    pass


@cli.group(context_settings=CONTEXT_SETTINGS)
def env():
    pass


@env.command(
    context_settings=CONTEXT_SETTINGS,
    short_help="Create Coiled conda software environment locally",
)
@click.option("-n", "--name", help="Name of environment")
@click.argument("coiled_uri")
def create(name, coiled_uri):
    if shutil.which("conda") is None:
        raise RuntimeError(
            "Conda must be installed in order to use 'coiled env create'"
        )
    asyncio.run(create_conda_env(env_name=name, uri=coiled_uri))


async def create_conda_env(env_name, uri):
    token = dask.config.get("coiled.cloud.token")
    async with aiohttp.ClientSession(
        headers={"Authorization": "Token " + token}
    ) as session:
        account, name = uri.split("/")
        server = dask.config.get("coiled.cloud.server")
        response = await session.request(
            "GET", server + f"/api/v1/{account}/software_environments/{name}/?cli=true",
        )
        if response.status >= 400:
            text = await response.text()
            raise Exception(text)

        results = await response.json()
        if sys.platform == "linux":
            platform = "linux"
        elif sys.platform == "darwin":
            platform = "osx"
        elif sys.platform == "win32":
            platform = "windows"
        else:
            raise ValueError(f"Invalid platform {sys.platform} encountered")

        solved_spec = results[f"solved_spec_{platform}"]
        with tmpfile(extension="yml") as fn:
            with open(fn, mode="w") as f:
                yaml.dump(yaml.safe_load(solved_spec), f)

            if env_name is None:
                env_name = f"coiled-{account}-{name}"
            conda = os.environ["CONDA_EXE"]
            proc = await asyncio.create_subprocess_shell(
                f"{conda} env create -n {env_name} -f {f.name}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            while proc.returncode is None:
                await asyncio.sleep(0.5)
                async for line in proc.stdout:
                    print(line.decode())
                async for line in proc.stderr:
                    print(line.decode())
