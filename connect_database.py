import mysql.connector
from password import password


class ConnectDatabase:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 3306
        self._user = "root"
        self._password = password
        self._database = "db_students_2"
        self.con = None
        self.cursor = None

    def connect_db(self):
        self.con = mysql.connector.connect(
            host=self._host,
            port=self._port,
            database=self._database,
            user=self._user,
            password=self._password
        )

        #Create a cursor for executing SQL queries
        self.cursor = self.con.cursor(dictionary=True)

    def add_info(self, student_id, first_name, last_name, state, city, email_address):
        #Connect to the database
        self.connect_db()

        #Construct SQL query for adding information
        sql = f"""
            INSERT INTO student_info (studentId, firstName, lastName, state, city, emailAddress)
            VALUES ('{student_id}', '{first_name}','{last_name}','{state}','{city}','{email_address}');
        """

        try:
            #Execute the SQL query for adding information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            #Rollback the transaction in case of an error
            self.con.rollback()
            return E
        
        finally:
            #Close the database connection
            self.con.close()

    
    def update_info(self, student_id, first_name, last_name, state, city, email_address):
        #Connect to the database
        self.connect_db()

        #Construct the query for updating information
        sql = f"""
            UPDATE student_info
                SET firstName ='{first_name}', lastname='{last_name}', state='{state}', city='{city}',
                emailAddress='{email_address}'
                WHERE studentId={student_id};
        """
        
        try:
            #Execute the SQL query for updating information
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            self.con.rollback()
            return E
        
        finally:
            self.con.close()

    def delete_info(self, studentId):
        self.connect_db()

        sql = f"""
            DELETE FROM student_info WHERE studentId={studentId};
        """

        try:
            self.cursor.execute(sql)
            self.con.commit()

        except Exception as E:
            self.con.rollback()
            return E
        
        finally:
            self.con.close()

    def search_info(self, student_id=None, first_name=None, last_name=None, state=None, city=None, email_address=None):
        self.connect_db()

        condition = ""
        if student_id:
            condition += f"studentId LIKE '%{student_id}%'"
        else:
            if first_name:
                if condition:
                    condition += f" and firstName LIKE '%{first_name}%'"
                else:
                    condition += f"firstName LIKE '%{first_name}'"

            if last_name:
                if condition:
                    condition += f" and lastName LIKE '%{last_name}%'"
                else:
                    condition += f"lastName LIKE '%{last_name}'"

            if state:
                if condition:
                    condition += f" and state LIKE '%{state}%'"
                else:
                    condition += f"state LIKE '%{state}'"

            if city:
                if condition:
                    condition += f" and city LIKE '%{city}%'"
                else:
                    condition += f"city LIKE '%{city}'"

            if email_address:
                if condition:
                    condition += f" and emailAddress LIKE '%{email_address}%'"
                else:
                    condition += f"emailAddress LIKE '%{email_address}'"

        if condition:
            #Construct SQL query for searching information with conditions
            sql = f"""
                SELECT * FROM student_info WHERE {condition};
            """
        else:
            #Construct SQL query for searching all information
            sql = f"""
                SELECT * FROM student_info;
            """

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        
        except Exception as E:
            return E
        
        finally:
            self.con.close()

    def get_all_states(self):
        self.connect_db()

        sql = f"""
            SELECT state FROM student_info" GROUP BY state;
        """

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        
        except Exception as E:
            self.con.rollback()
            return E
        
        finally:
            self.con.close()

    def get_all_cities(self):
        self.connect_db()

        sql = f"""
            SELECT state FROM student_info" GROUP BY city;
        """

        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        
        except Exception as E:
            self.con.rollback()
            return E
        
        finally:
            self.con.close()