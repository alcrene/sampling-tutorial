# Installation

If this package contains private repositories accessed through `ssh`, the easiest is to execute

    ssh-add

before starting the installation. (See <https://www.ssh.com/ssh/agent>.)

If installing on a remote machine, see the additional instructions [below](#extra-indications-for-installing-on-a-remote-server).

Note that you likely need to make sure that the path to this package contains no spaces (the newest version of virtualenv fixes this, but will take a while to trickle down to standard installations).

## Automatic installation

### Linux

Execute `install.sh` :

    chmod u+x install.sh
    ./install.sh
 
### MacOS, Windows

Unfortunately I don't yet have tested versions of the install script for these OSes. You will need to follow the manual instructions [below](#manual-installation).

# Running the code

After running the install script, open `START` from within a file browser. Alternatively,

    ./START
    
# Running in a Jupyter Lab

If you used the installation script, the virtual environment is already registered for use with Jupyter. Just make sure to select it by clicking on "Change kernel" within Jupyter Lab; the kernel name will match this directory.

If you didn't run the installation script you will need to register the kernel yourself by following the instructions [here](https://ipython.readthedocs.io/en/stable/install/kernel_install.html). In brief,

    source venv/bin/activate
    python -m ipykernel install --user --name [kernel name] --display-name "[kernel display name]"
    

# Manual installation

Change to the directory containing this file, create a virtual environment and activate it

  - Linux

      cd [project directory]
      python3 -m venv venv
      source venv/bin/activate

Upgrade the virtual environment's `pip`

    pip install --upgrade pip
    
Install project dependencies

    pip install -r requirements.txt
    
Install project code

    pip install ./python
    
Deactivate the virtual environment

    deactivate

# Extra indications for installing on a remote server

If there are no private repositories, the instructions above should work as-is.

If there are private repositories, make sure you have SSH agent forwarding configured. (<https://www.ssh.com/ssh/agent#sec-SSH-Agent-Forwarding>)
You can then run `ssh-add` on the local machine, before `ssh`-ing to the server and running the install script.

Note that agent forwarding may not work through additional clients such as [tmux](https://tmux.github.io/).
