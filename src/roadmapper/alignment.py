from dataclasses import asdict, astuple, dataclass
from enum import Enum, EnumMeta
from typing import Optional, Tuple, Union

StrOrAlignment = Union[str, "Alignment"]


class CaseInsensitiveEnumMeta(EnumMeta):
    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.upper()
        return super().__getitem__(key)


class AlignmentDirection(Enum, metaclass=CaseInsensitiveEnumMeta):
    CENTER = 1
    CENTRE = 1
    LEFT = 2
    RIGHT = 3


class OffsetType(Enum, metaclass=CaseInsensitiveEnumMeta):
    UNIT = 1
    PERCENT = 2


@dataclass(kw_only=True)
class Alignment:
    direction: AlignmentDirection = (AlignmentDirection.CENTER,)
    offset_type: Optional[OffsetType] = None
    offset: Optional[Union[int, float]] = None

    @classmethod
    def from_value(
        cls,
        alignment: Optional[StrOrAlignment],
        default_offset_type: Optional[OffsetType] = None,
        default_offset: Optional[float] = None,
    ) -> "Alignment":
        if alignment is None:
            return cls(offset_type=default_offset_type, offset=default_offset)
        if isinstance(alignment, Alignment):
            return cls.from_alignment(alignment)
        if isinstance(alignment, str):
            return cls.from_string(alignment)
        else:
            raise ValueError(
                'Invalid argument "alignment": expected None, str, or Alignment instance,'
                f" got {type(alignment).__name__}."
            )

    @classmethod
    def from_alignment(cls, alignment: "Alignment") -> "Alignment":
        kwargs = asdict(alignment)
        new = cls(**kwargs)
        return new

    @classmethod
    def from_string(cls, alignment: str) -> "Alignment":
        new = cls()
        new.update_from_alignment_string(alignment)
        return new

    @staticmethod
    def parse_offset(offset: str) -> Tuple[Union[int, float], OffsetType]:
        if offset.endswith("%"):
            return (float(offset[:-1]) / 100, OffsetType.PERCENT)
        else:
            return (int(offset), OffsetType.UNIT)

    def update_from_alignment_string(self, alignment: str) -> None:
        parts = alignment.split(":")

        try:
            self.direction = AlignmentDirection[parts[0]]
        except KeyError as e:
            raise ValueError(
                f'Invalid alignment direction "{parts[0]}".'
                f" Valid alignment directions are {[d.name for d in AlignmentDirection]}"
            ) from e

        if len(parts) == 2:
            self.offset, self.offset_type = self.parse_offset(parts[1])

    def as_tuple(
        self,
    ) -> Tuple[AlignmentDirection, Optional[OffsetType], Optional[Union[int, float]]]:
        return astuple(self)

    def percent_of(self, whole: Union[int, float]) -> float:
        if self.offset_type != OffsetType.PERCENT:
            raise ValueError("Cannot return percent_of when offset_type != 'PERCENT'")
        return whole * self.offset

    def __str__(self):
        offset_str = ""
        if self.offset is not None:
            offset_str = ":"
            offset_str += (
                f"{self.offset * 100}%"
                if self.offset_type == OffsetType.PERCENT
                else str(self.offset)
            )
        return f"{self.direction.name.lower()}{offset_str}"


if __name__ == "__main__":
    result1 = Alignment.from_value("left:50%")
    print(result1)

    result2 = Alignment.from_value(result1)
    print(result2.as_tuple())

    result3 = Alignment.from_value("Center")
    print(result3)

    # expect ValueError about type of argument.
    Alignment.from_value(1)

    # Expect ValueError about alignment direction.
    Alignment.from_value("widdershins:50")
