#!/bin/bash
set -e

echo "Building resurrexi.io..."

# Run build script
python3 build.py

echo ""
echo "Deploying to SudoSenpai..."

# Create directory if it doesn't exist
ssh sudosenpai@192.168.2.49 "mkdir -p /mnt/storage/resurrexi-io"

# Rsync entire project (for K8s PVC mounting)
rsync -avz --delete \
  --exclude='.git' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='venv' \
  ./ sudosenpai@192.168.2.49:/mnt/storage/resurrexi-io/

echo ""
echo "✓ Deployment complete!"
echo "Site files synced to: sudosenpai:/mnt/storage/resurrexi-io/"
echo ""
echo "To deploy to K8s:"
echo "  kubectl apply -f k8s/"
echo "  kubectl -n resurrexi-io rollout restart deployment/resurrexi-io"
echo ""
echo "Access via NodePort: http://192.168.2.49:30801"
