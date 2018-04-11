#!/bin/bash

# Helper functions for checks written in bash

function log::info {
    echo "$1"
}

function log::debug {
    if [ "x$DEBUG" = "x" ]; then
        return
    fi
    echo "$1"
}

function log::error {
    echo 1>&2 "$1"
}
