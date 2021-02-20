# AutoTrainingBooker
Disclaimer: Only for personal usage  
Python version: 3.8.8

## Getting started
### Installation
#### Windows, Linux and Mac OS X
1. Clone repo as zip or with: 

   ```
   $ git clone https://github.com/tdl1304/AutoTrainingBooker.git
   ```
2. Setup a virtual environment inside the folder of the repository.
    Simply enter into cmd/unix terminal:
    ##### Windows cmd
     ```
   $ cd AutoTrainingBooker
   $ python -m venv .
   $ .\Scripts\activate
   ```
   ##### Mac OS X/Linux terminal
     ```
   $ cd AutoTrainingBooker
   $ python -m venv .
   $ source bin/activate
   ```
   
   If everything were successful you should get something like this
   ```
   $ (AutoTrainingBooker) path-to-folder\AutoTrainingBooker>
   ```
3. Install all requirements using pip:
    ```
   $ pip install -r requirements.txt
   ```
4. Create a distribution with [PyInstaller](https://pypi.org/project/pyinstaller/).
While inside the same folder simply enter:
   ##### Windows and Linux
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
5. Optionally make a shortcut or just run the executable file  


