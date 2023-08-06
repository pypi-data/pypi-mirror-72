"""dock-r app install functions"""

import os

import runnow
import uio

import dock_r


WIN_BATCH_SCRIPT_TEMPLATE = """
docker pull {image}
docker run --rm -it -v %cd%:/home -w /home {image} %*
"""


LIN_SHELL_SCRIPT_TEMPLATE = """
#!/bin/bash
docker pull {image} >2>&1
docker run --rm -it -v ${cwd}:/home -w /home {image} %*
"""


def run(image: str, raise_error=True, rm=True):
    """Run an image as an app.

    The active directory will automatically be mapped on the container as a volume, and
    the container will be executed with the flags '-it' (interactive) and '--rm' (post-run
    cleanup).

    Parameters
    ----------
    image : str
        The image to run.
    raise_error : bool, optional
        False to ignore errors instead of raising them, by default True.
    rm : bool, optional
        Whether to remove the container after execution. Default is True to delete.
    """
    cwd = os.getcwd()
    dock_r.pull(image)
    runnow.run(f"docker run --rm -it -v {cwd}:/home -w /home {image}")


def install(image: str, alias: str):
    """Install the image under a new alias.

    Parameters
    ----------
    image : str
        The docker image to install.
    alias : str
        The alias to install under.
    """
    dock_r.pull(image)
    if uio.is_windows():
        _install_win(image, alias)
    else:
        _install_lin(image, alias)


def uninstall(alias: str):
    """Uninstalls an image alias.

    Parameters
    ----------
    alias : str
        The alias to uninstall.
    """
    if uio.is_windows():
        _uninstall_win(alias)
    else:
        _uninstall_lin(alias)


def _install_win(image: str, alias: str):
    script_txt = WIN_BATCH_SCRIPT_TEMPLATE.format(image=image)
    ext = "bat"
    installation_dir = os.path.realpath(f"~")
    installation_path = os.path.realpath(f"{installation_dir}/{alias}.{ext}")
    uio.create_text_file(installation_path, script_txt)


def _install_lin(image: str, alias: str):
    script_txt = LIN_SHELL_SCRIPT_TEMPLATE.format(image=image)
    ext = "sh"

    installation_dir = os.path.realpath(f"~")
    installation_path = os.path.realpath(f"{installation_dir}/{alias}.{ext}")
    uio.create_text_file(installation_path, script_txt)


def _uninstall_win(alias: str):
    ext = "bat"
    installation_dir = os.path.realpath(f"~")
    installation_path = os.path.realpath(f"{installation_dir}/{alias}.{ext}")
    uio.delete_file(installation_path)


def _uninstall_lin(alias: str):
    ext = "sh"
    installation_dir = os.path.realpath(f"~")
    installation_path = os.path.realpath(f"{installation_dir}/{alias}.{ext}")
    uio.delete_file(installation_path)
