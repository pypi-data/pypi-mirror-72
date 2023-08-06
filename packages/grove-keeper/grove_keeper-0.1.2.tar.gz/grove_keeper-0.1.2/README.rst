==========================
Encrypt Tools for Good Bot
==========================

Why it exists
-------------

This tool is made to be used with Good Bot. Passwords prompt happen often and 
storing passwords in the program's YAML files would have been insanely unsafe, 
especially when considering that one of the main advantages of Good Bot is that
the scripts can be version controlled. To avoid annoying mistakes like pushing 
a password to Github, I made this package. 

If you provide the path towards the key to Good Bot, he will decrypt the 
passwords and use them to record your videos. All you need to do is to provide 
the path towards the passwords file and the key in the YAML file. Then, instead
of typing your passwords in the file, just write which passwords you want 
(Password 1 for the first password) and Good Bot will take care of the rest.

Remember that this program is to avoid mistakes, but it cannot make them 
disappear. Pushing your key and your password file to a remote repository will 
result in those passwords being compromised.

How it works
------------

This program uses `Click <https://click.palletsprojects.com/en/7.x/>`_ to 
create a CLI and `Fernet <https://cryptography.io/en/latest/fernet/>`_ to 
encrypt and decrypt passwords. Here is what is happening depending on the 
command you will be using.

add-password
^^^^^^^^^^^^

After prompting the user for a password, this command will encrypt the password 
and save it to an existing file. To add the new content, the script opens the 
file and splits it on newlines. To open the files, the program is using Click's
built in `file handler <https://click.palletsprojects.com/en/7.x/arguments/#file-arguments>`_. 
It then inserts the password at the provided 
index. While the new password is encrypted, the content of the file is not 
decrypted, nor is it analyzed by the program. The user is also deemed 
responsible of providing the same key to encrypt their new password as the one 
that was used to encrypt the rest of the file.

keygen
^^^^^^

This just uses the `cryptography <https://github.com/pyca/cryptography>`_ 
Python library to generate a Fernet key and writes it to a file.

new-passwords
^^^^^^^^^^^^^

After prompting the users for passwords and storing them in a list, the program
creates a file using Click's file handler and writes every password on a 
different line. This is the only way passwords are indexed. There is no other 
information stored to help classify passwords other than the lines they 
were written on.

Usage
-----

If the program is installed, all you have to do is type ``groveKeeper`` in the 
command line followed by the command corresponding to what you want to use the 
program for!

add-password
^^^^^^^^^^^^

Options
"""""""

``-p`` : Assuming the passwords are in a 0 indexed list, this is where the 
new password will be inserted.

Arguments
"""""""""

``EXISTING_FILE`` : The path towards the file to which your new password will
be written. This file needs to exist since it's opened in reading mode.

``KEY`` : The path to the key that will be used to encrypt the password.

keygen
^^^^^^

Arguments
"""""""""

``OUTPUT`` : A file where the key will be written. The file does not have to 
be created beforehand. This path should end with a filename with the ``.key``
extension. The program will still work with a text file but adding the 
extension is a good way to quickly locate key files and not delete them by 
mistake.

new-passwords
^^^^^^^^^^^^^

Options
"""""""

``-n`` : This in a positive integer representing the amount of passwords you 
want to add to the file that will be created.

Arguments
"""""""""

``OUTPUT`` : A path and a filename. This is where the encrypted passwords 
will be written. The end of the path must be the name of a file.

``KEY`` : The location of the key that will be used to encrypt the passwords.

Finally, the program has simple help messages if you are ever stuck. Just 
typing ``grove-keeper`` will echo possible commands and options.

Use with caution ⚠️ . 
^^^^^^^^^^^^^^^^^^^^^

While this program is meant to make Good Bot safer, it still has its flaws. 
The passwords you encrypt can always be decrypted by anybody who possesses the 
key. **Keep it safely!** Creating new passwords and accounts exclusively for 
your tutorials is highly recommended.

Installation
------------

You can install this program using:


``pip install grove-keeper``

You can also clone this repo and invoke the script with Python:

``python [YOUR_PATH]/cli.py``

