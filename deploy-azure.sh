#!/usr/bin/env bash
# Manual deploy to Azure using the CLI.
# Prereqs: `az login` and an active subscription.
set -e

RG="labtracker-rg"
LOC="eastasia"
APP="labtesttracker-app"
ACR="labtrackeracr"
IMG="$ACR.azurecr.io/labtesttracker:latest"

echo "==> creating resource group"
az group create -n "$RG" -l "$LOC" -o none

echo "==> creating container registry"
az acr create -n "$ACR" -g "$RG" --sku Basic -o none

echo "==> building & pushing image to ACR"
az acr build -t "$IMG" -r "$ACR" .

echo "==> creating app service plan (Linux, B1)"
az appservice plan create -n labtracker-plan -g "$RG" --sku B1 --is-linux -o none

echo "==> creating web app from image"
az webapp create -n "$APP" -g "$RG" -p labtracker-plan -i "$IMG" -o none

echo "==> done. Open https://$APP.azurewebsites.net"
