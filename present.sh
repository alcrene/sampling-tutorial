 #!/bin/sh

# Change to the script's directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
 
venv/bin/jupyter nbconvert Introduction\ to\ sampling.ipynb --to slides --TagRemovePreprocessor.remove_input_tags={\"to_remove\"} --post serve
