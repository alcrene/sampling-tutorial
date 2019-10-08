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

To run the code, change to the `run` directory. If it isn't already, activate the virtual environment

    source venv/bin/activate
    
Running a script is then done by executing a line of the form

>>>> Change execution call as needed <<<<

    python ../code/[script file] params/[param file] ""

for example,

    python ../code/gradient_descent.py params/gradient_descent.py ""

Note the extra quotes at the end – this is an artifact of the way we've accomodated parallelized calls.

>>>> Sumatra/mackelab.smttk only section >>>>

Executing through `Sumatra` is very similar

    smt run -m ../code/[script file] params/[param file] ""

To execute multiple runs at once, optionally providing the number of cores to use, use the provided `smttk` wrapper for `Sumatra`:
    
    smttk run -n[cores] -m ../code/[script file] params: params/[param file 1] params/[param file 2] ...
    
Note that when using `smttk` we don't need the trailing quotes.
If only one parameter file is provided, `params:` is not necessary:

    smttk run -n[cores] -m ../code/[script file] params/[param file]
    
Any parameter file can use the specialized [expansion syntax](#parameter-expansion-syntax) to define a range of parameters to iterate over.
    
<<<< End Sumatra/mackelab.smttk specific section <<<<
    
# Running in a Jupyter Lab

If you used the installation script, the virtual environment is already registered for use with Jupyter. Just make sure to select it by clicking on "Change kernel" within Jupyter Lab; the kernel name will match this directory.

If you didn't run the installation script you will need to register the kernel yourself by following the instructions [here](https://ipython.readthedocs.io/en/stable/install/kernel_install.html). In brief,

    source venv/bin/activate
    python -m ipykernel install --user --name [kernel name] --display-name "[kernel display name]"
    
>>>> mackelab.smttk specific >>>>

# Parameter expansion syntax

Parameter files follow the same format as NeuroEnsemble's [Parameters](https://parameters.readthedocs.io/en/latest/) package. One addition is made to the format to allow easily specifying ranges of parameters. For example, if a script requires a single parameter `mu` and$ that we want to run it with values 1, 5 and 20, we would write the following in the parameters file:

    {
      mu: *[1, 5, 20]
    }

This is only supported when calling with `smttk`.

<<<< end mackelab.smttk specific <<<<

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
