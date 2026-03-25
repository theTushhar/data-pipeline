# Customer Data Pipeline

A simple data pipeline with three components:
1. **Flask Mock Server**: Simulates a customer data source API.
2. **FastAPI Pipeline Service**: Fetches data from the mock server and saves it to a PostgreSQL database (configured via `.env`).
3. **External PostgreSQL**: The database is specified in the `.env` file (e.g., Aiven).

## Design Decisions

### 1. **Upsert Logic (Idempotency)**
During data ingestion, I used SQLAlchemy's `session.merge()` instead of simple `insert`. This ensures that if the ingestion process is run multiple times, it updates existing records instead of failing or creating duplicates. This makes the pipeline **idempotent** and resilient to network failures.

### 2. **Type Safety & Validation**
I implemented **Pydantic schemas** in the FastAPI service. This provides:
- Automatic documentation (via Swagger UI at `/docs`).
- Input/output validation (ensuring emails are valid, dates are correctly formatted).
- Clear separation between the Database models and API response models.

## Project Structure
- `mock-server/`: Flask application and mock data.
- `pipeline-service/`: FastAPI application, models, and ingestion logic.
- `docker-compose.yml`: Orchestrates the services.

## Setup and Running

1. Ensure Docker and Docker Compose are installed.
2. Ensure you have a `.env` file in the root with `DATABASE_URL`.
3. Run the following command from the root directory:
   ```bash
   docker-compose up --build
   ```

## API Endpoints

### Flask Mock Server (Port 5000)
- `GET /api/health`: Check health status.
- `GET /api/customers?page=1&limit=10`: Get paginated mock customers.

### FastAPI Pipeline Service (Port 8000)
- `POST /api/ingest`: Trigger data ingestion from the mock server to the database.
- `GET /api/customers?page=1&limit=10`: Get paginated customers from the database.
- `GET /api/customers/{id}`: Get a specific customer from the database.

## Architecture
1. **Ingestion**: The `pipeline-service` makes HTTP requests to the `mock-server`.
2. **Storage**: Data is processed and stored in `PostgreSQL` using SQLAlchemy.
3. **Upsert Logic**: The ingestion process uses `merge` to avoid duplicate records based on `customer_id`.
