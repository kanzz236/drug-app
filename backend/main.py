from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from api import drug, ocr, symptom

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Drug Prescription & AI Recognition API",
    version="2.0",
    description="Backend modular structure cho ứng dụng nhận diện và tra cứu đơn thuốc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drug.router)
app.include_router(ocr.router)
app.include_router(symptom.router)

@app.get("/")
def root():
    return {"message": "Hệ thống backend đã sẵn sàng hoạt động ngon nghẻ!"}