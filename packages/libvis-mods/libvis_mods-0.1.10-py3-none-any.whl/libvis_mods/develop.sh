#!/bin/bash

: ${1?"Usage: $0 SOURCES_PATH"}

cd $1

if yarn -v; then
    yarn
    yarn dev
elif npm -v; then
    npm i
    npm run dev
else
    >&2 echo "You don't have neither yarn nor npm installed."
fi

