# MusicSpace

# Imports
#Imports relevant modules to be used

from tkinter import *
import time
from guizero import *
import sys
import os
from pygame import mixer
import requests, json

app_icons = os.path.abspath('app_icons')
song_album_art = os.path.abspath('song_album_art')
song_mp3_files = os.path.abspath('song_mp3_files')
song_lyrics_files = os.path.abspath('song_lyrics_files')

mixer.init()

# Functions

# search for tracks function searches through an array of songs imported from
# the songs database and finds the track (or tracks) searched for

def search_for_tracks():
    music_list.clear()
    search_for_tracks = []
    song_search_parameter = ""
    song_search_parameter = search_bar1.value
    if search_bar1.value == "":
        error("Error", "Please enter a valid artist, song name, album, genre or mood")
    else:
        for x in range(len(program_songs)):
            if song_search_parameter.lower() == (program_songs[x][0]).lower() or song_search_parameter.lower() == (program_songs[x][1]).lower() or song_search_parameter.lower() == (program_songs[x][2]).lower() or song_search_parameter.lower() == (program_songs[x][3]).lower() or song_search_parameter.lower() == (program_songs[x][4]).lower():
                search_for_tracks.append("{0} - {1} - {2} - {3}".format(*program_songs[x]))
        for y in search_for_tracks:
            music_list.append(y)

# search liked songs function searches through the array of songs imported from that user's liked songs table in the database and returns the specific tracks that the user searched for

def search_liked_songs():
    liked_songs_database = []
    search_for_tracks = []
    song_search_parameter = ""
    song_search_parameter = search_bar3.value
    if search_bar3.value == "":
        error("Error", "Please enter a valid artist, song name, album, genre or mood")
    else:
        music_list3.clear()
        for i in cursor.execute("SELECT * FROM '{}'".format("liked_songs-" + user_signed_in[2])):
            liked_songs_database.append(i)
        for x in range(len(liked_songs_database)):
            if song_search_parameter.lower() == (liked_songs_database[x][0]).lower() or song_search_parameter.lower() == (liked_songs_database[x][1]).lower() or song_search_parameter.lower() == (liked_songs_database[x][2]).lower() or song_search_parameter.lower() == (liked_songs_database[x][3]).lower() or song_search_parameter.lower() == (liked_songs_database[x][4]).lower():
                search_for_tracks.append("{0} - {1} - {2} - {3}".format(*liked_songs_database[x]))
        for y in search_for_tracks:
            music_list3.append(y)
        
# adds recommended songs (songs from the same artist, album, genre or mood) to
# the recommended songs page based on the song that was previously played by
# by searching through an array of songs imported from the songs database and
# finding matching songs.

def add_recommended_songs():
    if sign_in_successful == True:
        check_in_recommended_songs_database = []
        recommended_songs_database = []
        recommended_songs = []
        recommended_songs.clear()
        recommended_songs_database.clear()
        check_in_recommended_songs_database.clear()
        selected_song = []

        if music_list.value in recommended_songs:
            pass
        else:
            recommended_songs.append(music_list.value)
            for x in range(len(app_songs)):
                if app_songs[x] == recommended_songs[0]:
                    selected_song.append(program_songs[x])              
            for v in program_songs:
                if selected_song[0][0] == [v][0][0] and selected_song[0][1] != [v][0][1] and v not in recommended_songs or selected_song[0][2] == [v][0][2] and selected_song[0][1] != [v][0][1] and v not in recommended_songs:
                    recommended_songs.append("{0} - {1} - {2} - {3}".format(*v))
            for t in range(len(recommended_songs)):
                for r in range(len(app_songs)):
                    if recommended_songs[t] == app_songs[r]:
                        recommended_songs_database.append(program_songs[r])                    
            for i in cursor.execute("SELECT * FROM '{}'".format("recommended_songs-" + user_signed_in[2])):
                check_in_recommended_songs_database.append(i)
            for s in range(len(recommended_songs_database)):
                if recommended_songs_database[s] not in check_in_recommended_songs_database:
                    cursor.execute("INSERT INTO '{}' (Artist, Song_name, Album, Genre, Mood) VALUES (?,?,?,?,?)".format("recommended_songs-" + user_signed_in[2]), recommended_songs_database[s])                    
            connection.commit()            

# adds the song the user has selected in the search page to the liked songs page

def add_to_liked_songs():
    if sign_in_successful == True:
        if search.visible == True:
            liked_song = []
            liked_song.clear()
            liked_song_buffer = []
            liked_song_buffer.clear()
            liked_songs_database = []
            liked_songs_database.clear()
            
            liked_song.append(music_list.value)
            for x in range(len(app_songs)):
                if app_songs[x] == liked_song[0]:
                    liked_song_buffer.append(program_songs[x])
            for i in cursor.execute("SELECT * FROM '{}'".format("liked_songs-" + user_signed_in[2])):
                liked_songs_database.append(i)
            if liked_song_buffer[0] not in liked_songs_database:
                cursor.execute("INSERT INTO '{}' (Artist, Song_name, Album, Genre, Mood) VALUES (?,?,?,?,?)".format("liked_songs-" + user_signed_in[2]), liked_song_buffer[0])
                info("Added", "Song has successfully been added to Liked songs")
            else:
                error("Error", "Song has already been added to Liked songs")
            connection.commit()
    else:
        info("Please sign in", text="Please sign in to your account to access this feature.")

    if recommended.visible == True:
        liked_song = []
        liked_song.clear()
        liked_song_buffer = []
        liked_song_buffer.clear()
        liked_songs_database = []
        liked_songs_database.clear()
            
        liked_song.append(music_list2.value)
        for x in range(len(app_songs)):
            if app_songs[x] == liked_song[0]:
                liked_song_buffer.append(program_songs[x])
        for i in cursor.execute("SELECT * FROM '{}'".format("liked_songs-" + user_signed_in[2])):
            liked_songs_database.append(i)
        if liked_song_buffer[0] not in liked_songs_database:
            cursor.execute("INSERT INTO '{}' (Artist, Song_name, Album, Genre, Mood) VALUES (?,?,?,?,?)".format("liked_songs-" + user_signed_in[2]), liked_song_buffer[0])
            info("Added", "Song has successfully been added to Liked songs")
        else:
            error("Error", "Song has already been added to Liked songs")
        connection.commit()
        
# removes the song the user has selected from the liked songs page

def remove_from_liked_songs():
    liked_songs_database = []
    for i in range(len(app_songs)):
        if app_songs[i] == music_list3.value :
            liked_song = [program_songs[i]]
            music_list3.remove(music_list3.value)
    for c in cursor.execute("SELECT * FROM '{}'".format("liked_songs-" + user_signed_in[2])):
        liked_songs_database.append(c)
    for x in range(len(liked_songs_database)):
        if liked_songs_database[x] == liked_song[0]:
            cursor.execute("DELETE FROM '{}' WHERE Song_name = ?".format("liked_songs-" + user_signed_in[2]),(liked_song[0][1],))
            info("Removed", "Song has successfully been removed from Liked songs")
    connection.commit()   

# searches through an array of songs imported from the songs database and adds
# ones that match the parameter the user has entered in some way into the
# listbox (similar to the search_songs function)

def create_custom_playlists():
    music_list1.clear()
    song_search_results_text1.text = "Search results: "
    search_for_tracks = []
    global save_playlist_tracks
    save_playlist_tracks = []
    song_search_parameter = ""
    if search_bar2.value == "":
        error("Error", "Please enter a key word")
    else:
        song_search_parameter = search_bar2.value
    for x in range(len(program_songs)):
        if song_search_parameter.lower() == (program_songs[x][0]).lower() or song_search_parameter.lower() == (program_songs[x][1]).lower() or song_search_parameter.lower() == (program_songs[x][2]).lower() or song_search_parameter.lower() == (program_songs[x][3]).lower() or song_search_parameter.lower() == (program_songs[x][4]).lower():
            save_playlist_tracks.append(program_songs[x])
            search_for_tracks.append("{0} - {1} - {2} - {3}".format(*program_songs[x]))
    for y in search_for_tracks:
        music_list1.append(y)

# pulls the temperature data for the location the user is in and displays
# songs that match the current weather in the listbox once the "Try me!" button
# is clicked. For example, if the temperature is above 15 C (warm) it will
# display songs with the mood "Happy" whereas if the temperature is below 15 C
# (cold) it will display songs that have the mood "Sad."

def create_playlist_based_on_current_weather():
    if enter_location.value == "":
        error("Error", "Please enter a location")
    else:
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        CITY = enter_location.value
        API_KEY = "8e728e551d764c43966e73a2d8c907ae"
        URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
        response = requests.get(URL)

        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
  
        current_temp_celsius = round(temperature - 273.15)
        current_weather = ""

        if current_temp_celsius > 15:
            current_weather = "Warm"
        elif current_temp_celsius < 15:
            current_weather = "Cold"

        mood = ""
        if current_weather == "Warm":
            mood = "Happy"
        elif current_weather == "Cold":
            mood = "Sad"

        song_search_results_text1.value = "The current weather in " + enter_location.value + " is " + str(current_temp_celsius) + "°C (" + current_weather + ") " + "so we recommend:" 
        music_list1.clear()

        search_for_tracks = []
        global save_playlist_tracks
        save_playlist_tracks = []
        for x in range(len(program_songs)):
            if mood == program_songs[x][4]:
                save_playlist_tracks.append(program_songs[x])
                search_for_tracks.append("{0} - {1} - {2} - {3}".format(*program_songs[x]))
        for y in search_for_tracks:
            music_list1.append(y)
    
# saves songs in the created playlist listbox into the database as a new table
# and stores the name of the database in the saved_playlist_names table to be
# imported and displayed in the saved playlists page 

def save_custom_playlist():
    if sign_in_successful == True:
        if enter_playlist_name.value == "":
            error("Error", "Please enter a playlist name")
        else:
            table_name = enter_playlist_name.value
            saved_playlist_names = []
            for x in cursor.execute("SELECT * FROM '{}'".format("saved_playlist_names-" + user_signed_in[2])):
                saved_playlist_names.append("{0}".format(*x))
            if table_name not in saved_playlist_names:
                cursor.execute("CREATE TABLE '{}' (Artist VARCHAR(255), Song_name VARCHAR(255), Album VARCHAR(255), Genre VARCHAR(255), Mood VARCHAR(255))".format(table_name + "-" + user_signed_in[2]))
                for i in range(len(save_playlist_tracks)):
                    cursor.execute("INSERT INTO '{}' (Artist, Song_name, Album, Genre, Mood) VALUES (?,?,?,?,?)".format(table_name + "-" + user_signed_in[2]), save_playlist_tracks[i])
                playlist_name = [enter_playlist_name.value]
                cursor.execute("INSERT INTO '{}' (Playlist_name) VALUES (?)".format("saved_playlist_names-" + user_signed_in[2]), (playlist_name[0],)) 
                connection.commit()
                info("Playlist created", "Playlist has successfully been created")  
            else:
                error("Error", "A playlist with this name already exists, please enter a different name")
    else:
        info("Please sign in", text="Please sign in to your account to access this feature.")

# deletes the playlist that the user has selected in the selected playlist page
# listbox

def delete_selected_playlist():
    selected_playlist_name = playlist_list.value
    delete_playlist_warning = saved_playlists.yesno(title="Delete playlist", text="Are you sure you want to delete this playlist?")             
    if delete_playlist_warning == True:
        cursor.execute("DELETE FROM '{}' WHERE Playlist_name = ?".format("saved_playlist_names-" + user_signed_in[2]),(selected_playlist_name,))
        cursor.execute("DROP TABLE '{}'".format(selected_playlist_name + "-" + user_signed_in[2]))
        playlist_list.remove(selected_playlist_name)
        info("Playlist deleted", "Playlist has successfully been deleted")
        connection.commit()

# saves user sign up data into the user_account_information table in the
# database to be searched for matching sign in details when the user tries to
# sign in

def save_user_sign_up_data():
    if first_name_entry.value or last_name_entry.value or email_entry1.value or password_entry1.value == "":
        error("Error", "Please fill in all required fields")
    else:
        cursor.execute("INSERT INTO user_account_information (First_name, Last_name, Email, Password) VALUES (?,?,?,?)", (first_name_entry.value, last_name_entry.value, email_entry1.value, password_entry1.value,))
        cursor.execute("CREATE TABLE '{}' (Artist VARCHAR(255), Song_name VARCHAR(255), Album VARCHAR(255), Genre VARCHAR(255), Mood VARCHAR(255))".format("recommended_songs-" + email_entry1.value,))
        cursor.execute("CREATE TABLE '{}' (Artist VARCHAR(255), Song_name VARCHAR(255), Album VARCHAR(255), Genre VARCHAR(255), Mood VARCHAR(255))".format("liked_songs-" + email_entry1.value))
        cursor.execute("CREATE TABLE '{}' (Playlist_name VARCHAR(255))".format("saved_playlist_names-" + email_entry1.value))
        connection.commit()
        info("Account created", "Account has successfully been created")
        sign_up.hide()
        sign_in.show()

# sign in to account function searches through the user_account_information
# table in the database for the record in the table that matches the email and
# password entered by the user on the sign up page. If the matching record is
# found (the user has entered correct sign in details) the sign in will be
# granted and a corresponding pop up message will be displayed, if not, an error
# message will be displayed stating: "Incorrect sign in information. Try again."  

sign_in_successful = False

def sign_in_to_account():
    global sign_in_successful
    sign_in_successful = False
    user_account_data = []
    global user_signed_in
    for x in cursor.execute("SELECT * FROM user_account_information"):
        user_account_data.append(x)

    for i in range(len(user_account_data)):
        if user_account_data[i][2] == email_entry.value and user_account_data[i][3] == password_entry.value:
            user_signed_in = user_account_data[i]
            sign_in_successful = True
            welcome_back_text.value = "Welcome back " + user_signed_in[0]
            users_liked_songs_text.value = user_signed_in[0] + "'s liked songs:"
            users_saved_playlists_text.value = user_signed_in[0] + "'s saved playlists:"
            user_instruction4.value = user_signed_in[0] + ", we recommend you these songs based on your past search results..."
            sign_in.hide()
            home.show()

    if sign_in_successful == True:
        info("Successful", "Sign in successful")

    elif sign_in_successful == False:
         error("Error", "Incorrect account details entered. Please try again.")

# open lyrics function allows the user to access the lyrics of a song by reading
# from the corresponding text file containing the lyrics and displaying them in
# the listbox

def open_lyrics():
    song_lyrics_listbox.clear()
    song_lyrics.show()
    song_name = ""

    if recommended.visible == True:
        for z in range(len(app_songs)):
            if music_list2.value == app_songs[z]:
                song_name = program_songs[z][1]               
    elif search.visible == True:
        for z in range(len(app_songs)):
            if music_list.value == app_songs[z]:
                song_name = program_songs[z][1]
    elif liked_songs.visible == True:
        for z in range(len(app_songs)):
            if music_list3.value == app_songs[z]:
                song_name = program_songs[z][1]
    elif selected_playlist.visible == True:
        for z in range(len(app_songs)):
            if selected_playlist_song_list.value == app_songs[z]:
                song_name = program_songs[z][1]
    elif create_playlists.visible == True:
        for z in range(len(app_songs)):
            if music_list1.value == app_songs[z]:
                song_name = program_songs[z][1]

    file = open(song_lyrics_files + "/" + song_name + ".txt", "r")
    for x in file:
        song_lyrics_listbox.append(x)
    file.close()
    song_lyrics.title = song_name + " Lyrics"
    song_lyrics_title.value = song_name
        
# play track function plays the selected track by loading its corresponding mp3
# file into the mixer and playing it

global played_tracks
played_tracks = []

def play_track():
    global played_song
    played_song = ""
    global songs_playing_next
    songs_playing_next = []
    
    if recommended.visible == True:
        search_selected_song = ""
        for z in range(len(app_songs)):
            if music_list2.value == app_songs[z]:
                search_selected_song = program_songs[z][0] + " - " + program_songs[z][1] + ".mp3"
                played_song = program_songs[z]
                played_tracks.append(program_songs[z])
        mixer.music.load(song_mp3_files + "/" + search_selected_song)
        mixer.music.play()
        song_title2.value = music_list2.value

        for i in range(len(program_songs)):
            if program_songs[i][0] == played_song[0] or program_songs[i][2] == played_song[2] or program_songs[i][3] == played_song[3] and program_songs[i] not in songs_playing_next:
                songs_playing_next.append(program_songs[i])
                
    elif search.visible == True:
        search_selected_song = ""
        for z in range(len(app_songs)):
            if music_list.value == app_songs[z]:
                search_selected_song = program_songs[z][0] + " - " + program_songs[z][1] + ".mp3"
                played_song = program_songs[z]
                played_tracks.append(program_songs[z])
        mixer.music.load(song_mp3_files + "/" + search_selected_song)
        mixer.music.play()
        song_title.value = music_list.value

        add_recommended_songs()
        for i in range(len(program_songs)):
            if program_songs[i][0] == played_song[0] or program_songs[i][2] == played_song[2] or program_songs[i][3] == played_song[3] and program_songs[i] not in songs_playing_next:
                songs_playing_next.append(program_songs[i])

    elif liked_songs.visible == True:
        search_selected_song = ""
        for z in range(len(app_songs)):
            if music_list3.value == app_songs[z]:
                search_selected_song = program_songs[z][0] + " - " + program_songs[z][1] + ".mp3"
                played_song = program_songs[z]
                played_tracks.append(program_songs[z])
        mixer.music.load(song_mp3_files + "/" + search_selected_song)
        mixer.music.play()
        song_title3.value = music_list3.value

        for i in range(len(program_songs)):
            if program_songs[i][0] == played_song[0] or program_songs[i][2] == played_song[2] or program_songs[i][3] == played_song[3] and program_songs[i] not in songs_playing_next:
                songs_playing_next.append(program_songs[i])
        
    elif create_playlists.visible == True:
        search_selected_song = ""
        for z in range(len(app_songs)):
            if music_list1.value == app_songs[z]:
                search_selected_song = program_songs[z][0] + " - " + program_songs[z][1] + ".mp3"
                played_song = program_songs[z]
                played_tracks.append(program_songs[z])
        mixer.music.load(song_mp3_files + "/" + search_selected_song)
        mixer.music.play()
        song_title1.value = music_list1.value

        for i in range(len(program_songs)):
            if program_songs[i][0] == played_song[0] or program_songs[i][2] == played_song[2] or program_songs[i][3] == played_song[3] and program_songs[i] not in songs_playing_next:
                songs_playing_next.append(program_songs[i])
                
    elif selected_playlist.visible == True:
        search_selected_song = ""
        for z in range(len(app_songs)):
            if selected_playlist_song_list.value == app_songs[z]:
                search_selected_song = program_songs[z][0] + " - " + program_songs[z][1] + ".mp3"
                played_song = program_songs[z]
                played_tracks.append(program_songs[z])
        mixer.music.load(song_mp3_files + "/" + search_selected_song)
        mixer.music.play()
        song_title4.value = selected_playlist_song_list.value

        for i in range(len(program_songs)):
            if program_songs[i][0] == played_song[0] or program_songs[i][2] == played_song[2] or program_songs[i][3] == played_song[3] and program_songs[i] not in songs_playing_next:
                songs_playing_next.append(program_songs[i])
                
# stop track function stops the current track being played in the mixer   

def stop_track():
    mixer.music.stop()

# pause track function pauses the current track being played in the mixer and
# changes the text of the pause button from "pause" (False) to "play" (True) to
# reflect this change

def pause_track():
    if pause_button.text == "Pause":
        mixer.music.pause()
        pause_button.text = "Play"
    else:
        mixer.music.unpause()
        pause_button.text = "Pause"

# next track function plays the next track by playing the song in the next index of the songs_playing_next array whilst removing the index of the current song from the array to avoid it being played repeatedly

def next_track():
    search_next_song = False
    global played_song
    global songs_playing_next
    songs_playing_next.remove(played_song)
  
    while search_next_song == False:
        for i in range(len(songs_playing_next)):
            if search_next_song == False:
                next_song = song_mp3_files + "/" + songs_playing_next[i][0] + " - " + songs_playing_next[i][1] + ".mp3"
                played_song = songs_playing_next[i]
                mixer.music.load(next_song)
                mixer.music.play()
                if recommended.visible == True:
                    song_title2.value = "{0} - {1} - {2} - {3}".format(played_song[0], played_song[1], played_song[2], played_song[3])
                    search_next_song = True
                elif search.visible == True:
                    song_title.value = "{0} - {1} - {2} - {3}".format(played_song[0], played_song[1], played_song[2], played_song[3]) 
                    search_next_song = True
                elif liked_songs.visible == True:
                    song_title3.value = "{0} - {1} - {2} - {3}".format(played_song[0], played_song[1], played_song[2], played_song[3])
                    search_next_song = True
                elif selected_playlist.visible == True:
                    song_title4.value = "{0} - {1} - {2} - {3}".format(played_song[0], played_song[1], played_song[2], played_song[3])
                    search_next_song = True
                elif create_playlists.visible == True:
                    song_title1.value = "{0} - {1} - {2} - {3}".format(played_song[0], played_song[1], played_song[2], played_song[3])
                    search_next_song = True                   
        else:
            break

# prev track function plays the track that was played previously by taking the name of the song in the second to last position (index[-2]) of the array played_tracks containing the names of all songs that have been played since the program was opened

def prev_track():
    prev_song = ""
    for i in range(len(played_tracks)):
        if played_song == played_tracks[i]:
            prev_song = song_mp3_files + "/" + played_tracks[-2][0] + " - " + played_tracks[-2][1] + ".mp3"
            mixer.music.load(prev_song)
            mixer.music.play()
            if recommended.visible == True:
                song_title2.value = played_tracks[-2][0] + " - " + played_tracks[-2][1] + " - " + played_tracks[-2][2] + " - " + played_tracks[-2][3]
            elif search.visible == True:
                song_title.value = played_tracks[-2][0] + " - " + played_tracks[-2][1] + " - " + played_tracks[-2][2] + " - " + played_tracks[-2][3]
            elif liked_songs.visible == True:
                song_title3.value = played_tracks[-2][0] + " - " + played_tracks[-2][1] + " - " + played_tracks[-2][2] + " - " + played_tracks[-2][3]
            elif selected_playlist.visible == True:
                song_title4.value = played_tracks[-2][0] + " - " + played_tracks[-2][1] + " - " + played_tracks[-2][2] + " - " + played_tracks[-2][3]
            elif create_playlists.visible == True:
                song_title1.value = played_tracks[-2][0] + " - " + played_tracks[-2][1] + " - " + played_tracks[-2][2] + " - " + played_tracks[-2][3]

# when the home button is pressed the home_window function opens the home window
# and hides all other windows         

def home_window():
    home.show()
    home.set_full_screen()
    sign_in.hide()
    recommended.hide()
    search.hide()
    liked_songs.hide()
    saved_playlists.hide()
    create_playlists.hide()
    selected_playlist.hide()

# when the sign in button is pressed the sign_in_window function opens the sign
# in window and hides all other windows

def sign_in_window():
    email_entry.clear()
    password_entry.clear()
    sign_in.show()
    sign_in.set_full_screen()
    sign_up.hide()
    home.hide()
    recommended.hide()
    search.hide()
    liked_songs.hide()
    saved_playlists.hide()
    create_playlists.hide()
    selected_playlist.hide()

# when the sign up button is pressed in the sign in window the sign_up_window
# function opens the sign up window and hides all other windows

def sign_up_window():
    first_name_entry.clear()
    last_name_entry.clear()
    email_entry1.clear()
    password_entry1.clear()
    sign_up.show()
    sign_up.set_full_screen()
    sign_in.hide()
    home.hide()
    recommended.hide()
    search.hide()
    liked_songs.hide()
    saved_playlists.hide()
    create_playlists.hide()
    selected_playlist.hide()
    
# when the recommended window button is pressed the recommended_window function
# opens the recommended window and hides all other windows

def recommended_window():
    if sign_in_successful == True:
        home.hide()
        sign_in.hide()
        recommended.show()
        recommended.set_full_screen()
        search.hide()
        liked_songs.hide()
        saved_playlists.hide()
        create_playlists.hide()
        selected_playlist.hide()
        music_list2.clear()
        for i in cursor.execute("SELECT * FROM '{}'".format("recommended_songs-" + user_signed_in[2])):
            music_list2.append("{0} - {1} - {2} - {3}".format(*i))
    else:
        info("Please sign in", text="Please sign in to your account to access this feature.")

# when the search button is pressed the search_window function opens the search
# window and hides all other windows

def search_window():
    home.hide()
    sign_in.hide()
    recommended.hide()
    search.show()
    search.set_full_screen()
    liked_songs.hide()
    saved_playlists.hide()
    create_playlists.hide()
    selected_playlist.hide()

# when the liked songs button is pressed the liked_songs_window function opens
# the liked songs window and hides all other windows

def liked_songs_window():
    if sign_in_successful == True:
        home.hide()
        sign_in.hide()
        recommended.hide()
        search.hide()
        liked_songs.show()
        liked_songs.set_full_screen()
        saved_playlists.hide()
        create_playlists.hide()
        selected_playlist.hide()
        music_list3.clear()
        for i in cursor.execute("SELECT * FROM '{}'".format("liked_songs-" + user_signed_in[2])):
            music_list3.append("{0} - {1} - {2} - {3}".format(*i))
    else:
        info("Please sign in", text="Please sign in to your account to access this feature.")

# when the saved playlists button is pressed the saved_playlists_window function
# opens the saved_playlists window and hides all other windows

def saved_playlists_window():
    if sign_in_successful == True:  
        home.hide()
        sign_in.hide()
        recommended.hide()
        search.hide()
        liked_songs.hide()
        saved_playlists.show()
        saved_playlists.set_full_screen()
        create_playlists.hide()
        selected_playlist.hide()
        playlist_list.clear()
        for x in cursor.execute("SELECT * FROM '{}'".format("saved_playlist_names-" + user_signed_in[2])):
            playlist_list.append("{0}".format(*x))
    else:
        info("Please sign in", text="Please sign in to your account to access this feature.")

# when the create playlists button is pressed the create_playlists_window
# function opens the create playlists window and hides all other windows

def create_playlists_window():
    home.hide()
    sign_in.hide()
    recommended.hide()
    search.hide()
    liked_songs.hide()
    saved_playlists.hide()
    create_playlists.show()
    create_playlists.set_full_screen()
    selected_playlist.hide()

# when a song record is double clicked in a listbox a small window shows up with
# information about that song

def create_song_info_card():
    selected_song_card_info = ""
    card = Window(search, "Song info", width=340, height=300)
    card.bg = "Black"
    picture = Drawing(card, width=300, height=200)

    for i in range(len(app_songs)):
        if music_list.value == app_songs[i]:
            selected_song_card_info = program_songs[i]

    picture.image(50,0, song_album_art + "/" + selected_song_card_info[1] + ".png")
    artist = Text(card, text="Artist: " + selected_song_card_info[0])
    artist.text_color = "white"
    song_name = Text(card, text="Song name: " + selected_song_card_info[1])
    song_name.text_color = "white"
    album = Text(card, text="Album: " + selected_song_card_info[2])
    album.text_color = "white"
    genre = Text(card, text="Genre: " + selected_song_card_info[3])
    genre.text_color = "white"

# when a playlist record is double clicked in the listbox on the saved playlists
# window a window shows up with the playlist and the songs inside it

def selected_playlist_window():
    song_title4.value = ""
    selected_playlist_song_list.clear()
    selected_playlist.show()
    selected_playlist.set_full_screen()
    
    selected_playlist.title = playlist_list.value
    selected_playlist.bg = "Black"
    
    selected_playlist_name_text.value = playlist_list.value

    selected_playlist_in_listbox = playlist_list.value
    for i in cursor.execute("SELECT * FROM '{}'".format(selected_playlist_in_listbox + "-" + user_signed_in[2])):
        selected_playlist_song_list.append("{0} - {1} - {2} - {3}".format(*i))

# if the user confirms they want to quit in the yesno pop up warning the
# quit_program function destroys the app widget, closes the connection with the
# songs database and quits the program

def quit_program():
    quit_program_warning = app.yesno(title="Quit", text="Are you sure you want to quit?") 
    if quit_program_warning == True:
        connection.close()
        app.destroy()
        quit()

# App/Widgets

# Initialising windows

app = App(title="Music recommendation app", layout="grid", width=1920, height=1080)
app.hide()

home = Window(app, title="Home", width=1920, height=1080)
home.show()
home.set_full_screen()

sign_in = Window(app, title="Sign In", width=1920, height=1080)
sign_in.hide()

sign_up = Window(app, title="Sign up", width=1920, height=1080)
sign_up.hide()

recommended = Window(app, title="Recommended", width=1920, height=1080)
recommended.hide()

search = Window(app, title="Search", width=1920, height=1080)
search.hide()

liked_songs = Window(app, title="Liked songs", width=1920, height=1080)
liked_songs.hide()

saved_playlists = Window(app, title="Saved playlists", width=1920, height=1080)
saved_playlists.hide()

create_playlists = Window(app, title="Create playlists", width=1920, height=1080)
create_playlists.hide()

selected_playlist = Window(app, title="", width=1920, height=1080)
selected_playlist.hide()

song_lyrics = Window(app, title="", width=700, height=500)
song_lyrics.hide()

# Home window

home.bg = "black"
box = Box(home, layout="grid", border=5)

box1 = Box(home, layout="grid", align="left")
sign_in_button = PushButton(box1, grid=[0,2], text="Sign In", width=10, height=1, command=sign_in_window)
sign_in_button.text_color = "white"
space = Text(box1, grid=[0,3])
home_button = PushButton(box1, text="Home", grid=[0,4], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,5])
recommended_button = PushButton(box1, text="Recommended", grid=[0,6], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,7])
search_button = PushButton(box1, text="Search", grid=[0,8], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,9])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,10], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,11])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,12], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,13])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,14], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(home, layout="grid")
title = Text(box2, text="MusicSpace", grid=[2,2], size=35, align="top", color="White")
space = Text(box2, grid=[1,3])
welcome_back_text = Text(box2, text="Welcome back", grid=[1,4], size=20, color="white", align="left")
space = Text(box2, grid=[1,5])
home_text = Text(box2, text="Home", grid=[1,6], size=20, color="white")
recommended_text = Text(box2, text="Recommended", grid=[2,6], size=20, color="white")
search_text = Text(box2, text="Search", grid=[3,6], size=20, color="white")
space = Text(box2, grid=[1,7])
home_shortcut = PushButton(box2, grid=[1,8], image=app_icons + "/Home.png", command=home_window)
recommended_shortcut = PushButton(box2, grid=[2,8], image=app_icons + "/Recommended songs.png", command=recommended_window)
search_shortcut = PushButton(box2, grid=[3,8], image=app_icons + "/Search.png", command=search_window)
space = Text(box2, grid=[1,9])
liked_songs_text = Text(box2, text="Liked songs", grid=[1,10], size=20, color="white")
saved_playlists_text = Text(box2, text="Saved playlists", grid=[2,10], size=20, color="white")
create_playlists_text = Text(box2, text="Create playlists", grid=[3,10], size=20, color="white")
space = Text(box2, grid=[1,11])
liked_songs_shortcut = PushButton(box2, grid=[1,12], image=app_icons + "/Liked songs.png", command=liked_songs_window)
saved_playlists_shortcut = PushButton(box2, grid=[2,12], image=app_icons + "/Saved playlists.png", command=saved_playlists_window)
create_playlists_shortcut = PushButton(box2, grid=[3,12], image=app_icons + "/Create playlists.png", command=create_playlists_window)
space = Text(box2, grid=[1,13])

box4 = Box(home, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[6,15], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# Sign In window

sign_in.bg = "black"

box = Box(sign_in, layout="grid")
filler_text = Text(box, text="____", size=30, color="black", grid=[1,1], align="right")
title = Text(box, text="Sign In", size=30, color="white", grid=[2,1], align="right")
space = Text(box, grid=[1,2])

box1 = Box(sign_in, layout="grid", align="left")
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(sign_in, layout="grid")
email_entry_text = Text(box2, text="Email: ", grid=[1,3], size=15, color="white")
email_entry = TextBox(box2, grid=[2,3], width=60)
email_entry.bg = "white"
space = Text(box2, grid=[1,4])
password_entry_text = Text(box2, text="Password: ", grid=[1,5], size=15, color="white")
password_entry = TextBox(box2, grid=[2,5], width=60)
password_entry.hide_text = True
password_entry.bg = "white"
space = Text(box2, grid=[1,6])

box3 = Box(sign_in, layout="grid")
sign_in_button = PushButton(box3, text="Sign In", grid=[1,6], width=10, height=1, command=sign_in_to_account)
sign_in_button.text_color = "white"
space = Text(box3, grid=[1,7])
sign_up_instruction = Text(box3, text="Dont have an account? Sign up today.", grid=[1,8], size=15, color="white")
sign_up_button = PushButton(box3, text="Sign up", grid=[1,9], width=10, height=1, command=sign_up_window)
sign_up_button.text_color = "white"

# Sign up window

sign_up.bg = "black"
box3 = Box(sign_up, layout="grid")
filler_text = Text(box3, text="____", size=30, color="black", grid=[1,0], align="right")
title = Text(box3, text="Sign up", size=30, color="white", grid=[2,0], align="right")

box = Box(sign_up, layout="grid", align="left")
sign_in_button = PushButton(box, grid=[0,2], text="Sign In", width=10, height=1, command=sign_in_window)
sign_in_button.text_color = "white"
space = Text(box, grid=[0,3])
home_button = PushButton(box, text="Home", grid=[0,4], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box, grid=[0,5])
recommended_button = PushButton(box, text="Recommended", grid=[0,6], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box, grid=[0,7])
search_button = PushButton(box, text="Search", grid=[0,8], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box, grid=[0,9])
liked_songs_button = PushButton(box, text="Liked songs", grid=[0,10], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box, grid=[0,11])
saved_playlists_button = PushButton(box, text="Saved playlists", grid=[0,12], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box, grid=[0,13])
create_playlist_button = PushButton(box, text="Create playlists", grid=[0,14], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box1 = Box(sign_up, layout="grid")
space = Text(box1, grid=[1,1])
enter_your_details_text = Text(box1, text="  Enter your details below:", size=15, grid=[2,2], align="left", color="white")
space = Text(box1, grid=[1,3])
first_name_entry_text = Text(box1, text="First name: ", grid=[1,4], size=15, color="white")
first_name_entry = TextBox(box1, grid=[2,4], width=60)
first_name_entry.bg = "white"
space = Text(box1, grid=[1,5])
last_name_entry = Text(box1, text="Last name: ", grid=[1,6], size=15, color="white")
last_name_entry = TextBox(box1, grid=[2,6], width=60)
last_name_entry.bg = "white"
space = Text(box1, grid=[1,7])
email_entry1_text = Text(box1, text="Email: ", grid=[1,8], size=15, color="white")
email_entry1 = TextBox(box1, grid=[2,8], width=60)
email_entry1.bg = "white"
space = Text(box1, grid=[1,9])
password_entry1_text = Text(box1, text="Password: ", grid=[1,10], size=15, color="white")
password_entry1 = TextBox(box1, grid=[2,10], width=60)
password_entry1.bg = "white"
space = Text(box1, grid=[1,11])

box2 = Box(sign_up, layout="grid")
create_account_button = PushButton(box2, text="Create account", grid=[2,12], width=10, height=1, command=save_user_sign_up_data)
create_account_button.text_color = "white"

# Recommended window

recommended.bg = "black"

box1 = Box(recommended, layout="grid", align="left")
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(recommended, layout="grid")
title = Text(box2, text="Recommended", grid=[1,2], size=30, color="White")
space = Text(box2, grid=[1,3])
user_instruction4 = Text(box2, text="", grid=[1,4], size=17, color="white", align="left")
user_instruction4.text_color = "white"
space = Text(box2, grid=[1,5])
music_list2 = ListBox(box2, items="", grid=[1,6], width=900, height=450, scrollbar=True)
music_list2.text_color = "white"
song_title2 = Text(box2, text="", grid=[1,7], size=18, color="white")
space = Text(box2, grid=[1,8])
add_to_liked_songs_button = PushButton(box2, grid=[1,9], width=13, height=2, text="Add to liked songs", command=add_to_liked_songs)
add_to_liked_songs_button.text_color = "white"
open_lyrics_button = PushButton(box2, grid=[1,9], width=12, height=2, align="right", text="Open lyrics", command=open_lyrics)
open_lyrics_button.text_color = "white"

box3 = Box(recommended, layout="grid", align="bottom")
prev_button = PushButton(box3, text="Prev", grid=[1,3], image=app_icons + "/prev_img.png", width=50, height=50, command=prev_track)
stop_button = PushButton(box3, text="Stop", grid=[2,3], image=app_icons + "/stop_img.png", width=50, height=50, command=stop_track)
play_button = PushButton(box3, text="Play", grid=[3,3], image=app_icons + "/play_img.png", width=50, height=50, command=play_track)
pause_button = PushButton(box3, text="Pause", grid=[4,3], image=app_icons + "/pause_img.png", width=50, height=50, command=pause_track)
next_button = PushButton(box3, text="Next", grid=[5,3], image=app_icons + "/next_img.png", width=50, height=50, command=next_track)

box4 = Box(recommended, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[6,3], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# Search window

search.bg = "black"

box1 = Box(search, layout="grid", align="left")
sign_in_button = PushButton(box1, grid=[0,2], text="Sign In", width=10, height=1, command=sign_in_window)
sign_in_button.text_color = "white"
space = Text(box1, grid=[0,3])
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(search, layout="grid")
title = Text(box2, text="Search", grid=[1,2], size=30, color="White")
space = Text(box2, grid=[1,3])
user_instruction = Text(box2, text="Search for songs, artists, genres and more...", grid=[1,4], size=20, color="white", align="left")
user_instruction.text_color = "white"
space = Text(box2, grid=[1,5])
search_bar1 = TextBox(box2, grid=[1,6], width=60)
search_bar1.bg = "white"
space = Text(box2, grid=[1,7])
song_search_button = PushButton(box2, grid=[1,8], width=10, height=1, text="Search", command=search_for_tracks)
song_search_button.text_color = "white"
space = Text(box2, grid=[1,9])
song_search_results_text = Text(box2, text="Search results: ", grid=[1,10], size=20, color="white", align="left")
music_list = ListBox(box2, items="", grid=[1,11], width=900, height=350, scrollbar=True)
music_list.text_color = "white"
song_title = Text(box2, text="", grid=[1,12], size=18, color="white")
space = Text(box2, grid=[1,13])
add_to_liked_songs_button = PushButton(box2, grid=[1,14], width=13, height=2, text="Add to liked songs", command=add_to_liked_songs)
add_to_liked_songs_button.text_color = "white"
open_lyrics_button = PushButton(box2, grid=[1,14], width=12, height=2, align="right", text="Open lyrics", command=open_lyrics)
open_lyrics_button.text_color = "white"

box3 = Box(search, layout="grid", align="bottom")
prev_button = PushButton(box3, text="Prev", grid=[1,3], image=app_icons + "/prev_img.png", width=50, height=50, command=prev_track)
stop_button = PushButton(box3, text="Stop", grid=[2,3], image=app_icons + "/stop_img.png", width=50, height=50, command=stop_track)
play_button = PushButton(box3, text="Play", grid=[3,3], image=app_icons + "/play_img.png", width=50, height=50, command=play_track)
pause_button = PushButton(box3, text="Pause", grid=[4,3], image=app_icons + "/pause_img.png", width=50, height=50, command=pause_track)
next_button = PushButton(box3, text="Next", grid=[5,3], image=app_icons + "/next_img.png", width=50, height=50, command=next_track)

box4 = Box(search, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[6,3], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# Liked songs window

liked_songs.bg = "black"

box1 = Box(liked_songs, layout="grid", align="left")
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(liked_songs, layout="grid")
title = Text(box2, text="Liked songs", grid=[1,2], size=30, color="White")
space = Text(box2, grid=[1,3])
search_liked_songs_text = Text(box2, text="Search for tracks in liked songs...", grid=[1,4], size=20, color="White", align="left")
space = Text(box2, grid=[1,5])
search_bar3 = TextBox(box2, grid=[1,6], width=60)
search_bar3.bg = "white"
space = Text(box2, grid=[1,7])
song_search_button = PushButton(box2, grid=[1,8], width=10, height=1, text="Search", command=search_liked_songs)
song_search_button.text_color = "white"
space = Text(box2, grid=[1,9])
users_liked_songs_text = Text(box2, text="", grid=[1,10], size=20, color="White", align="left")
space = Text(box2, grid=[1,11])
music_list3 = ListBox(box2, items="", grid=[1,12], width=900, height=400, scrollbar=True)
music_list3.text_color = "white"
song_title3 = Text(box2, text="", grid=[1,13], size=18, color="white")
space = Text(box2, grid=[1,14])
remove_from_liked_songs_button = PushButton(box2, grid=[1,15], width=17, height=2, text="Remove from liked songs", command=remove_from_liked_songs)
remove_from_liked_songs_button.text_color = "white"
open_lyrics_button = PushButton(box2, grid=[1,15], width=12, height=2, align="right", text="Open lyrics", command=open_lyrics)
open_lyrics_button.text_color = "white"

box3 = Box(liked_songs, layout="grid", align="bottom")
prev_button = PushButton(box3, text="Prev", grid=[1,3], image=app_icons + "/prev_img.png", width=50, height=50, command=prev_track)
stop_button = PushButton(box3, text="Stop", grid=[2,3], image=app_icons + "/stop_img.png", width=50, height=50, command=stop_track)
play_button = PushButton(box3, text="Play", grid=[3,3], image=app_icons + "/play_img.png", width=50, height=50, command=play_track)
pause_button = PushButton(box3, text="Pause", grid=[4,3], image=app_icons + "/pause_img.png", width=50, height=50, command=pause_track)
next_button = PushButton(box3, text="Next", grid=[5,3], image=app_icons + "/next_img.png", width=50, height=50, command=next_track)

box4 = Box(liked_songs, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[6,3], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# Saved playlists window

saved_playlists.bg = "black"

box1 = Box(saved_playlists, layout="grid", align="left")
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(saved_playlists, layout="grid")
title = Text(box2, text="Saved playlists", grid=[1,2], size=30, color="White")
space = Text(box2, grid=[1,3])
users_saved_playlists_text = Text(box2, text="", grid=[1,4], size=20, color="White", align="left")
space = Text(box2, grid=[1,5])
playlist_list = ListBox(box2, items="", grid=[1,6], width=900, height=450, scrollbar=True)
playlist_list.text_color = "white"
space = Text(box2, grid=[1,7])
delete_playlist_button = PushButton(box2, grid=[1,8], width=11, height=2, text="Delete playlist", command=delete_selected_playlist)
delete_playlist_button.text_color = "white"

box4 = Box(saved_playlists, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[6,3], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# Create playlists window

create_playlists.bg = "black"

box1 = Box(create_playlists, layout="grid", align="left")
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1, command=home_window)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"

box2 = Box(create_playlists, layout="grid")
title = Text(box2, text="Create custom playlists", grid=[1,2], size=30, color="White")
space = Text(box2, grid=[1,3])
user_instruction = Text(box2, text="Enter key words such as: Happy, Rap...", grid=[1,4], size=20, color="white", align="left")
user_instruction.text_color = "white"
user_instruction2 = Text(box2, text="Create playlist based on", grid=[1,4], size=20, color="white", align="right")
user_instruction2.text_color = "white"
user_instruction3 = Text(box2, text="current weather:", grid=[1,5], size=20, color="white", align="right")
user_instruction3.text_color = "white"
space = Text(box2, grid=[1,6])
search_bar2 = TextBox(box2, grid=[1,7], width=60, align="left")
search_bar2.bg = "white"
enter_location_text = Text(box2, text="Enter your city, town, borough", grid=[1,7], size=20, color="white", align="right")
enter_location_text = Text(box2, text="or state...", grid=[1,8], size=20, color="white", align="right")
space = Text(box2, grid=[1,9])
enter_location = TextBox(box2, grid=[1,10], width=60, align="right")
enter_location.bg = "white"
space = Text(box2, grid=[1,11])
enter_playlist_name_text = Text(box2, text="Enter playlist name: ", grid=[1,12], size=20, color="white")
enter_playlist_name = TextBox(box2, grid=[1,13], width=60)
enter_playlist_name.bg = "white"
create_playlist_button = PushButton(box2, grid=[1,13], width=10, height=1, text="Create playlist", align="left", command=create_custom_playlists)
create_playlist_button.text_color = "White"
try_me_button = PushButton(box2, grid=[1,13], width=10, height=1, text="Try me!", align="right", command=create_playlist_based_on_current_weather)
try_me_button.text_color = "white"
space = Text(box2, grid=[1,14])
song_search_results_text1 = Text(box2, text="Search results: ", grid=[1,15], size=20, color="white", align="left")
music_list1 = ListBox(box2, items="", grid=[1,16], width=900, height=250, scrollbar=True)
music_list1.text_color = "white"
song_title1 = Text(box2, text="", grid=[1,17], size=18, color="white")
space = Text(box2, grid=[1,18])
save_playlist_button = PushButton(box2, grid=[1,19], width=13, height=2, text="Save custom playlist", command=save_custom_playlist)
save_playlist_button.text_color = "white"
open_lyrics_button = PushButton(box2, grid=[1,19], width=12, height=2, align="right", text="Open lyrics", command=open_lyrics)
open_lyrics_button.text_color = "white"

box3 = Box(create_playlists, layout="grid", align="bottom")
prev_button = PushButton(box3, text="Prev", grid=[1,3], image=app_icons + "/prev_img.png", width=50, height=50, command=prev_track)
stop_button = PushButton(box3, text="Stop", grid=[2,3], image=app_icons + "/stop_img.png", width=50, height=50, command=stop_track)
play_button = PushButton(box3, text="Play", grid=[3,3], image=app_icons + "/play_img.png", width=50, height=50, command=play_track)
pause_button = PushButton(box3, text="Pause", grid=[4,3], image=app_icons + "/pause_img.png", width=50, height=50, command=pause_track)
next_button = PushButton(box3, text="Next", grid=[5,3], image=app_icons + "/next_img.png", width=50, height=50, command=next_track)

box4 = Box(create_playlists, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[6,2], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# selected playlist window
    
selected_playlist.title = playlist_list.value
selected_playlist.bg = "Black"

box1 = Box(selected_playlist, layout="grid", align="left")
home_button = PushButton(box1, text="Home", grid=[0,2], width=10, height=1)
home_button.text_color = "white"
space = Text(box1, grid=[0,3])
recommended_button = PushButton(box1, text="Recommended", grid=[0,4], width=10, height=1, command=recommended_window)
recommended_button.text_color = "white"
space = Text(box1, grid=[0,5])
search_button = PushButton(box1, text="Search", grid=[0,6], width=10, height=1, command=search_window)
search_button.text_color = "white"
space = Text(box1, grid=[0,7])
liked_songs_button = PushButton(box1, text="Liked songs", grid=[0,8], width=10, height=1, command=liked_songs_window)
liked_songs_button.text_color = "white"
space = Text(box1, grid=[0,9])
saved_playlists_button = PushButton(box1, text="Saved playlists", grid=[0,10], width=10, height=1, command=saved_playlists_window)
saved_playlists_button.text_color = "white"
space = Text(box1, grid=[0,11])
create_playlist_button = PushButton(box1, text="Create playlists", grid=[0,12], width=10, height=1, command=create_playlists_window)
create_playlist_button.text_color = "white"
    
box2 = Box(selected_playlist, layout="grid")
selected_playlist_name_text = Text(box2, text=playlist_list.value, grid=[1,2], size=30)
space = Text(box2, grid=[1,3])
selected_playlist_name_text.text_color = "white"
selected_playlist_song_list = ListBox(box2, items="", grid=[1,4], width=900, height=450, scrollbar=True)
selected_playlist_song_list.text_color = "white"
song_title4 = Text(box2, text="", grid=[1,5], size=18, color="white")
space = Text(box2, grid=[1,6])
open_lyrics_button = PushButton(box2, grid=[1,6], width=12, height=2, text="Open lyrics", command=open_lyrics)
open_lyrics_button.text_color = "white"

box3 = Box(selected_playlist, layout="grid", align="bottom")
prev_button = PushButton(box3, text="Prev", grid=[1,3], image=app_icons + "/prev_img.png", width=50, height=50, command=prev_track)
stop_button = PushButton(box3, text="Stop", grid=[2,3], image=app_icons + "/stop_img.png", width=50, height=50, command=stop_track)
play_button = PushButton(box3, text="Play", grid=[3,3], image=app_icons + "/play_img.png", width=50, height=50, command=play_track)
pause_button = PushButton(box3, text="Pause", grid=[4,3], image=app_icons + "/pause_img.png", width=50, height=50, command=pause_track)
next_button = PushButton(box3, text="Next", grid=[5,3], image=app_icons + "/next_img.png", width=50, height=50, command=next_track)

box4 = Box(selected_playlist, layout="grid", align="right")
quit_button = PushButton(box4, text="Quit", grid=[2,3], width=10, height=2, command=quit_program) 
quit_button.text_color = "white"

# Song lyrics window

song_lyrics.bg = "black"

box = Box(song_lyrics, layout="grid")
song_lyrics_title = Text(box, text="", grid=[0,0], size=30, color="White")
song_lyrics_listbox = ListBox(box, items="", grid=[0,1], width=700, height=450, scrollbar=True)
song_lyrics_listbox.text_color = "white"

global app_songs
global program_songs
program_songs = []
app_songs = []

# Establishes connection with database, imports songs from database and stores
# them in an array called "program_songs." Then it linear searches through this
# array to store it in a particular format in another array called "app_songs"
# so that it can be displayed to the user in a listbox.

import sqlite3
connection = sqlite3.connect("program_database.db")
cursor = connection.cursor()

for x in cursor.execute("SELECT * FROM songs_table ORDER BY Artist"):
    program_songs.append(x)

for i in program_songs:
    app_songs.append("{0} - {1} - {2} - {3}".format(*i))

# Displays a song info card for the song selected when double clicked

music_list.when_double_clicked = create_song_info_card

# Opens a window for the selected playlist and shows the songs inside it
# in a listbox allowing them to be played if desired

playlist_list.when_double_clicked = selected_playlist_window

app.display()
