# lib/car.py
from . import CURSOR, CONN
from .owner import Owner


class Car:
    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, make, model, year, owner_id, id=None):
        self.id = id
        self.make = make
        self.model = model
        self.year = year
        self.owner_id = owner_id

    def __repr__(self):
        return (
            f"<Car {self.id}: {self.year} {self.make} {self.model}, "
            f"Owner ID: {self.owner_id}>"
        )

    @property
    def make(self):
        return self._make
    
    @make.setter
    def make(self, value):
        if isinstance(value, str) and len(value):
            self._make
        else:
            raise ValueError(
                "Make must be a non-empty string"
            )

    

    # --- DDL ---
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Car instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY,
                make TEXT,
                model TEXT,
                year INTEGER,
                owner_id INTEGER,
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Car instances"""
        sql = "DROP TABLE IF EXISTS cars;"
        CURSOR.execute(sql)
        CONN.commit()

    # --- CRUD (instance) ---
    def save(self):
        """
        Insert a new row with the attributes of the current Car instance.
        Update object id using the primary key of the new row.
        Save the object in the local dictionary using PK as the key.
        """
        sql = """
            INSERT INTO cars (make, model, year, owner_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.make, self.model, self.year, self.owner_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        """Update the table row corresponding to the current Car instance"""
        sql = """
            UPDATE cars
            SET make = ?, model = ?, year = ?, owner_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.make, self.model, self.year, self.owner_id, self.id))
        CONN.commit()

    def delete(self):
        """
        Delete the table row corresponding to the current Car instance,
        delete the dictionary entry, and reassign id attribute.
        """
        sql = "DELETE FROM cars WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    # --- CRUD (class) ---
    @classmethod
    def create(cls, make, model, year, owner_id):
        """Initialize a new Car instance and save it to the database"""
        car = cls(make, model, year, owner_id)
        car.save()
        return car

    @classmethod
    def instance_from_db(cls, row):
        """
        Return a Car object having the attribute values from the table row.
        Keeps a single in-memory instance per DB row (identity map).
        """
        car = cls.all.get(row[0])
        if car:
            car.make = row[1]
            car.model = row[2]
            car.year = row[3]
            car.owner_id = row[4]
        else:
            car = cls(row[1], row[2], row[3], row[4], id=row[0])
            cls.all[car.id] = car
        return car

    @classmethod
    def get_all(cls):
        """Return a list containing one Car object per table row"""
        sql = "SELECT * FROM cars"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return Car object matching the specified primary key"""
        sql = "SELECT * FROM cars WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_model(cls, model):
        """Return first Car object matching the specified model"""
        sql = "SELECT * FROM cars WHERE model = ?"
        row = CURSOR.execute(sql, (model,)).fetchone()
        return cls.instance_from_db(row) if row else None