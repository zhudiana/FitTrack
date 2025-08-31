from fastapi import APIRouter, HTTPException, Path, status
from pydantic import BaseModel, Field
from app.db.models import MeasurementLog
from app.dependencies import db_dependency, user_dependency

router = APIRouter(
    prefix='/measurement',
    tags=['measurement']
)

class MeasurementRequest(BaseModel):
    weight_kg: float = Field(gt=0)
    chest_cm: float = Field(gt=0)
    waist_cm: float = Field(gt=0)
    arm_cm: float = Field(gt=0)
    thigh_cm: float = Field(gt=0)

@router.get("/read_all_measurements", status_code=status.HTTP_200_OK)
async def read_all_measurements(db: db_dependency):
    return db.query(MeasurementLog).all()

@router.get("/{measurement_id}", status_code=status.HTTP_200_OK)
async def get_measurements(db: db_dependency, measurement_id: float = Path(gt=0)):
    measurement_model = db.query(MeasurementLog).filter(MeasurementLog.id == measurement_id).first()

    if measurement_model is not None:
        return measurement_model
    raise HTTPException(status_code=404, detail="Measurement not found")


@router.post("/create_measurement", status_code=status.HTTP_201_CREATED)
async def create_measurement(user: user_dependency, db: db_dependency, measurement_request: MeasurementRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    measurement_model = MeasurementLog(**measurement_request.model_dump(), owner_id=user.get("id"))
    
    db.add(measurement_model)
    db.commit()

@router.put("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_measurement(db: db_dependency, measurement_request: MeasurementRequest, measurement_id: int = Path(gt=0)):
    measurement_model = db.query(MeasurementLog).filter(MeasurementLog.id == measurement_id).first()

    if measurement_model is None:
        raise HTTPException(status_code=404, detail="Measurement not found")

    measurement_model.weight_kg = measurement_request.weight_kg
    measurement_model.chest_cm = measurement_request.chest_cm
    measurement_model.waist_cm = measurement_request.waist_cm
    measurement_model.arm_cm = measurement_request.arm_cm
    measurement_model.thigh_cm = measurement_request.thigh_cm

    db.add(measurement_model)
    db.commit()

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(db: db_dependency, measurement_id: int = Path(gt=0)):
    measurement_model = db.query(MeasurementLog).filter(MeasurementLog.id == measurement_id).first()

    if measurement_model is None:
        raise HTTPException(status_code=404, detail="Measurement not found")

    db.query(MeasurementLog).filter(MeasurementLog.id == measurement_id).delete()
    db.commit()