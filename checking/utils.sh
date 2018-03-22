#!/bin/bash

# Helper functions for checks written in bash

function logging::info {
    echo "$1"
}

function logging::debug {
    if [ "x$DEBUG" = "x" ]; then
        return
    fi
    echo -e "\n  | DEBUG   | $1"
}

function logging::error {
    echo 1>&2 "$1"
}
