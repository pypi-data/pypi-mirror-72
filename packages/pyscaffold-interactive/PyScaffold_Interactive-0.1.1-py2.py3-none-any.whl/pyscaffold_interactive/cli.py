# -*- coding: utf-8 -*-
"""
Interactively generate a Python project template with customizations
using PyScaffold
"""

import argparse
import sys
import logging
from collections.abc import Iterable

import click
from pyscaffold import templates, info
from pyscaffold.api import create_project
from pyscaffold.extensions.tox import Tox
from pyscaffold.extensions.travis import Travis

from pyscaffold_interactive import __version__

__author__ = "Sarthak Jariwala"
__copyright__ = "Sarthak Jariwala"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def prompt_text(text, default=None):
  """Prompt user text input
  """
  prompt_ans = click.prompt(click.style(text, fg="blue"), default=default)
  return prompt_ans


def prompt_choice(text, choices, default=None):
  """Prompt user input from provided choices
  """
  # choices must be iterable
  assert isinstance(choices, Iterable)

  prompt_ans = click.prompt(
    click.style(text, fg="blue"),
    show_choices=True,
    type=click.Choice(choices, case_sensitive=False),
    default=default)
  
  return prompt_ans


def main():
  """Interactive Python project template setup using PyScaffold
  """

  license_choices = templates.licenses.keys()
  extensions = []

  click.echo(
    click.style(f"\nPyScaffold-Interactive - A tool to interactively "+
    "create python project templates using PyScaffold\n", 
    fg="green")
  )

  project_name = prompt_text("Enter your project name ",default="PyProject")

  author = prompt_text("Package author name ", default=info.username())

  email = prompt_text("Author email", default=info.email())

  url = prompt_text("Project URL", 
  default="https://github.com/SarthakJariwala/PyScaffold-Interactive")

  description = prompt_text(
    "Enter package description\n",
    default="Generated using PyScaffold and PyScaffold-Interactive")

  license = prompt_choice("Choose License\n", license_choices, default='mit').lower()

  make_tox = prompt_choice(
    "Generate config files for automated testing using tox? ",
    ['y','n'], default='y').lower()

  if make_tox == 'y': extensions.append(Tox('tox'))

  create_travis = prompt_choice(
    "Generate config and script files for Travis CI.? ",
    ['y','n'], default='y').lower()

  if create_travis == 'y': extensions.append(Travis('travis'))

  create_project(
    project=project_name,
    license=license,
    extensions=extensions,
    opts={
      "description":f"{description}",
      "author":f"{author}",
      "email":f"{email}",
      "url":f"{url}"
    }
  )

  click.echo(
    click.style(f"\nSuccess! {project_name} created. Lets code!", fg="green")
  )

  click.echo(
    click.style("\nAll putup commands are also available. For help - ", 
    fg="green") + 
    click.style("'putup --help'", fg='red')
  )


def run():
    """Entry point for console_scripts
    """
    main()


if __name__ == "__main__":
    run()
