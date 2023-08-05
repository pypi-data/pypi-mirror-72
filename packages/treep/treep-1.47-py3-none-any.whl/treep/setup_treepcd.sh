# This file defines a shell function `treepcd` to easily change to the
# directory of a repository in the workspace.  To be able to use this function,
# you need to source this file (e.g. in your .bashrc).

# cd to the specified repository in the current workspace
# Usage:  treepcd <repository_name>
function treepcd () {
    repo_path=$(treep --path $1)
    if [ $? -eq 0 ]
    then
        cd ${repo_path}
    else
        # echo error message on stderr
        echo ${repo_path} 1>&2
        return 1
    fi
}

# add tab completion of repository names to treepcd
# based on https://iridakos.com/programming/2018/03/01/bash-programmable-completion-tutorial
function _treepcd_complete() {
    COMPREPLY=($(compgen -W "$(treep --local-repos)" "${COMP_WORDS[1]}"))
}
complete -F _treepcd_complete treepcd
