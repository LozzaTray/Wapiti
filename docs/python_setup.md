# Python Setup Docs

## Virtual Environment VENV

It is easiest to use a python virtual environment so we are all working from the same base of installed packages. First we need to pick a base python to work from (I picked `python3.X`). You need to be able to access pip for this particular version of python. `python3 -m pip` is the most reliable way of doing this that I have found. The `-m` flag just tells the shell to look inside the python package directory.

We now need to install the venv package (called **virtualenv** by pip), as you would any other package.

```python3 -m pip install virtualenv```

If you get a permissions error try adding the `--user` flag after the install command. This will only install the package for the current user. Now navigate to the root directory of the project and type the following command.

```python3 -m venv .venv```

This will create a virtual python environment inside a directory `.venv`. If you cannot find the module `venv` then try replacing this with `virtualenv`. To activate the python virtual environment use the command.

```source .venv/bin/activate```

A little prefix should have appeared to the left-hand side of your terminal telling you which environment you are in. You can leave the venv whenever you want with `deactivate`. While you are in the virtual environment any pip or python commands should use the venv version of python.