# lib/owner.py
from . import CURSOR, CONN


class Owner:
    """Owner model: one Owner -> many Cars."""

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Owner {self.id}: {self.name}>"
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError(
                "Name must be a non-empty string"
            )

    # --- Table ---
    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Owner instances"""
        sql = """
            CREATE TABLE IF NOT EXISTS owners (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Owner instances"""
        sql = """
            DROP TABLE IF EXISTS owners;
        """
        CURSOR.execute(sql)
        CONN.commit()

    # --- CRUD ---
    def save(self):
        """
        Insert a new row with the current Owner instance values.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key.
        """
        if self.id:
            # Already in DB; perform update to keep row in sync
            self.update()
            return

        sql = """
            INSERT INTO owners (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        """Initialize a new Owner instance and save the object to the database"""
        owner = cls(name)
        owner.save()
        return owner

    def update(self):
        """Update the table row corresponding to the current Owner instance."""
        sql = """
            UPDATE owners
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.id))
        CONN.commit()

    def delete(self):
        """
        Delete the table row corresponding to the current Owner instance,
        delete the dictionary entry, and reassign id attribute.
        """
        sql = """
            DELETE FROM owners
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Delete from local identity map and reset id
        del type(self).all[self.id]
        self.id = None

    # --- Identity Map hydration ---
    @classmethod
    def instance_from_db(cls, row):
        """Return an Owner object having the attribute values from the table row."""
        owner = cls.all.get(row[0])
        if owner:
            # ensure attributes match row values in case local instance was modified
            owner.name = row[1]
        else:
            owner = cls(row[1], id=row[0])
            cls.all[owner.id] = owner
        return owner

    # --- Query helpers ---
    @classmethod
    def get_all(cls):
        """Return a list containing an Owner object per row in the table"""
        sql = "SELECT * FROM owners"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Return an Owner object corresponding to the row matching the specified primary key"""
        sql = "SELECT * FROM owners WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        """Return an Owner object corresponding to first row matching specified name"""
        sql = "SELECT * FROM owners WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # --- Relations ---
    def cars(self):
        """Return list of cars associated with current owner"""
        from .car import Car
        sql = """
            SELECT * FROM cars
            WHERE owner_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Car.instance_from_db(row) for row in rows]
    