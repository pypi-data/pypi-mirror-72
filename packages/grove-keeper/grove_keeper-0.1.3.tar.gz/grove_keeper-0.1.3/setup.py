# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grove_keeper']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'cryptography>=2.9.2,<3.0.0']

entry_points = \
{'console_scripts': ['groveKeeper = grove_keeper.cli:main']}

setup_kwargs = {
    'name': 'grove-keeper',
    'version': '0.1.3',
    'description': 'A simple password manager to be used with Good Bot.',
    'long_description': '==========================\nEncrypt Tools for Good Bot\n==========================\n\nWhy it exists\n-------------\n\nThis tool is made to be used with Good Bot. Passwords prompt happen often and \nstoring passwords in the program\'s YAML files would have been insanely unsafe, \nespecially when considering that one of the main advantages of Good Bot is that\nthe scripts can be version controlled. To avoid annoying mistakes like pushing \na password to Github, I made this package. \n\nIf you provide the path towards the key to Good Bot, he will decrypt the \npasswords and use them to record your videos. All you need to do is to provide \nthe path towards the passwords file and the key in the YAML file. Then, instead\nof typing your passwords in the file, just write which passwords you want \n(Password 1 for the first password) and Good Bot will take care of the rest.\n\nRemember that this program is to avoid mistakes, but it cannot make them \ndisappear. Pushing your key and your password file to a remote repository will \nresult in those passwords being compromised.\n\nHow it works\n------------\n\nThis program uses `Click <https://click.palletsprojects.com/en/7.x/>`_ to \ncreate a CLI and `Fernet <https://cryptography.io/en/latest/fernet/>`_ to \nencrypt and decrypt passwords. Here is what is happening depending on the \ncommand you will be using.\n\nadd-password\n^^^^^^^^^^^^\n\nAfter prompting the user for a password, this command will encrypt the password \nand save it to an existing file. To add the new content, the script opens the \nfile and splits it on newlines. To open the files, the program is using Click\'s\nbuilt in `file handler <https://click.palletsprojects.com/en/7.x/arguments/#file-arguments>`_. \nIt then inserts the password at the provided \nindex. While the new password is encrypted, the content of the file is not \ndecrypted, nor is it analyzed by the program. The user is also deemed \nresponsible of providing the same key to encrypt their new password as the one \nthat was used to encrypt the rest of the file.\n\nkeygen\n^^^^^^\n\nThis just uses the `cryptography <https://github.com/pyca/cryptography>`_ \nPython library to generate a Fernet key and writes it to a file.\n\nnew-passwords\n^^^^^^^^^^^^^\n\nAfter prompting the users for passwords and storing them in a list, the program\ncreates a file using Click\'s file handler and writes every password on a \ndifferent line. This is the only way passwords are indexed. There is no other \ninformation stored to help classify passwords other than the lines they \nwere written on.\n\nUsage\n-----\n\nIf the program is installed, all you have to do is type ``groveKeeper`` in the \ncommand line followed by the command corresponding to what you want to use the \nprogram for!\n\nadd-password\n^^^^^^^^^^^^\n\nOptions\n"""""""\n\n``-p`` : Assuming the passwords are in a 0 indexed list, this is where the \nnew password will be inserted.\n\nArguments\n"""""""""\n\n``EXISTING_FILE`` : The path towards the file to which your new password will\nbe written. This file needs to exist since it\'s opened in reading mode.\n\n``KEY`` : The path to the key that will be used to encrypt the password.\n\nkeygen\n^^^^^^\n\nArguments\n"""""""""\n\n``OUTPUT`` : A file where the key will be written. The file does not have to \nbe created beforehand. This path should end with a filename with the ``.key``\nextension. The program will still work with a text file but adding the \nextension is a good way to quickly locate key files and not delete them by \nmistake.\n\nnew-passwords\n^^^^^^^^^^^^^\n\nOptions\n"""""""\n\n``-n`` : This in a positive integer representing the amount of passwords you \nwant to add to the file that will be created.\n\nArguments\n"""""""""\n\n``OUTPUT`` : A path and a filename. This is where the encrypted passwords \nwill be written. The end of the path must be the name of a file.\n\n``KEY`` : The location of the key that will be used to encrypt the passwords.\n\nFinally, the program has simple help messages if you are ever stuck. Just \ntyping ``grove-keeper`` will echo possible commands and options.\n\nUse with caution ⚠️ . \n^^^^^^^^^^^^^^^^^^^^^\n\nWhile this program is meant to make Good Bot safer, it still has its flaws. \nThe passwords you encrypt can always be decrypted by anybody who possesses the \nkey. **Keep it safely!** Creating new passwords and accounts exclusively for \nyour tutorials is highly recommended.\n\nInstallation\n------------\n\nYou can install this program using:\n\n\n``pip install grove-keeper``\n\nYou can also clone this repo and invoke the script with Python:\n\n``python [YOUR_PATH]/cli.py``\n\n',
    'author': 'tricky',
    'author_email': 'etienne.parent@beon.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
