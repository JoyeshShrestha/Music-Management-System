from flask import url_for, redirect, flash

import pymysql
# from main import 
from user import User
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
from db import get_db_connection


load_dotenv()


class Music_db():
    def __init__(self):
        pass


    def get_data_musics(self, page, per_page, artist_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor(DictCursor)
            cursors = connection.cursor()

            # Calculate offset
            offset = (page - 1) * per_page

            # Corrected query: WHERE comes before LIMIT and OFFSET
            query = "SELECT * FROM music WHERE artist_id = %s LIMIT %s OFFSET %s"
            
            # Execute query with artist_id, limit, and offset
            cursor.execute(query, (artist_id, per_page, offset))
            musics = cursor.fetchall()

            # Query to count total musics for the artist
            total_query = "SELECT COUNT(*) FROM music WHERE artist_id = %s"
            cursors.execute(total_query, (artist_id,))
            total_musics = cursors.fetchone()[0]

            artist_query = "SELECT name FROM artist WHERE id = %s"
            cursors.execute(artist_query, (artist_id,))
            artist = cursors.fetchone()[0]
            print(artist)
            # Close the cursor and connection
            cursor.close()
            cursors.close()
            connection.close()

            return musics, total_musics, artist

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("dashboard"))

    

    def check_music_exists(self,title,artist_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use a parameterized query to prevent SQL injection
            check_name_query = "SELECT * FROM music WHERE title = %s AND artist_id = %s"
            cursor.execute(check_name_query, (title,artist_id))

            # Fetch the first matching user
            music_tuple = cursor.fetchone()

            cursor.close()
            connection.close()

            if music_tuple:
                return True
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        

    def insert_data_music(self,title,album_name,genre,artist_id):
            try:
                # Establish database connection
                connection = get_db_connection()
                cursor = connection.cursor()

                # Use parameterized queries to prevent SQL injection
                insert_table_query = """
                INSERT INTO music (artist_id,title, album_name, genre)
                VALUES (%s, %s, %s, %s);
                """

                # Execute the query with parameters
                cursor.execute(insert_table_query, (artist_id,title,album_name,genre))

                # Commit the transaction
                connection.commit()

                # Close the cursor and connection
                cursor.close()
                connection.close()

                flash("Music inserted successfully!")
                return True

            except Exception as e:
                # Handle exceptions and flash error message
                flash(f"An error occurred: {e}")
                return redirect(url_for("add_music",artist_id=artist_id))
                        
    def get_music_data(self,artist_id,music_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor(DictCursor)

            # Use parameterized queries to prevent SQL injection
            select_table_query = """
            SELECT * FROM music WHERE id = %s AND artist_id = %s ;
            """

            # Execute the query with parameters
            cursor.execute(select_table_query,(music_id,artist_id))

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
            return redirect(url_for("get_all_musics",artist_id=artist_id))
        

    def update_data_music(self,artist_id,music_id,title,album_name,genre):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()
            # Use parameterized queries to prevent SQL injection
            update_artist_query = """
                                        UPDATE music
                                        SET artist_id = %s,
                                            title = %s,
                                            album_name = %s,
                                            genre = %s
                                        WHERE id = %s ;
                                    """


            # Execute the query with parameters
            cursor.execute(update_artist_query, (artist_id,title,album_name,genre,music_id))

            # Commit the transaction
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Flash success message and redirect to login
            flash("Music edited successfully!")
            return redirect(url_for("get_all_musics",artist_id=artist_id))
        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_musics",artist_id=artist_id))


    def delete_music_query(self,artist_id,music_id):
        try:
            # Establish database connection
            connection = get_db_connection()
            cursor = connection.cursor()

            # Use parameterized queries to prevent SQL injection
            delete_table_query = """
            DELETE FROM music where artist_id = %s AND id = %s;
            """

            # Execute the query with parameters
            cursor.execute(delete_table_query, (artist_id,music_id))


            # Commit the transaction
            connection.commit()

            

            # Close the cursor and connection
            cursor.close()
            connection.close()

            flash(f"Deleted Successfully")
        
            return True

        except Exception as e:
            # Handle exceptions and flash error message
            flash(f"An error occurred: {e}")
            return redirect(url_for("get_all_musics",artist_id=artist_id))    