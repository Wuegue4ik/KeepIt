# Deployment Guide

This document contains a step-by-step guide to deploying the **KeepIt** application.

## Cloning a repository

```bash
git clone https://github.com/Wuegue4ik/KeepIt.git /project-name
```

## Environment variables

Before launching, you need to create a `.env` file in the project's root directory.

| Variable | Description |
| :--- | :--- |
| `DB_LOGIN` | PostgreSQL database username |
| `DB_PASSWORD` | Database user password |
| `DB_HOST` | PostgreSQL connection address/host |
| `DB_PORT` | PostgreSQL connection port |
| `DB_NAME` | Database name |
| `REDIS_URL` | URL string for connecting to the Redis server |
| `CORS_ORIGINS` | Comma-separated list of allowed sources (CORS) |
| `OPENAPI_URL` | Link/path to the OpenAPI (Swagger) specification |

You can view example values ​​in `.env.example` in the project's root directory.

## Frontend

Install frontend dependencies:

```bash
cd /project-name/frontend
npm install && npm run build
npm run generate-api
```

## Backend

Install frontend dependencies:

```bash
cd /project-name/backend

python -m venv .venv
source .venv/bin/activate  # On Linux / macOS
# Or
# .venv\Scripts\activate
# On Windows

pip install -r requirements.txt
```

## Application update

```bash
git pull origin main

```

I don't think this application will receive any further updates.

# Deployment using Nix packages

```bash
git clone https://github.com/Wuegue4ik/KeepIt.git /project-name
cd /project-name
nix-shell
```

## Environment variables

Don't forget that you need to create a `.env` file in the project's root directory.