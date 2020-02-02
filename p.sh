#!/usr/bin/bash
p() {
  out="$(_p "$@")"
  exit_code=$?

  if [ ${exit_code} -eq 42 ]; then
    eval "$out"
    return $?
  else
    echo "$out"
    return ${exit_code}
  fi
}
