from flask import url_for, redirect, flash

import pymysql
# from main import 
from user import User
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from db import get_db_connection


load_dotenv()


class Artist_db():
    def __init__(self):
        pass


    def get_data_artists(self,page,per_page):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor(DictCursor)
            cursors = connection.cursor()

            offset = (page - 1) * per_page
            query = "SELECT * FROM artist LIMIT %s OFFSET %s"
            
            # Execute query with the limit and offset
            cursor.execute(query, (per_page, offset))
            artists = cursor.fetchall()

            # Count total users
            total_query = "SELECT COUNT(*) FROM artist"
            cursors.execute(total_query)
            total_artists =  cursors.fetchone()[0]


            # Close the cursor and connection
            cursor.close()
            connection.close()

        
            return artists, total_artists


        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("register"))
    

    def check_name_exists(self,name):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use a parameterized query to prevent SQL injection
            check_name_query = "SELECT * FROM artist WHERE name = %s"
            cursor.execute(check_name_query, (name,))

            # Fetch the first matching user
            user_tuple = cursor.fetchone()

            cursor.close()
            connection.close()

            if user_tuple:
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        

    def insert_data_artist(self,name, number_albums,first_release,date_of_birth,gender,address):
            try:
                # Establish database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Use parameterized queries to prevent SQL injection
                insert_table_query = """
                INSERT INTO artist (name, dob, gender, address, first_release_year, no_of_albums_released)
                VALUES (%s, %s, %s, %s, %s, %s);
                """

                # Execute the query with parameters
                cursor.execute(insert_table_query, (name, date_of_birth, gender, address,first_release, number_albums))

                # Commit the transaction
                connection.commit()

                # Close the cursor and connection
                cursor.close()
                connection.close()

                flash("Artist inserted successfully!")
                return True

            except Exception as e:
                # Handle exceptions and flash error message
                flash(f"An error occurred: {e}")
                return redirect(url_for("add_artist"))
                        
    def get_artist_data(self,artist_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor(DictCursor)

            # Use parameterized queries to prevent SQL injection
            select_table_query = """
            SELECT * FROM artist WHERE id = %s ;
            """

            # Execute the query with parameters
            cursor.execute(select_table_query,artist_id)

            # Commit the transaction
            connection.commit()
            artist_tuple = cursor.fetchone()

            

            # Close the cursor and connection
            cursor.close()
            connection.close()

        
            return artist_tuple

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_users"))
        

    def update_data_user(self,artist_id,name,number_albums,first_release,date_of_birth,gender,address):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()
            # Use parameterized queries to prevent SQL injection
            update_artist_query = """
                                        UPDATE artist
                                        SET name = %s,
                                            dob = %s,
                                            gender = %s,
                                            address = %s,
                                            first_release_year = %s,
                                            no_of_albums_released = %s
                                        WHERE id = %s;
                                    """


            # Execute the query with parameters
            cursor.execute(update_artist_query, (name, date_of_birth, gender, address,first_release, number_albums, artist_id))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Flash success message and redirect to login
            flash("Artist edited successfully!")
            return redirect(url_for("get_all_artists"))
        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_artists"))


    def delete_artist_query(self,artist_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            delete_table_query = """
            DELETE FROM artist where id = %s ;
            """

            # Execute the query with parameters
            cursor.execute(delete_table_query, (artist_id,))


            # Commit the transaction
            connection.commit()

            

            # Close the cursor and connection
            cursor.close()
            connection.close()

        
            return True

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_artists"))    