#!/bin/bash

# API Demo Script for Clicker Game
# This script demonstrates how to use the API endpoints

echo "=== Clicker Game API Demo ==="

# Set the base URL
BASE_URL="http://localhost:8000"

# 1. Get player profile (requires authentication)
echo
echo "1. Getting player profile:"
curl -X GET "$BASE_URL/api/player/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"

# 2. Process clicks
echo
echo "2. Processing clicks:"
curl -X POST "$BASE_URL/api/click/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "clicks": 5,
    "timestamp": "2026-01-25T12:00:00Z",
    "energy": 995,
    "balance": 1005
  }'

# 3. List upgrades
echo
echo "3. Listing upgrades:"
curl -X GET "$BASE_URL/api/upgrades/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"

# 4. Purchase upgrade
echo
echo "4. Purchasing upgrade:"
curl -X POST "$BASE_URL/api/upgrades/purchase/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "upgrade_id": 1,
    "expected_cost": 100
  }'

# 5. Get daily rewards status
echo
echo "5. Getting daily rewards status:"
curl -X GET "$BASE_URL/api/daily-rewards/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"

# 6. Claim daily reward
echo
echo "6. Claiming daily reward:"
curl -X POST "$BASE_URL/api/daily-rewards/claim/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

# 7. List tasks
echo
echo "7. Listing tasks:"
curl -X GET "$BASE_URL/api/tasks/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json"

# 8. Claim task reward
echo
echo "8. Claiming task reward:"
curl -X POST "$BASE_URL/api/tasks/claim/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": 1
  }'

# 9. Sync player state
echo
echo "9. Syncing player state:"
curl -X POST "$BASE_URL/api/player/sync/" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "energy": 1000,
    "balance": 1500
  }'

echo
echo "=== API Demo Complete ==="
echo "Note: Replace YOUR_AUTH_TOKEN with a valid authentication token"
echo "Note: Make sure the Django server is running on localhost:8000"