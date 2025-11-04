import os
from passlib.hash import bcrypt
from app.models.user import User
from seeds.utils import norm, bool_from_csv, _csv_open

def load_users(db, data_dir):
    path = os.path.join(data_dir, "users.csv")
    rdr = _csv_open(path)
    if rdr is None: return

    created, updated = 0, 0
    for row in rdr:
        email = norm(row.get("email")).lower()
        name = norm(row.get("name"))
        password = norm(row.get("password")) or "changeme123"
        role = norm(row.get("role")) or "editor"
        active = bool_from_csv(row.get("active"), True)

        if not email:
            print("[users] fila sin email -> skip")
            continue

        user = db.query(User).filter(User.email == email).one_or_none()
        if user:
            changed = False
            if user.name != name and name:
                user.name = name; changed = True
            if user.role != role:
                user.role = role; changed = True
            if user.active != active:
                user.active = active; changed = True
            if password:
                user.password_hash = bcrypt.hash(password); changed = True
            if changed:
                updated += 1; print(f"[users] ↺ actualizado: {email}")
            else:
                print(f"[users] = sin cambios: {email}")
        else:
            db.add(User(email=email, name=name or email.split("@")[0],
                        password_hash=bcrypt.hash(password), role=role, active=active))
            created += 1; print(f"[users] + creado: {email}")
    print(f"[users] creado={created}, actualizado={updated}")
