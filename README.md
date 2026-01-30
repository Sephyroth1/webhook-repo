# webhook-repo

This repository contains the webhook receiver and UI for the GitHub Webhook
assessment task.

It is organized as a **monorepo** containing both the backend and frontend.

## Overview

The application flow is:

GitHub → Webhook (Flask) → MongoDB → API → React UI (polls every 15 seconds)

The backend receives GitHub webhook events and stores minimal required data
in MongoDB.  
The frontend polls the backend every 15 seconds and displays the latest activity.

## Repository Structure

