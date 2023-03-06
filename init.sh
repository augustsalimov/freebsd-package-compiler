#!/usr/bin/env bash

python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools
pip install -r requirements.txt
cp .env.example .env