# Makefile

# Variables
PYTHON := python3
PIP := pip3
REQUIREMENTS := Dashboard/requirements.txt
MAIN_SCRIPT := Dashboard/main.py

# Default target
.PHONY: all
all: run

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r $(REQUIREMENTS)

# Run the main script
.PHONY: run
run:
	$(PYTHON) $(MAIN_SCRIPT)

# Clean (optional)
.PHONY: clean
clean:
	rm -rf __pycache__
