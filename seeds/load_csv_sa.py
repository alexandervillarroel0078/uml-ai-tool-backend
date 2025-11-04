# seeds/loaders/__init__.py
# # SELECT * FROM "user";
# # SELECT * FROM diagram;
# # SELECT * FROM clase;
# # SELECT * FROM atributo;
# # SELECT * FROM metodo;
# # SELECT * FROM relacion;
# # SELECT * FROM alembic_version;



# # DO $$ DECLARE
# #     r RECORD;
# # BEGIN
# #     -- Desactivar temporalmente restricciones
# #     EXECUTE 'SET session_replication_role = replica';

# #     -- Eliminar todas las tablas del esquema público
# #     FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
# #         EXECUTE 'DROP TABLE IF EXISTS public.' || quote_ident(r.tablename) || ' CASCADE';
# #     END LOOP;

# #     -- Restaurar las restricciones
# #     EXECUTE 'SET session_replication_role = origin';
# # END $$;from app.db import SessionLocal
from seeds.loaders import (
    users_loader, diagrams_loader, clases_loader,
    atributos_loader, metodos_loader, relaciones_loader
)

DATA_DIR = "seeds/data"

def main():
    db = SessionLocal()
    try:
        # print("== Cargando users.csv =="); users_loader.load_users(db, DATA_DIR); db.commit()
        print("== Cargando diagrams.csv =="); diagrams_loader.load_diagrams(db, DATA_DIR); db.commit()
        # print("== Cargando clases.csv =="); clases_loader.load_clases(db, DATA_DIR); db.commit()
        # print("== Cargando atributos.csv =="); atributos_loader.load_atributos(db, DATA_DIR); db.commit()
        # print("== Cargando metodos.csv =="); metodos_loader.load_metodos(db, DATA_DIR); db.commit()
        # print("== Cargando relaciones.csv =="); relaciones_loader.load_relaciones(db, DATA_DIR); db.commit()
        print("✅ Seeds completados.")
    except Exception as e:
        db.rollback()
        print("💥 Error en carga:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()


# python -m seeds.loaders.users_loader
# python -m seeds.loaders.diagrams_loader
# python -m seeds.loaders.clases_loader
# python -m seeds.loaders.atributos_loader
# python -m seeds.loaders.relaciones_loader
