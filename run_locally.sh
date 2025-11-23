#!/bin/bash
# This script runs the Memory Vault application locally
# 
# Environment variables can be set in two ways:
# 1. Create a .env file in the project root (copy .env.example and fill in your values)
# 2. Export them directly: export TELEGRAM_TOKEN='your_token'
#
# The application will automatically load variables from .env file if it exists

export DEV='true'
source venv/bin/activate
python3 -m src.__init__ ${1:-}  # Pass 'ngrok' as argument to enable ngrok mode
