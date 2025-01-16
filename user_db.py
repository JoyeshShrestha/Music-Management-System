# Establish a database connection

from flask import url_for, redirect, flash

from db import get_db_connection

from user import User

from pymysql.cursors import DictCursor


class User_db():


    def create_table(self):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Raw SQL to create a table
            create_table_query =  """
            CREATE TABLE IF NOT EXISTS user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(500) NOT NULL,
                phone VARCHAR(20),
                dob DATETIME,
                gender ENUM('m', 'f', 'o') DEFAULT 'o',
                address VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("Table 'User' created successfully!")
            cursor.close()
            connection.close()
        except Exception as e:
            print( f"An error occurred: {e}")
    
        




    def check_email_exists(self,email):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use a parameterized query to prevent SQL injection
            check_email_query = "SELECT * FROM user WHERE email = %s"
            cursor.execute(check_email_query, (email,))

            # Fetch the first matching user
            user_tuple = cursor.fetchone()

            cursor.close()
            connection.close()

            if user_tuple:
                return User.from_tuple(user_tuple)
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def update_data_user(self,id,first_name,last_name,date_of_birth,gender,email,password,phone,address):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            update_user_query = """
                                    UPDATE user
                                    SET first_name = %s,
                                        last_name = %s,
                                        email = %s,
                                        password = %s,
                                        phone = %s,
                                        dob = %s,
                                        gender = %s,
                                        address = %s
                                    WHERE id = %s;
                                    """


            # Execute the query with parameters
            cursor.execute(update_user_query, (first_name, last_name, email, password, phone, date_of_birth, gender, address, id))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Flash success message and redirect to login
            flash("User edited successfully!")
            return redirect(url_for("get_all_users"))


        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_users"))



    def insert_data_user(self,first_name, last_name, date_of_birth, gender, email, password, phone, address):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            insert_table_query = """
            INSERT INTO user (first_name, last_name, email, password, phone, dob, gender, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Execute the query with parameters
            cursor.execute(insert_table_query, (first_name, last_name, email, password, phone, date_of_birth, gender, address))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Flash success message and redirect to login
            flash("User inserted successfully!")
            return True

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return False
                    


    def get_data_users(self,page,per_page):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor(DictCursor)
            cursors = connection.cursor()

            offset = (page - 1) * per_page
            query = "SELECT * FROM user LIMIT %s OFFSET %s"
            
            # Execute query with the limit and offset
            cursor.execute(query, (per_page, offset))
            users = cursor.fetchall()

            # Count total users
            total_query = "SELECT COUNT(*) FROM user"
            cursors.execute(total_query)
            total_users =  cursors.fetchone()[0]


            # Close the cursor and connection
            cursor.close()
            connection.close()

        
            return users, total_users


        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("register"))
                    


    def delete_user_query(self,user_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            delete_table_query = """
            DELETE FROM user where id = %s ;
            """

            # Execute the query with parameters
            cursor.execute(delete_table_query, (user_id,))


            # Commit the transaction
            connection.commit()

            

            # Close the cursor and connection
            cursor.close()
            connection.close()

        
            return True

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_users"))

    def get_user_data(self,user_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor(DictCursor)

            # Use parameterized queries to prevent SQL injection
            select_table_query = """
            SELECT * FROM user WHERE id = %s ;
            """

            # Execute the query with parameters
            cursor.execute(select_table_query,user_id)

            # Commit the transaction
            connection.commit()
            user_tuple = cursor.fetchone()

            

            # Close the cursor and connection
            cursor.close()
            connection.close()

        
            return user_tuple

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_users"))