#!/bin/bash

target_version="latest"

function build_addon() {
  cd ..
  cd addon
  rm -f *.zip
  blender --command extension build
  blender --command extension server-generate --repo-dir=. --html
  blender --command extension server-generate --repo-dir=.
  mv *.zip ../site/
  mv *.html ../site/
  mv *.json ../site/
  cd ..
}

function build_ekur() {
  cd ..
  cd ekur
  cargo build --release
  mv -f target/release/ekur "../build/ekur-$target_version"
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -b|--blender) build_addon ;;
        -e|--ekur) build_ekur ;;
        -v|--version) target_version="$2"; shift ;;
        -h|--help) echo "Usage: $0 [-b|--blender] [-e|--ekur] [-v|--version VERSION]"; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; echo "Use -h or --help for usage information"; exit 1 ;;
    esac
    shift
done
