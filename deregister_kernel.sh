echo "Deregistering the kernel will make it unavailable to Jupyter."
echo "To completely remove it for your system, delete the virtual environment after it has been deregistered."
echo ""

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIRNAME=${PWD##*/}
KERNELNAME="${DIRNAME//\ /_}"   # Replace spaces with underscores

source venv/bin/activate
jupyter kernelspec remove $KERNELNAME
deactivate
