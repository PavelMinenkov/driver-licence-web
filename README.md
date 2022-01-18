# Web part of Driver-Licence demos
Includes **Policy**, **Insurance**, **Carsharing** actors.

## Env variables
  - DATABASE_USER: postgres database user
  - DATABASE_PASSWORD: postgres database password
  - DATABASE_NAME: postgres database name
  - DATABASE_HOST: postgres host address

## Development 
To prepare dev environment in **PyCharm**, follow next steps:
  - Set env variable VERSION on dev machine to `dev` (example: `export VERSION=dev`)
  - Build docker image in PyCharm add Run/Debug configuration: Docker->Docker-Compose and set `compose file` to `docker-compose.yml` located in project root directory THEN run build
  - Prepare remote interpreter: File->Settings->Interpreter->Docker-Compose
  - Enable Django support: File->Settings->Languages&Frameworks (set settings to `settings\develop.py`)
  - Add run configuration: Run/Debug configuration: Django server, host: `0.0.0.0` port: `80`
  - Check `http://localhost` in browser