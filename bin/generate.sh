#! /usr/bin/env bash
p=/tmp/kick/a
rm -fr "$p" ; mkdir -p "$p" ;  ./bin/kick "$p" && ls "$p" && code "$p"