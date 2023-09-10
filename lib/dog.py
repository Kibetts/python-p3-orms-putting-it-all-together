import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self,name, breed):
        self.name = name
        self.breed = breed
        self.id = None
        
    def save(self):
        CURSOR.execute(
            'INSERT INTO dogs (name, breed) VALUES ("joey","cocker spaniel")',
            (self.name, self.breed)
        )
        self.id = CURSOR.lastrowid 
        CONN.commit()

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        CONN.commit() 

    @classmethod
    def drop_table(cls):
        CURSOR.execute ('DROP TABLE IF EXISTS dogs')
        CONN.commit()


    def save(self):
        CURSOR.execute(
            'INSERT INTO dogs (name, breed) VALUES (?, ?)',
            (self.name, self.breed)
        )
        self.id = CURSOR.lastrowid 
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog
    
    @classmethod
    def new_from_db(cls, db_data):
        dog_id, name, breed = db_data
        new_dog = cls(name, breed)
        new_dog.id = dog_id
        return new_dog
    
    @classmethod
    def get_all(cls):
        CURSOR.execute("SELECT * FROM dogs")
        db_data = CURSOR.fetchall()
        dogs = [cls.new_from_db(data) for data in db_data]
        return dogs
    
    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,))
        db_data = CURSOR.fetchone()
        if db_data:
            return cls.new_from_db(db_data)
        return None
    
    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,))
        db_data = CURSOR.fetchone()
        if db_data:
            return cls.new_from_db(db_data)
        return None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name_and_breed(name, breed)
        if existing_dog:
            return existing_dog
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog
    
    @classmethod
    def find_by_name_and_breed(cls, name, breed):
        CURSOR.execute('SELECT * FROM dogs WHERE name = ? AND breed = ?', (name, breed))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None
    
    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])  
        dog.id = row[0] 
        return dog
    
    def update(self):
        if self.id:
            CURSOR.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))
            CONN.commit()
        else:
            raise ValueError("Cannot update without an ID")
    