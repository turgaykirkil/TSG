from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="TSG OCR Service",
    description="Ticaret Sicil Gazetesi için OCR servisi",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """
    Ana endpoint. Servisin çalıştığını doğrulamak için kullanılır.
    """
    return {
        "message": "TSG OCR Servisi çalışıyor.",
        "status": "active",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Geliştirme sunucusunu başlat
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
