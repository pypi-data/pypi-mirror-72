from setuptools import setup
import sys

if sys.version_info < (3, 4, 0, 'final', 0):
    raise SystemExit('Python 3.4.0 or later is required !')
    

setup(
    name = "PyIpCom",
    version = "1.0",
    author = "Himanshu Jha",
    py_modules=["PyIpCom"],
    install_requires = ["PyGithub"],
)