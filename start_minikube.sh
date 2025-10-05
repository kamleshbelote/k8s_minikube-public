#!/bin/bash

echo "Stopping Minikube..."
minikube stop
sleep 5  # Wait 5 seconds

echo "Starting Minikube..."
minikube start
sleep 10  # Wait 10 seconds to ensure Minikube fully starts

echo "Enabling metrics-server..."
minikube addons enable metrics-server
sleep 5  # Wait 5 seconds

echo "Starting Minikube dashboard..."
minikube dashboard

# command to run this command: ./start_minikube.sh