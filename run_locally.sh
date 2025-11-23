# Set your tokens as environment variables before running this script
# export TELEGRAM_TOKEN='your_telegram_token_here'
# export NGROK_TOKEN='your_ngrok_token_here'  # Optional, only needed for ngrok mode
export DEV='true'
source venv/bin/activate
python3 -m src.__init__ ngrok
