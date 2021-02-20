# Auto Training Booker
**Python version: 3.8.8**  
Although it may work with other versions. Not tested yet.  
  
**How it works - in a nutshell**  
It checks for available bookings two days ahead at a specified time. 
It will check **every 2 minutes** at **1 hour** before the specified time. Once a booking has been made, it will wait till the next day and about the same hour. Terminating the program during runtime is **safe**.  
  
*Disclaimer: only for personal usage* 

### Table of Contents
* [Auto Training Booker](#auto-training-booker)
* [Getting started](#getting-started)
    * [Windows](#windows)
    * [Mac OS X](#mac-os-x)
    * [Linux Ubuntu](#linux-ubuntu)
* [Installation](#installation)
    * [Step 1](#clone-repo-as-zip-or-with)
    * [Step 2](#setup-a-virtual-environment-inside-the-folder-of-the-repository)
    * [Step 3](#install-all-requirements-using-pip)
    * [Step 4](#create-a-distribution-with-pyinstallerhttpspypiorgprojectpyinstaller)
    * [Step 5](#optionally-make-a-shortcut-or-just-run-the-executable-file)
    * [PyCharm](#pycharm)
* [How-to-use](#how-to-use)
    * [Setup](#setup)
* [Limitations](#limitations)
## Getting started
1. Install [python](https://www.python.org/downloads/release/python-388/) 
##### Windows 
2. Select "Add Python 3.8.8 to PATH"
3. Do a custom installation
4. Select pip (others, leave as default)
5. Hit next
6. Select:
   * Install for all users
   * Add Python to environment variables
   * Create shortcuts for installed applications
   * Precomplie standard libary
7. Customize Install Location and use: C:\Python38
8. Hit install

##### Mac OS X
* **Default installation**
##### Linux Ubuntu
    $ sudo apt-get install software-properties-common
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt-get update
    $ sudo apt-get install python3.8
## Installation
1. ##### Clone repo as zip or with: 

   ```
   $ git clone https://github.com/tdl1304/AutoTrainingBooker.git
   ```
2. ##### Setup a virtual environment inside the folder of the repository.
    Simply enter into cmd/unix terminal:
    ##### Windows cmd
     ```
   $ cd AutoTrainingBooker
   $ python -m venv .
   $ .\Scripts\activate
   ```
   ##### Mac OS X terminal
     ```
   $ cd AutoTrainingBooker
   $ python -m venv .
   $ source bin/activate
   ```
   ##### Linux terminal
     ```
   $ cd AutoTrainingBooker
   $ python3 -m venv .
   $ source bin/activate
   ```
   If everything were successful you should get something like this
   ```
   $ (AutoTrainingBooker) path-to-folder\AutoTrainingBooker>
   ```
3. ##### Install all requirements using pip:  
   **Use "pip3" instead of "pip" for Linux Ubuntu**
    ```
   $ pip install -r requirements.txt
   ```
   
4. ##### Create a distribution with [PyInstaller](https://pypi.org/project/pyinstaller/).
   While inside the same folder simply enter:
   ##### Windows and Linux Ubuntu
   ```
   $ pyinstaller booker.py -F --name "AutoTrainingBooker" --clean
   ```
   ##### Mac OS X
   ```
   $ pyinstaller booker.py -F 
   --name "AutoTrainingBooker" 
   --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk'
   --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' 
   --clean
   ```
   Once done, an executable file should be inside the folder AutoTrainingBooker\dist
5. ##### Optionally make a shortcut or just run the executable file  

### PyCharm
1. Create new project from git repository and paste in repo-link
2. Set your interpreter to python ~3.8 and install all requirements. How-to-do for [commandline](#install-all-requirements-using-pip).
3. If you want to create and executable follow this [step](#create-a-distribution-with-pyinstallerhttpspypiorgprojectpyinstaller)

## How-to-use
1. #### Setup
   * Username: examplestudent@stud.ntnu.no
   * Password: examplepassword **NOT THE SAME AS FEIDE**
   * Studio ID: XXX
     * Choices: 
        * Gløshaugen: 306
        * Dragvoll 307
        * Portalen: 308
        * DMMH: 402 
        * Moholt: 540
   * Booking time: 10:00
2. *Username* and *Password* are stored in **sit.psw**, and *Studio ID* 
    and *Booking time* are stored in **config.json**.  
  
    If you wish to edit any of these attributes, simply delete the files and rerun the program or edit the files in a texteditor.
3. It will try to book a session two days ahead at the desired *booking time*.

## Limitations
* Wrong username and password forces a crash, simply edit **sit.psw** [look here](#how-to-use)
  * In rare occurrences, the user is denied from access to sit.no, this could likely be because of many repeated failed attempts.
* Overlapping sessions will cause a crash and have to be fixed manually
* Program could crash if **Studio ID** or **Booking time** is invalid/not found [look here](#how-to-use)

## Updates
Using git:
   ```
   $ git status
   $ git pull 
   ```
TODO: Will implement automatic pulls with webhooks in the future.


