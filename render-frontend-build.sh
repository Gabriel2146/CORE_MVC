#!/bin/bash
# Script to build Vue frontend for Render deployment

echo "Installing frontend dependencies..."
npm install

echo "Building frontend for production..."
npm run build
