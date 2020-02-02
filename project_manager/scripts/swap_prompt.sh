#!/usr/bin/bash

if [[ -z ${_P_CURRENT_PROJECT+x} ]]; then
  export PROMPT="${_P_OLD_PROMPT}"
else
  export _P_OLD_PROMPT=${PROMPT}
  new_prompt='[${_P_CURRENT_PROJECT}]'
  export PROMPT="$new_prompt${PROMPT}"
fi
