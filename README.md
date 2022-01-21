# Web part of Driver-Licence demos
Includes **Policy**, **Insurance**, **Carsharing** actors.

## Env variables
  - DATABASE_USER: postgres database user
  - DATABASE_PASSWORD: postgres database password
  - DATABASE_NAME: postgres database name
  - DATABASE_HOST: postgres host address
  - REDIS_HOST, REDIS_PORT: redis server address

## Development 
Pre-requirements:
    - PyCharm professional installed
    - Docker & docker-compose installed (check it by typing `docker --version` and then `docker-compose --version`)

To prepare dev environment in **PyCharm**, follow next steps:
  - Set global env variable VERSION on dev machine to `dev` (example: `export VERSION=dev`) and restart PyCharm if needed to apply changes
  - Build docker image in PyCharm add Run/Debug configuration: Docker->Docker-Compose and set `compose file` to `docker-compose.yml` located in project root directory, set Services to `application` THEN run build
  - Prepare remote interpreter: File->Settings->Interpreter->Docker-Compose (set Service to `application`)
  - Enable Django support: File->Settings->Languages&Frameworks (set settings to `settings\develop.py`)
  - Add run configuration: Run/Debug configuration: Django server, host: `0.0.0.0` port: `80`
  - Check `http://localhost` in browser