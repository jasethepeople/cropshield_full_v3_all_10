#!/bin/bash
echo "Setting up Willard Valley Co-op demo..."
curl -X POST http://localhost:8000/field/analyze -H "Content-Type: application/json" -d '{"farm_id":"clark_22","polygon":[[-112.05,41.41],[-112.04,41.41],[-112.04,41.40],[-112.05,41.40]],"crop_type":"alfalfa"}'
echo "Co-op seeded. Check http://localhost:3000"
