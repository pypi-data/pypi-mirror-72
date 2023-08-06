# Steps for using PyHandEarth Shell Script

*DISCLAIMER: I don't how this will work if you already have parts of this installed. I deleted Google Earth Pro and the virtual environment prior to running this and it installed everything as expected on my system.*

Make sure to download the PyHand_Earth repo from github before running this script. The script will download the model to /home/your_username_here/Desktop/PyHand_Earth/tyler/testing by default.
Edit the last part of the curl command on line 29 of the script to change the directory if necessary.

1. Download PyHandEarth.sh

2. Place the file in your /home/your_username_here/ directory

3. In terminal, navigate to /home/your_username_here/ directory
- You can access this directory in the terminal using `cd ~` or `cd /home/your_username_here`

4. Run `chmod +x PyHandEarth.sh` in terminal. 
- This sets the execute permission for a shell script

5. Run `./PyHandEarth` in terminal. 
- This executes the shell script

### After Running the Script
- Google Earth Pro should be installed and accessible in your app drawer 
- Additionally, a virtual environment folder and the needed project dependencies should be created at /home/your_username_here/earth01
- As mentioned at the top, the model will be downloaded to /home/your_username_here/Desktop/PyHand_Earth/tyler/testing
