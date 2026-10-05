from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class FieldContract:
    name: str
    semantic_type: str
    data_type: str
    nullable: bool = True
    unit: str | None = None
    description: str | None = None

@dataclass
class DataContract:
    name: str
    version: str
    fields: list[FieldContract]
    primary_key: list[str]
    time_fields: list[str]
    entity_fields: list[str]
    measure_fields: list[str]
    dimension_fields: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "fields": [asdict(f) for f in self.fields],
            "primary_key": self.primary_key,
            "time_fields": self.time_fields,
            "entity_fields": self.entity_fields,
            "measure_fields": self.measure_fields,
            "dimension_fields": self.dimension_fields,
        }
