#!/bin/bash
cd frontend
npm install
chmod +x ./node_modules/.bin/vite
npx vite build
