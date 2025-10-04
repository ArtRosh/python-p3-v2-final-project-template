from typing import Optional
from . import CONN, CURSOR


class Car:
    """Car model: many Cars belong to one Owner."""

    def __init__(self, make: str, model: str, year: int, owner_id: int, id: Optional[int] = None):
        self._id = id  # read-only outside of ORM
        self.make = make
        self.model = model
        self.year = year
        self.owner_id = owner_id

    # --- Getters/Setters ---
    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def make(self) -> str:
        return self._make
    @make.setter
    def make(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("make must be a non-empty string")
        self._make = v.strip()

    @property
    def model(self) -> str:
        return self._model
    @model.setter
    def model(self, v: str) -> None:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("model must be a non-empty string")
        self._model = v.strip()

    @property
    def year(self) -> int:
        return self._year
    @year.setter
    def year(self, v: int) -> None:
        if not isinstance(v, int):
            raise ValueError("year must be an integer")
        if v < 1886 or v > 2100:
            raise ValueError("year must be between 1886 and 2100")
        self._year = v

    @property
    def owner_id(self) -> int:
        return self._owner_id
    @owner_id.setter
    def owner_id(self, v: int) -> None:
        if not isinstance(v, int) or v <= 0:
            raise ValueError("owner_id must be a positive integer")
        self._owner_id = v

    # --- Table ---
    @classmethod
    def create_table(cls) -> None:
        CURSOR.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                owner_id INTEGER NOT NULL,
                FOREIGN KEY (owner_id) REFERENCES owners(id) ON DELETE CASCADE
            );
            """
        )
        CONN.commit()

    @classmethod
    def drop_table(cls) -> None:
        CURSOR.execute("DROP TABLE IF EXISTS cars;")
        CONN.commit()

    # --- CRUD ---
    def save(self) -> "Car":
        if self._id is None:
            CURSOR.execute(
                "INSERT INTO cars (make, model, year, owner_id) VALUES (?, ?, ?, ?);",
                (self._make, self._model, self._year, self._owner_id),
            )
            CONN.commit()
            self._id = CURSOR.lastrowid
        else:
            CURSOR.execute(
                "UPDATE cars SET make = ?, model = ?, year = ?, owner_id = ? WHERE id = ?;",
                (self._make, self._model, self._year, self._owner_id, self._id),
            )
            CONN.commit()
        return self

    def delete(self) -> None:
        if self._id is not None:
            CURSOR.execute("DELETE FROM cars WHERE id = ?;", (self._id,))
            CONN.commit()
            self._id = None

    @classmethod
    def all(cls) -> list["Car"]:
        CURSOR.execute("SELECT id, make, model, year, owner_id FROM cars;")
        return [cls(id=r[0], make=r[1], model=r[2], year=r[3], owner_id=r[4]) for r in CURSOR.fetchall()]

    @classmethod
    def find_by_id(cls, id_: int) -> Optional["Car"]:
        CURSOR.execute("SELECT id, make, model, year, owner_id FROM cars WHERE id = ?;", (id_,))
        row = CURSOR.fetchone()
        return cls(id=row[0], make=row[1], model=row[2], year=row[3], owner_id=row[4]) if row else None

    def __repr__(self) -> str:
        return f"<Car id={self._id} {self._year} {self._make} {self._model} owner_id={self._owner_id}>"
    