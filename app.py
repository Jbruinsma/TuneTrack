import os
from playlistManager import PlaylistManager, Playlist, MusicObject
from music_library import available_music
from form import PlaylistForm, EditingForm
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, current_app, session, g
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['SECRET_KEY'] = 'secret'

DEFAULT_IMAGE = "DefaultPlaylistCover.png"
playlist_manager_storage = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_valid_json_value():

    info_dict = {}

    currently_playing = g.playlistManager.currently_playing.val
    name = currently_playing.music_name
    artist = currently_playing.music_artist
    path = currently_playing.mp3_file
    image = currently_playing.image

    info_dict['music_name'] = name
    info_dict['artist'] = artist
    info_dict['path'] = path
    info_dict['image'] = image

    return info_dict

def add_music_pieces(value):
    piece = available_music[f'{value}']
    piece_name = piece['music_name']
    piece_artist = piece['artist']
    piece_image = piece['image']
    piece_path = piece['path']

    return MusicObject(music_name= piece_name, music_artist= piece_artist, image=  piece_image, mp3_file= piece_path)


def check_session(user_session):
    if user_session:
        return True
    else:
        return False

def provide_error_message():
    return jsonify({'error: "playlistManager" not initialized'}), 400


@app.before_request
def load_playlist_manager():
    session_id = session.get('session_id')
    if session_id and session_id in playlist_manager_storage:
        g.playlistManager = playlist_manager_storage[session_id]
    else:
        g.playlistManager = None

@app.route('/')
def load_content():
    session_id = session.get('session_id')
    if not session_id:
        session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']

    if session_id not in playlist_manager_storage:
        playlist_manager_storage[session_id] = PlaylistManager()

    g.playlistManager = playlist_manager_storage[session_id]

    user_playlists = g.playlistManager.playlists
    return render_template('home.html', title='Home', playlists=user_playlists)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    form = PlaylistForm()

    if check_session(g.playlistManager):

        if form.validate_on_submit():
            chosen_music_pieces = request.form.get("chosen_music_pieces", "")
            selected_music = chosen_music_pieces.split(",") if chosen_music_pieces else []

            playlist_title = form.playlist_name.data

            file = request.files.get('playlist_image')
            if file and allowed_file(file.filename):
                original_filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
            else:
                unique_filename = "DefaultPlaylistCover.png"

            new_playlist = Playlist(image=unique_filename, name=playlist_title)
            new_playlist.music_list.clear()
            for value in selected_music:
                new_playlist.music_order_list.append(value)
                new_playlist.music_list.append(add_music_pieces(value))

            g.playlistManager.playlists.append(new_playlist)

            return redirect(url_for('load_content'))

    else:
        return provide_error_message()

    return render_template('createPlaylist.html', title='Create Playlist', form=form, available_music=available_music)

@app.route('/edit_playlist/<int:playlist_id>', methods=['GET', 'POST'])
def edit_playlist(playlist_id):

    def create_available_music_dict():
        chosen_pieces = g.playlistManager.playlists[playlist_id].music_order_list
        available_music_pieces = {}
        for key in available_music:
            available_music_pieces[f'{key}'] = available_music[f'{key}']
        for selected_key in chosen_pieces:
            available_music_pieces.pop(selected_key)
        return available_music_pieces, chosen_pieces

    if check_session(g.playlistManager):

        edit_form = EditingForm()
        playlist = g.playlistManager.playlists[playlist_id]
        playlist_music_pieces = playlist.music_list
        available_music_to_user = create_available_music_dict()

        playlist_name = playlist.playlist_name

        if edit_form.validate_on_submit():
            playlist.playlist_name = edit_form.playlist_name.data

            if edit_form.playlist_image.data:
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], playlist.image)
                if os.path.exists(old_image_path) and playlist.image != DEFAULT_IMAGE:
                    os.remove(old_image_path)

                image_file = edit_form.playlist_image.data
                original_filename = secure_filename(image_file.filename)
                unique_filename = f"{playlist_id}_{original_filename}"
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

                image_file.save(image_path)
                playlist.image = unique_filename

            else:
                playlist.image = request.form.get("current_playlist_image", playlist.image)

            playlist.music_order_list.clear()
            playlist.music_list.clear()
            chosen_music_pieces = request.form.get("chosen_music_pieces", "")
            selected_music = chosen_music_pieces.split(",") if chosen_music_pieces else []

            for value in selected_music:
                playlist.music_order_list.append(value)
                playlist.music_list.append(add_music_pieces(value))

            flash("Playlist updated successfully!", "success")
            return redirect(url_for('view_playlist', playlist_id=playlist_id))

        return render_template('editing.html',
                               playlist_id=playlist_id,
                               title= f'Editing: {playlist.playlist_name}',
                               form=edit_form, playlist_image_url=playlist.image,
                               playlist_name=playlist_name,
                               chosen_music_pieces=playlist_music_pieces,
                               chosen_music_piece_values=available_music_to_user[1],
                               available_music=available_music_to_user[0])

    else:
        return provide_error_message()

@app.route('/delete_playlist/<int:playlist_id>', methods= ['GET', 'POST'])
def delete_playlist(playlist_id):
    if check_session(g.playlistManager):

        g.playlistManager.delete_playlist(playlist_id= playlist_id)
        return redirect(url_for('load_content'))

    else:
        return provide_error_message()

@app.route('/playlist/<int:playlist_id>')
def view_playlist(playlist_id):

    if check_session(g.playlistManager):

        playlist = g.playlistManager.playlists[playlist_id]
        music_list = playlist.music_list
        return render_template('playlist.html', playlist_id=playlist_id, title=f'Playlists/{playlist.playlist_name}', playlist_title=playlist.playlist_name, playlist_image=playlist.image, music_list= music_list)

    else:
        return provide_error_message()

@app.route('/play/<int:index>/<int:playlist_id>')
def play_page(index, playlist_id):

    if check_session(g.playlistManager):

        len_of_playlist = len(g.playlistManager.playlists[playlist_id].music_list)
        return render_template('playing.html',
                               index= index,
                               playlist_id= playlist_id,
                               playlist_len= len_of_playlist)

    else:
        return provide_error_message()

@app.route('/play_specific/<int:index>/<int:playlist_id>')
def play_specific(index, playlist_id):

    if check_session(g.playlistManager):

        len_of_playlist = len(g.playlistManager.playlists[playlist_id].music_list)
        return render_template('playing.html',
                               index= index,
                               playlist_id= playlist_id,
                               playlist_len= len_of_playlist)

    else:
        return provide_error_message()

@app.route('/api/get/<int:playlist_id>')
def play_api(playlist_id):

    if check_session(g.playlistManager):

        g.playlistManager.start_playing_playlist(index= 0, playlist_id= playlist_id)
        return jsonify([convert_to_valid_json_value(), g.playlistManager.piece_id_value_list])

    else:
        return provide_error_message()

@app.route('/api/get_specific/<int:index>/<int:playlist_id>')
def get_specific(index, playlist_id):

    if check_session(g.playlistManager):

        g.playlistManager.start_playing_playlist(index= index,playlist_id= playlist_id)
        return jsonify([convert_to_valid_json_value(), g.playlistManager.piece_id_value_list])

    else:
        return provide_error_message()

@app.route('/shuffle/<string:index>/<int:playlist_id>')
def shuffle(index, playlist_id):

    if check_session(g.playlistManager):

        len_of_playlist = len(g.playlistManager.playlists[playlist_id].music_list)
        return render_template('playing.html',
                               index=str(index),
                               playlist_id=playlist_id,
                               playlist_len=len_of_playlist)

    else:
        return provide_error_message()

@app.route('/api/get_shuffle/-1/<int:playlist_id>')
def shuffle_api(playlist_id):

    if check_session(g.playlistManager):

        g.playlistManager.start_playing_playlist(index= -1, playlist_id= playlist_id)
        return jsonify([convert_to_valid_json_value(), g.playlistManager.piece_id_value_list])

    else:
        return provide_error_message()

@app.route('/api/next')
def next_():

    if check_session(g.playlistManager):

        g.playlistManager.next_()
        return jsonify([convert_to_valid_json_value(), g.playlistManager.piece_id_value_list])

    else:
        return provide_error_message()

@app.route('/api/prev')
def prev():

    if check_session(g.playlistManager):

        g.playlistManager.previous_()
        return jsonify([convert_to_valid_json_value(), g.playlistManager.piece_id_value_list])

    else:
        return provide_error_message()

@app.route('/api/shuffle_from/<int:index>/<int:playlist_id>')
def shuffle_from(index, playlist_id):

    if check_session(g.playlistManager):

        g.playlistManager.create_shuffle_from_index(index= index, playlist_id= playlist_id)
        return jsonify(index)

    else:
        return provide_error_message()

@app.route('/api/update_value_list', methods=['POST'])
def update_value_list():

    def validate_value_list():
        unadded_values = []

        for value in temp_list:
            if value in g.playlistManager.piece_id_value_list:
                continue
            else:
                unadded_values.append(value)
        return unadded_values

    if check_session(g.playlistManager):

        data = request.json
        temp_list = data.get('tempValueList')
        new_list =  validate_value_list() + g.playlistManager.piece_id_value_list
        g.playlistManager.piece_id_value_list = new_list
        return jsonify(g.playlistManager.piece_id_value_list)

    else:
        return provide_error_message()

@app.route('/api/get/value_list')
def get_value_list():

    if check_session(g.playlistManager):

        return jsonify(g.playlistManager.piece_id_value_list)

    else:
        return provide_error_message()

@app.route('/api/unshuffle_playlist/<int:index>/<int:playlist_id>')
def unshuffle_playlist(index, playlist_id):

    if check_session(g.playlistManager):

        g.playlistManager.unshuffle_playlist(currently_playing_index=index, playlist_id=playlist_id)
        return jsonify(g.playlistManager.piece_id_value_list)

    else:
        return provide_error_message()

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port=3000)
