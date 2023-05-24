#!/bin/bash
python3.10 -m pip install --upgrade pip
python3.10 -m pip install --no-cache-dir -r requirements.txt
python3.10 -m flake8
python3.10 -m pytest
