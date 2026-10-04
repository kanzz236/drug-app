from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class ActiveIngredient(Base):
    __tablename__ = "active_ingredients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    medicines = relationship("Medicine", back_populates="active_ingredient")


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    sdk_code = Column(String, nullable=True)
    strength = Column(String, nullable=True)
    dosage_form = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)
    indication = Column(Text, nullable=True)
    contraindication = Column(Text, nullable=True)
    side_effect = Column(Text, nullable=True)
    warning = Column(Text, nullable=True)
    
    active_ingredient_id = Column(Integer, ForeignKey("active_ingredients.id"), nullable=True)

    active_ingredient = relationship("ActiveIngredient", back_populates="medicines")
    symptoms = relationship("Symptom", secondary="medicine_symptoms", back_populates="medicines")


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)

    medicines = relationship("Medicine", secondary="medicine_symptoms", back_populates="symptoms")


class MedicineSymptom(Base):
    __tablename__ = "medicine_symptoms"

    medicine_id = Column(Integer, ForeignKey("medicines.id"), primary_key=True)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), primary_key=True)