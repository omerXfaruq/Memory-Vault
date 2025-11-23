
## Requirements

- Python 3.12
- sqlite
- requirements

### Setup

```bash
# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root (copy `.env.example` and fill in your values):

```bash
cp .env.example .env
# Edit .env with your actual tokens
```

Or set environment variables directly:
- `TELEGRAM_TOKEN` - Required
- `NGROK_TOKEN` - Optional, only needed for ngrok mode
- `DEV` - Optional, set to `true` for development mode

## Run With Ngrok

Run without timeout limit:

```bash
export NGROK_TOKEN={TOKEN} 
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

Run with timeout limit:

```bash
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

## Run With Public IP

Run with self-signed ssl certificate

```bash
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ self-signed
```

Run with authority-signed ssl certificate

```bash
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__
```
