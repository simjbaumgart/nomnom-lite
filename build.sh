#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
python3 -m pip install -r backend/requirements.txt

echo "Building Frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Moving frontend build to backend/static..."
mkdir -p backend/static
rm -rf backend/static/*
cp -r frontend/dist/* backend/static/

echo "Build complete!"
