import logging
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models.customer import Customer
from services.ingestion import ingest_data
from schemas import CustomerResponse, PaginatedCustomerResponse

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pipeline-service")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Data Pipeline API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please contact support."}
    )

@app.post("/api/ingest", tags=["Data Operations"])
def trigger_ingest(db: Session = Depends(get_db)):
    logger.info("Starting data ingestion process...")
    try:
        total = ingest_data(db)
        logger.info(f"Ingestion complete. {total} records processed.")
        return {"status": "success", "ingested_records": total}
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to ingest data from mock server")

@app.get("/api/customers", response_model=PaginatedCustomerResponse, tags=["Customer Information"])
def list_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()
    total = db.query(Customer).count()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "customers": customers
    }

@app.get("/api/customers/{id}", response_model=CustomerResponse, tags=["Customer Information"])
def get_customer_by_id(id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == id).first()
    if not customer:
        logger.warning(f"Customer {id} requested but not found.")
        raise HTTPException(status_code=404, detail="Customer record not found")
    return customer

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
