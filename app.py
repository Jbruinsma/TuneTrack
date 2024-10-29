import os
from playlistManager import PlaylistManager, Playlist
from music_library import available_music
from form import PlaylistForm
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['SECRET_KEY'] = 'secret'

playlistManager = PlaylistManager()

@app.route('/')
def load_content():
    user_playlists = playlistManager.playlists
    return render_template('home.html', title='Home', playlists=user_playlists)

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    form = PlaylistForm()
    form.selected_music.choices = [(key, f"{music['music_name']} - {music['artist']}") for key, music in available_music.items()]

    if form.validate_on_submit():
        file = request.files['playlist_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            playlist_name = form.playlist_name.data
            selected_music = form.selected_music.data
            print(f"Playlist created: {playlist_name}, Songs: {selected_music}, Image: {filename}")
            playlist_object = Playlist(name= playlist_name, image= filename)
            for song_key in selected_music:
                playlist_object.music_list.append(available_music[f"{song_key}"])
            playlistManager.playlists.append(playlist_object)
            print(f"Manager Playlist: {playlistManager.playlists}, Songs: {playlistManager.playlists[0].music_list}")
            print(len(playlistManager.playlists[0].music_list))
            return redirect(url_for('load_content'))
        else:
            flash("Invalid image file format.", "danger")
    else:
        print(f"Form errors: {form.errors}")

    return render_template('createPlaylist.html', title= 'Create Playlist', form=form, available_music=available_music)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/playlist/<int:playlist_id>')
def view_playlist(playlist_id):
    playlist = playlistManager.playlists[playlist_id]
    music_list = playlistManager.playlists[int(playlist_id)].music_list
    return render_template('playlist.html',
                           playlist_id=playlist_id,
                           title=f'Playlists/{playlist.playlist_name}',
                           playlist_title=playlist.playlist_name, playlist_image=playlist.image,
                           music_list=music_list)

@app.route('/play/<int:index>/<int:playlist_id>')
def play_page(index, playlist_id):
    len_of_playlist = len(playlistManager.playlists[playlist_id].music_list)
    return render_template('playing.html',
                           index= index,
                           playlist_id= playlist_id,
                           playlist_len= len_of_playlist)

@app.route('/play_specific/<int:index>/<int:playlist_id>')
def play_specific(index, playlist_id):
    len_of_playlist = len(playlistManager.playlists[playlist_id].music_list)
    return render_template('playing.html',
                           index= index,
                           playlist_id= playlist_id,
                           playlist_len= len_of_playlist)

@app.route('/api/get/<int:playlist_id>')
def play_api(playlist_id):
    playlistManager.start_playing_playlist(index= 0, playlist_id= playlist_id)
    return jsonify([playlistManager.currently_playing.val, playlistManager.piece_id_value_list])

@app.route('/api/get_specific/<int:index>/<int:playlist_id>')
def get_specific(index, playlist_id):
    playlistManager.start_playing_playlist(index= index,playlist_id= playlist_id)
    return jsonify([playlistManager.currently_playing.val, playlistManager.piece_id_value_list])

@app.route('/shuffle/<string:index>/<int:playlist_id>')
def shuffle(index, playlist_id):
    len_of_playlist = len(playlistManager.playlists[playlist_id].music_list)
    return render_template('playing.html',
                           index=str(index),
                           playlist_id=playlist_id,
                           playlist_len=len_of_playlist)

@app.route('/api/get_shuffle/-1/<int:playlist_id>')
def shuffle_api(playlist_id):
    starting_music = playlistManager.start_playing_playlist(index= -1, playlist_id= playlist_id)
    return jsonify([playlistManager.currently_playing.val, playlistManager.piece_id_value_list])

@app.route('/api/next')
def next_():
    playlistManager.next_()
    return jsonify([playlistManager.currently_playing.val, playlistManager.piece_id_value_list])

@app.route('/api/prev')
def prev():
    playlistManager.previous_()
    return jsonify([playlistManager.currently_playing.val, playlistManager.piece_id_value_list])

@app.route('/api/shuffle_from/<int:index>/<int:playlist_id>')
def shuffle_from(index, playlist_id):
    playlistManager.create_shuffle_from_index(index= index, playlist_id= playlist_id)
    return jsonify(index)

@app.route('/api/update_value_list', methods=['POST'])
def update_value_list():

    def validate_value_list():
        unadded_values = []

        for value in temp_list:
            if value in playlistManager.piece_id_value_list:
                continue
            else:
                unadded_values.append(value)
        return unadded_values

    data = request.json
    temp_list = data.get('tempValueList')
    new_list =  validate_value_list() + playlistManager.piece_id_value_list
    playlistManager.piece_id_value_list = new_list
    print(f"VALUE LIST: {playlistManager.piece_id_value_list}")
    return jsonify(playlistManager.piece_id_value_list)

@app.route('/api/get/value_list')
def get_value_list():
    return jsonify(playlistManager.piece_id_value_list)

@app.route('/api/unshuffle_playlist/<int:index>/<int:playlist_id>')
def unshuffle_playlist(index, playlist_id):
    playlistManager.unshuffle_playlist(currently_playing_index=index, playlist_id=playlist_id)
    return jsonify(playlistManager.currently_playing.val)

if __name__ == '__main__':
    app.run(debug=True)