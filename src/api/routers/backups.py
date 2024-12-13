from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.extras.database import get_db
from src.extras.utils import get_existing_ids, validate_rows
from src.extras.constants import MODELS, BACKUP_DIR
from src.extras.backup import backup_table_to_avro, restore_table_from_avro

router = APIRouter()


@router.post('/backups', status_code=status.HTTP_201_CREATED)
def upload_csv(db: Session = Depends(get_db)) -> dict[str, str]:

    try:
        for model in MODELS:
            backup_table_to_avro(model['model'], BACKUP_DIR, db=db)

        return {"response": "Backup creado con exito"}
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hubo un error en la creacion del backup: {e}"
        )


@router.post("/restore", status_code=status.HTTP_201_CREATED)
def restore_from_avro(db: Session = Depends(get_db)) -> dict[str, str]:
    # Insertar los registros en la tabla
    for model in MODELS:
        records: list[dict] = restore_table_from_avro(
            model['model'], model['backup_path'])
        try:

            # data = [record for record in records]
            deleted_records: list[dict] = get_existing_ids(
                records, model['model'], db=db)
            valid_records: list[dict] = validate_rows(
                deleted_records, model['model'])
            print(valid_records)

            if len(valid_records) == 0 and len(deleted_records) == 0:
                print(
                    f"no hay datos por restaurar en la tabla {model['model'].__table__}")
            else:
                db.bulk_insert_mappings(model['model'], valid_records)
                db.commit()
        except IntegrityError as e:
            print(
                f"Error de integridad al restaurar registro: {valid_records}. Error: {e}")
            db.rollback()  # Evita que el error afecte a otros registros
        print(f"Se restauraron los registros desde {model['backup_path']}.")
    return {'response': 'Base de datos restaurada con exito'}
