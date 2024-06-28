#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up Python environment..."
python -m compileall .

echo "Build completed successfully!"
