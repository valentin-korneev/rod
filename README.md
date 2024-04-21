# Rod

Base project for Django apps

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run

### Development
```bash
docker compose up -d --build
```

### Production
```bash
docker compose --profile prod up -d --build
```