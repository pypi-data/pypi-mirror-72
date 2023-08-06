# -*- coding: utf-8 -*-

import shutil, os
import pytest
import click
from click.testing import CliRunner
from pyscaffold_interactive import cli as pysci #import main, prompt_text, prompt_choice

__author__ = "Sarthak Jariwala"
__copyright__ = "Sarthak Jariwala"
__license__ = "mit"


@pytest.fixture
def runner():
    return CliRunner()

def test_default_vs_input(runner):
    """Test if the default value provided is overwritten by user input"""
    
    @click.command()
    def cli():
        ans = pysci.prompt_text("Project name", default="PyProject")
        click.echo(f'Project Name = {ans}')

    result = runner.invoke(cli, input="My Python Project\n")
    assert not result.exception
    assert result.output == "Project name [PyProject]: My Python Project\nProject Name = My Python Project\n"

def test_choices(runner):
    """Test if an error is thrown when user provides an input that is not in choices"""

    @click.command()
    def cli():
        ans = pysci.prompt_choice("Confrim", ['y', 'n'], default='y')
    
    result = runner.invoke(cli, input='z')

    assert result.output != 'y' # check if the output is not equal to default

def test_choice_iterable():
    """Test if choices are iterable"""
    
    with pytest.raises(AssertionError):
        pysci.prompt_choice("Confrim", 1)

def test_main(runner):
    """Test interactive creation of pyscaffold"""

    @click.command()
    def cli():
        return pysci.main()

    input="PyProject\nSarthak Jariwala\njariwala@uw.edu\nwww.example.com\nMy description\nmit\ny\ny\n"
    result = runner.invoke(cli, input=input)
    assert not result.exception
    assert result.exit_code == 0

    shutil.rmtree(os.path.join(os.getcwd(), "PyProject"))