from enum import StrEnum


class SerializerType(StrEnum):
    SIMPLE = "simple"
    DETAILED = "detailed"
    CREATE = "create"
    UPDATE = "update"

    @property
    def class_name(self) -> str:
        return f"{self.lower()}_serializer_class"
