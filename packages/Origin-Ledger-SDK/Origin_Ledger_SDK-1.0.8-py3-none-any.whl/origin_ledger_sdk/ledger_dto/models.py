
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List
from marshmallow_dataclass import class_schema

from .enums import MeasurementType, GGOAction


@dataclass
class Measurement():
    amount: int = field()
    type: MeasurementType = field()
    begin: datetime = field()
    end: datetime = field()
    sector: str = field()
    address: Optional[str] = field(default=None)

    class Meta:
        ordered = True

    @staticmethod
    def get_schema():
        return class_schema(Measurement)(exclude=["address"])

@dataclass
class GGONext():
    action: GGOAction = field()
    addresses: List[str] = field()
    
    class Meta:
        ordered = True
    

@dataclass
class GGO():
    origin: str = field()
    amount: int = field()
    begin: datetime = field()
    end: datetime = field()
    sector: str = field()
    tech_type: str = field()
    fuel_type: str = field()
    next: Optional[GGONext] = field(default=None)
    address: Optional[str] = field(default=None)
    
    class Meta:
        ordered = True

    @staticmethod
    def get_schema():
        return class_schema(GGO)(exclude=["address"])

@dataclass
class SettlementPart:
    ggo: str = field()
    amount: int = field()
    
    class Meta:
        ordered = True

@dataclass
class Settlement:
    measurement: str = field()
    parts : List[SettlementPart] = field()
    address: Optional[str] = field(default=None)
    
    class Meta:
        ordered = True

    @staticmethod
    def get_schema():
        return class_schema(Settlement)(exclude=["address"])
