# chimera

## Overview

Chimera is a web application designed to provide a user-friendly interface for managing and interacting with various services. It is built using modern web technologies and aims to simplify the deployment and management of applications.

## Running chimera

### Development Mode

To run chimera in development mode, you can use the following command:

#### Local

```bash
fastapi dev --host 0.0.0.0 --port 80 ./src/main.py
```

#### Dockerfile

```bash
docker build -t local:chimera .
docker run --rm -v ./src:/app/src -p 80:80 --name chimera local:chimera
```

#### Docker Compose

```bash
docker compose up --build --watch
# or to just run without rebuilding
docker compose watch
```

### Production Mode
To run chimera in production mode, you can use the following command:

```bash
docker compose -f compose.yml up -d
# and to stop the services
docker compose -f compose.yml down
```

## CLI

Chimera provides a command-line interface (CLI) for various administrative tasks. You can access the CLI using the following command:

```bash
docker compose exec web python ./cli.py --help
```
