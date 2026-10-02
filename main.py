from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Data Mahasiswa",
    description="API sederhana untuk mengelola data mahasiswa (CRUD: GET, POST, PUT, DELETE)",
    version="1.0.0",
)


# Model data mahasiswa (nama, alamat, ipk, semester, hobi)
class Mahasiswa(BaseModel):
    nama: Optional[str] = Field(None, example="Budi Santoso")
    alamat: Optional[str] = Field(None, example="Semarang")
    ipk: Optional[float] = Field(None, ge=0, le=4, example=3.75)
    semester: Optional[int] = Field(None, ge=1, le=14, example=5)
    hobi: Optional[str] = Field(None, example="Membaca")


# Simulasi database (in-memory)
mahasiswa_db: dict[int, dict] = {}


def dump(m: Mahasiswa, **kw) -> dict:
    # Kompatibel dengan Pydantic v1 dan v2
    return m.model_dump(**kw) if hasattr(m, "model_dump") else m.dict(**kw)


@app.get("/")
def read_root():
    return {"message": "API Data Mahasiswa berhasil dijalankan"}


# CREATE (POST)
@app.post("/mahasiswa/{mahasiswa_id}", status_code=201)
async def create_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):
    if mahasiswa_id in mahasiswa_db:
        raise HTTPException(status_code=400, detail="Data mahasiswa sudah ada")
    mahasiswa_db[mahasiswa_id] = dump(mahasiswa)
    return {
        "message": "Data mahasiswa berhasil dibuat",
        "mahasiswa_id": mahasiswa_id,
        "data": mahasiswa_db[mahasiswa_id],
    }


# READ ALL (GET)
@app.get("/mahasiswa")
async def read_all_mahasiswa():
    return {"data": mahasiswa_db}


# READ BY ID (GET)
@app.get("/mahasiswa/{mahasiswa_id}")
async def read_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
    return {"mahasiswa_id": mahasiswa_id, "data": mahasiswa_db[mahasiswa_id]}


# UPDATE (PUT) - hanya field yang diisi yang diperbarui
@app.put("/mahasiswa/{mahasiswa_id}")
async def update_mahasiswa(mahasiswa_id: int, mahasiswa: Mahasiswa):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
    mahasiswa_db[mahasiswa_id].update(dump(mahasiswa, exclude_unset=True))
    return {
        "message": "Data mahasiswa berhasil diperbarui",
        "mahasiswa_id": mahasiswa_id,
        "data": mahasiswa_db[mahasiswa_id],
    }


# DELETE
@app.delete("/mahasiswa/{mahasiswa_id}")
async def delete_mahasiswa(mahasiswa_id: int):
    if mahasiswa_id not in mahasiswa_db:
        raise HTTPException(status_code=404, detail="Data mahasiswa tidak ditemukan")
    deleted = mahasiswa_db.pop(mahasiswa_id)
    return {
        "message": "Data mahasiswa berhasil dihapus",
        "mahasiswa_id": mahasiswa_id,
        "data": deleted,
    }
