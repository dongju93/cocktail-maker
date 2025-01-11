#!/bin/zsh
find . -type d -name "__pycache__" -exec rm -rf {} +
uv sync -U --compile-bytecode
