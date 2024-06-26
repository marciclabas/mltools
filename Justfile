mod torch-utils
mod keras-utils
mod demetric
mod lines-dataset
mod files-dataset
mod ocr-dataset
mod checkptr

VENV := ".venv"
PYTHON := ".venv/bin/python"

help:
  @just --list

init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt