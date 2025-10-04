from . import CONN, CURSOR


class Owner:
    """Owner model: one Owner -> many Cars."""

    def __init__(self, name: str, id=None):
        self._id = id  # read-only outside ORM
        self.name = name  # route through setter for validation

    # --- Getters/Setters ---
    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("name must be a non-empty string")
        self._name = value.strip()

    @property
    def cars(self):
        """Read-only: all cars that belong to this owner (lazy DB query)."""
        if self._id is None:
            return []
        from .car import Car  # local import to avoid circular
        CURSOR.execute(
            "SELECT id, make, model, year, owner_id FROM cars WHERE owner_id = ?;",
            (self._id,),
        )
        rows = CURSOR.fetchall()
        return [Car(id=r[0], make=r[1], model=r[2], year=r[3], owner_id=r[4]) for r in rows]

    # --- Table ---
    @classmethod
    def create_table(cls):
        CURSOR.execute(
            "CREATE TABLE IF NOT EXISTS owners (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);"
        )
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS owners;")
        CONN.commit()

    # --- CRUD ---
    def save(self):
        if self._id is None:
            CURSOR.execute("INSERT INTO owners (name) VALUES (?);", (self._name,))
            CONN.commit()
            self._id = CURSOR.lastrowid
        else:
            CURSOR.execute("UPDATE owners SET name = ? WHERE id = ?;", (self._name, self._id))
            CONN.commit()
        return self

    def delete(self):
        if self._id is not None:
            CURSOR.execute("DELETE FROM owners WHERE id = ?;", (self._id,))
            CONN.commit()
            self._id = None

    @classmethod
    def all(cls):
        CURSOR.execute("SELECT id, name FROM owners ORDER BY name;")  # sorted for stable CLI display
        return [cls(id=row[0], name=row[1]) for row in CURSOR.fetchall()]

    @classmethod
    def find_by_id(cls, id_):
        CURSOR.execute("SELECT id, name FROM owners WHERE id = ?;", (id_,))
        row = CURSOR.fetchone()
        return cls(id=row[0], name=row[1]) if row else None

    def __repr__(self):
        return f"<Owner id={self._id} name={self._name}>"
    