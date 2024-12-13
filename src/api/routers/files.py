from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src.extras.database import get_db
from src.extras.utils import parse_csv, get_existing_ids, validate_rows, validate_row_limit
from src.extras.constants import MODELS

router = APIRouter()


@router.post('/csv', status_code=status.HTTP_201_CREATED)
def upload_csv(db: Session = Depends(get_db)):

    try:
        for model in MODELS:
            if not model['path'].endswith('.csv'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='El archivo a cargar debe ser un CSV')

            data = parse_csv(model['path'])
            new_data = get_existing_ids(data, model['model'], db=db)
            valid_rows = validate_rows(new_data, model['model'])
            valid_rows = validate_row_limit(valid_rows)
            db.bulk_insert_mappings(model['model'], valid_rows)
            db.commit()

        return {"response": "Carga exitosa"}
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hubo un error en la carga de los archivos CSV a la base de datos: {e}"
        )
