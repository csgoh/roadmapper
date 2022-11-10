from dataclasses import dataclass, field


def obj_to_string(obj, extra="    "):
    return (
        str(obj.__class__)
        + "\n"
        + "\n".join(
            (
                extra
                + (
                    str(item)
                    + " = "
                    + (
                        obj_to_string(obj.__dict__[item], extra + "    ")
                        if hasattr(obj.__dict__[item], "__dict__")
                        else str(obj.__dict__[item])
                    )
                )
                for item in sorted(obj.__dict__)
            )
        )
    )


@dataclass
class Door:
    window_type: str = "glass"
    winding_type: str = "spring"


@dataclass(kw_only=True)
class Car:
    engine_type: str
    wheels: int = 4
    doors: field(default_factory=list) = field(default_factory=list)


#x = Car(engine_type="electric", wheels=4, doors=[Door(), Door()])
x = Car(engine_type="electric")
# print(f"{Car.engine_type} {Car.wheels}")
print(f"{x.engine_type} {x.wheels}")
x.doors.append(Door())
print(obj_to_string(x))
