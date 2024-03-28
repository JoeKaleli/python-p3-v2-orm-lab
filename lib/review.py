from __init__ import CURSOR, CONN

class Review:
    instance_cache = {}  # Dictionary to store instances for caching

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return f"<Review {self.id}: {self.year}, {self.summary}, Employee: {self.employee_id}>"

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Persist the Review object to the "reviews" table and store it in a local dictionary."""
        # SQL INSERT statement
        sql = """
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """
        # Execute SQL INSERT statement
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        # Commit the transaction
        CONN.commit()

        # Retrieve the primary key (id) of the newly inserted row
        self.id = CURSOR.lastrowid

        # Store the Review object in a local dictionary
        Review.instance_cache[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        new_review = cls(year, summary, employee_id)
        # Save the new Review instance to the "reviews" table using the save() method
        new_review.save()
        # Return the new Review instance
        return new_review

    
    @classmethod
    def instance_from_db(cls, row):
     """Return a Review instance having the attribute values from the table row."""
     # Extract row data
     review_id, year, summary, employee_id = row  # Unpack the tuple directly
 
     # Check if the instance is already cached
     if review_id in cls.instance_cache:
         return cls.instance_cache[review_id]
 
     # Create a new Review instance from the row data
     new_review = cls(year, summary, employee_id, review_id)

     # Add the new instance to the dictionary cache
     cls.instance_cache[review_id] = new_review

     # Return the new instance
     return new_review


    @classmethod
    def find_by_id(cls, id):
        """Find and return a Review instance by its id."""
        # SQL query to select a row with the given id
        sql = """
            SELECT * FROM reviews WHERE id = ?
        """
        # Execute the query and fetch the row
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()

        # If row is not found, return None
        if row is None:
            return None

        # Return an Review instance from the row data
        return cls.instance_from_db(row)

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        # SQL query to update the row based on the id of the current object
        sql = """
            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """
        # Execute the query with the updated values
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Review instance."""
        # SQL query to delete the row based on the id of the current object
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """
        # Execute the query with the id of the current object
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # Remove the instance from the dictionary cache
        del Review.instance_cache[self.id]

        # Reset the id attribute to None
        self.id = None

    @classmethod 
    def get_all(cls):
     """Return a list containing one Review instance per table row."""
     # SQL query to select all rows from the 'reviews' table
     sql = """
         SELECT * FROM reviews
     """
     # Execute the query
     CURSOR.execute(sql)
     # Fetch all rows from the result set
     rows = CURSOR.fetchall()
     # Create a list to store Review instances
     reviews = []
     # Iterate over the rows and create Review instances
     for row in rows:
         # Extract data from the row
         id, year, summary, employee_id = row
         # Create a Review instance from the row data and append it to the list
         review = cls(id=id, year=year, summary=summary, employee_id=employee_id)
         reviews.append(review)
     # Return the list of Review instances
     return reviews
 


