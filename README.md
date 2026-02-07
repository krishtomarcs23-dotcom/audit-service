Audit Service

A Dockerized audit logging microservice built with FastAPI, PostgreSQL, and Alembic.
It records and stores audit events (who did what and when) and is designed to integrate with other microservices in a production-style setup.
🏛️ Architecture Overview

This Audit Service is implemented as an independent microservice responsible for capturing and persisting audit events across the system. It is designed to be loosely coupled and easily integrated with other services such as authentication or order management.

The service is built using FastAPI and runs inside a Docker container. It connects to a PostgreSQL database running in a separate container within the same Docker Compose network. Communication between services relies on Docker service names, ensuring consistent behavior across development and production-like environments.

Database interactions are managed using SQLAlchemy, while Alembic is used for database schema versioning and migrations. The core database schema existed prior to Alembic integration, and Alembic was introduced to manage all subsequent schema evolution in a controlled and versioned manner, starting with performance-oriented improvements.

Audit data is stored in a dedicated audit_events table containing the event type, the actor responsible for the event, and a timestamp. Indexes on these fields support efficient querying for common access patterns such as filtering by user, event type, and time ranges.

All database migrations are executed from within the service container, ensuring that Alembic operates with the same environment variables, networking configuration, and database connectivity as the running application. This avoids host-specific assumptions such as the use of localhost and closely mirrors real-world production deployments.

Overall, the architecture emphasizes clear separation of concerns, container-native configuration, and safe, version-controlled database evolution.

🚀 Features

FastAPI-based REST API

PostgreSQL database

Docker & Docker Compose first (no localhost assumptions)

Alembic for database migrations

Indexed audit table for fast queries

Clean separation of configuration and code

CI workflow included

🏗️ Tech Stack

Backend: FastAPI

Database: PostgreSQL 15

ORM: SQLAlchemy

Migrations: Alembic

Containerization: Docker, Docker Compose

📁 Project Structure
audit-service/
├── alembic/                 # Alembic migrations
│   └── versions/
├── .github/workflows/ci.yml # CI pipeline
├── db.py                    # Database configuration
├── models.py                # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── main.py                  # FastAPI entry point
├── auth.py                  # Authentication utilities
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── runbook.md
└── README.md

🗄️ Database Design
Table: audit_events
Column	Type	Description
id	Integer	Primary key
event_type	String	Type of event (LOGIN, CREATE…)
actor	String	User or service performing it
timestamp	DateTime	Event creation time
Indexes

For performance, the following indexes are applied:

event_type

actor

timestamp

Indexes are managed via Alembic migrations.

⚙️ Environment Variables

Create a .env file (not committed):

DB_USER=audituser
DB_PASSWORD=auditpass
DB_NAME=auditdb
DB_HOST=audit-postgres
DB_PORT=5432

DATABASE_URL=postgresql://audituser:auditpass@audit-postgres:5432/auditdb

API_KEY=supersecretkey123


⚠️ .env is ignored via .gitignore to avoid leaking secrets.

🐳 Running the Service (Docker-only)

Start everything using Docker Compose:

docker compose up --build


The API will be available at:

http://localhost:8000

🧬 Database Migrations (Alembic)

All migrations are executed inside the service container to ensure consistent networking.

Check migration history
docker compose exec audit-service alembic history

Apply migrations
docker compose exec audit-service alembic upgrade head


Alembic is the single source of truth for schema management.

🔌 Example Audit Event

A typical audit event includes:

what happened (event_type)

who performed it (actor)

when it happened (timestamp)

This service is intended to be called asynchronously by other services (Auth, Orders, etc.).

🧠 Design Notes

The database schema was created before Alembic was introduced.

Alembic now manages all future schema evolution (indexes, changes).

Migrations are append-only and immutable once applied.

Service-to-service communication assumes Docker networking.

📌 Use Cases

Authentication audit logs

Order lifecycle tracking

Compliance and traceability

System activity monitoring

📄 License

This project is intended for educational and demonstration purposes.

