PYTHON := python3
VENV   := .venv
BIN    := $(VENV)/bin/python

.PHONY: setup run demo clean check

# First-time setup: create venv, install deps, scaffold .env
setup:
	@echo "Setting up..."
	$(PYTHON) -m venv $(VENV)
	$(BIN) -m pip install -r requirements.txt -q
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env — open it and add your CDATA_EMAIL, CDATA_ACCESS_TOKEN, and ANTHROPIC_API_KEY"; \
	else \
		echo ".env already exists, skipping"; \
	fi
	@echo "Done. Run 'make check' to verify credentials, then 'make run' or 'make demo'."

# Verify credentials and connection
check:
	$(BIN) -c "\
from dotenv import load_dotenv; load_dotenv(); \
import os; \
missing = [k for k in ['CDATA_EMAIL','CDATA_ACCESS_TOKEN','ANTHROPIC_API_KEY'] if not os.environ.get(k)]; \
print('Missing:', missing) if missing else print('All credentials present'); \
"

# Interactive mode
run:
	$(BIN) main.py

# Scripted demo (press Enter to advance between acts)
demo:
	$(BIN) demo.py

# Auto-advancing demo (no keypresses — good for recordings)
demo-auto:
	$(BIN) demo.py --auto

# Fast typing speed (good for rehearsal)
demo-fast:
	$(BIN) demo.py --fast

# Remove venv and caches
clean:
	rm -rf $(VENV) __pycache__ *.pyc
