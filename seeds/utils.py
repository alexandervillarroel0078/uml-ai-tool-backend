import os, csv, uuid

def bool_from_csv(v: str | None, default: bool=False) -> bool:
    if v is None:
        return default
    return str(v).strip().lower() in ("true", "1", "yes", "y", "si", "sí")

def norm(s: str) -> str:
    return (s or "").strip()

def gen_uuid(s: str | None) -> uuid.UUID:
    return uuid.UUID(s) if s else uuid.uuid4()

def _csv_open(path: str):
    if not os.path.exists(path):
        print(f"[skip] No existe CSV: {path}")
        return None
    return csv.DictReader(open(path, newline="", encoding="utf-8"))
