# Contents

* Introduction
* Installation instructions
* Future edits

## Introduction

A simple GUI written in python3 to help keep track of pending repairs.

## Installation Instructions
Install as normal. Instructions provided below.

### Clone the repository
If you do not have git installed on your computer already, go to the [github repository]
(https://github.com/lm30/repairconsole) containing the source code.

On the right hand side, there is a green button labeled *Code*, it allows you multiple ways to clone this repository. Choose the one that best suits you.

### Set up instructions

Log into hostgator, go to "Remote MySQL" and add your IP to 'Add Access Host'.

Create a file called `dbInfoFile.txt` in the repairconsole directory and replace the brackets <> with the correct information.

> host <IP found on the hostgator site after logging in\>
>
> database <full name of the database for the repair console\>
>
> user <username of the user with access to that specific database in the repair console\>
>
> password <password associated with the username\>


### Create executable

Check if pip3 is installed on your computer using `pip3 --version`.

Install the standard pip install command to install the pyinstaller package which will be used to convert python code into an executable file:

`pip3 install pyinstaller`

Open the command prompt.

Change to the folder location where the python project is stored:

`cd folder_location`

Use the following command to convert the python file to a windows executable:

`pyinstaller --onefile <absolute path to the dbInfoFile.txt>:repairConsoleGUI repairConsoleGUI.py`

The executable file will be available in a new folder, **dist** which will be available at the same location as your python script.

# Future edits
Add a settings widget and frame to change whether automatic emails will be sent when a repair is finished or overdue. Also to select the overdue and finished colors and to change the number of days overdue.
	For now, to change the number of overdue days, go to the `overdueTable.py`, search for `overdue =` and change the value.

Hook up the automatic emails (already set up and ready to run) and create a repairer database in hostgator to send individual repairers their emails.

Archive finished entries after a set amount of days