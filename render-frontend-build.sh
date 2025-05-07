#!/bin/bash
cd frontend
npm install
npm audit fix --force
chmod +x ./node_modules/.bin/vite
npx vite build
