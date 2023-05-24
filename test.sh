#!/bin/bash
python3.10 -m pip install --upgrade pip > /dev/null
python3.10 -m pip install --no-cache-dir -r requirements.txt > /dev/null
python3.10 -m flake8
python3.10 -m pytest
