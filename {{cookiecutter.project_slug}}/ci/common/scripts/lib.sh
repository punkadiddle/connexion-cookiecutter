#!/bin/bash

COLOR_HEADER='\e[34;1m'
COLOR_RESET='\e[0m'

function line() {
    printf -v res '%120s' ' '
    printf "${COLOR_HEADER}%s${COLOR_RESET}\n" "${res// /─}"
}

function dline() {
    printf -v res '%120s' ' '
    printf "${COLOR_HEADER}%s${COLOR_RESET}\n" "${res// /═}"
}

function header() {
    printf -v res '%120s' ' '
    printf "\n${COLOR_HEADER}%s\n" "${res// /═}"
    printf '%-*s\n' 120 "$@"
    printf "${COLOR_HEADER}%s${COLOR_RESET}\n" "${res// /═}"
}