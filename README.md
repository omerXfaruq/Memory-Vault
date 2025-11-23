<div align="center">
  <h1> Memory-Vault</h1> 
  <em> Click on the image to try it</em> 

  [<img src="img/memory_vault_pp.png" alt="memory-vault" width=300>](http://t.me/memory_vault_bot)<br>
  <em>Whisper to future, Digital sticky notes, Learning machine</em>
</div>



Memory Vault is a Telegram bot that you can store your notes, and get reminded random notes, everyday. It is the simplest and easiest learning/remembering machine. Think of it like Digital Sticky Notes, but much more simple. Never forget your notes!

<br>


<div align="center">
<img src="img/sticky-notes.png" alt="drawing" width="300"/><br>
<em>(Just an engineer, without any design skills :D)</em>
</div>

# Introduction 

[omerXfaruq.github.io/Memory-Vault/](https://omerXfaruq.github.io/Memory-Vault/)




# Setup and Installation

## Requirements

- Python 3.12
- sqlite
- requirements

### Setup Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
# Edit .env with your actual tokens
```

Required environment variables:
- `TELEGRAM_TOKEN`: Your Telegram bot token

Optional:
- `NGROK_TOKEN`: For ngrok mode (prevents timeout)
- `DEV`: Set to `true` for development mode
- `PEM_FILE`: Path to SSL certificate for self-signed mode

## Running the Application

### Option 1: Using run_locally.sh (Recommended)

```bash
bash run_locally.sh [ngrok]
```

### Option 2: Run With Ngrok

Run without timeout limit:

```bash
# Make sure venv is activated
source venv/bin/activate

export NGROK_TOKEN={TOKEN} 
export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

Run with timeout limit:

```bash
# Make sure venv is activated
source venv/bin/activate

export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ ngrok
```

### Option 3: Run With Public IP

Run with self-signed ssl certificate:

```bash
# Make sure venv is activated
source venv/bin/activate

export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__ self-signed
```

Run with authority-signed ssl certificate:

```bash
# Make sure venv is activated
source venv/bin/activate

export TELEGRAM_TOKEN={TOKEN} 
python3 -m src.__init__
```

## Testing

Run all tests:

```bash
source venv/bin/activate
pytest tests/ -v
```


