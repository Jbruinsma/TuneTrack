from music_library import available_music
from node import LinkedList

class Playlist:
    def __init__(self, image, name):
        self.image = image
        self.playlist_name = name
        self.music_list = []
        self.music_order_list = []

class MusicObject:
    def __init__(self, music_name, music_artist, mp3_file, image):
        self.music_name = music_name
        self.music_artist = music_artist
        self.mp3_file = mp3_file
        self.image = image

def get_random(value):
    """Generate a random number from 0 to the provided value."""
    import random
    return random.randint(1, value)


class PlaylistManager:
    def __init__(self):

        self.playlist_ll = LinkedList()
        self.temp_shuffled_playlist_ll = LinkedList(start_label='shuffled_start', end_label='shuffled_end')

        self.piece_id_value_list = []
        self.shuffled_piece_id_value_list = []
        self.temp_value_list_storage = []

        self.playlists = []
        self.current_song_index = 1
        self.currently_playing = ''

    def create_playlist(self, returned_list):
        """Add Music Piece objects to the Music Piece list."""
        temp_playlist = []
        p_image = returned_list[0]
        p_name = returned_list[1]
        playlist = Playlist(image= p_image, name= p_name)
        rl_index = 0
        am_l = 1
        while rl_index < len(returned_list[2]):
            chosen_name = returned_list[2][rl_index]["name"]
            chosen_artist = returned_list[2][rl_index]["artist"]
            ml_name = available_music[f"{am_l}"]["music_name"]
            ml_artist = available_music[f"{am_l}"]["artist"]
            if chosen_name == ml_name and chosen_artist == ml_artist:
                name = chosen_name
                artist = chosen_artist
                mp3_file = available_music[f"{am_l}"]["mp3_file"]
                image = available_music[f"{am_l}"]["image"]
                music_object = MusicObject(name, artist, mp3_file, image)
                temp_playlist.append(music_object)
                rl_index += 1
            else:
                am_l += 1
        playlist.music_list = temp_playlist #CHANGE TO "song_list" IF BROKEN
        self.playlists.append(playlist)

    def delete_playlist(self, playlist_id):
        self.playlists.pop(playlist_id)

    def start_playing_playlist(self, index, playlist_id):
        """Return the first Music Piece object that will play."""

        def reset():
            """Reset the Playlist Manager's Linked List."""
            self.playlist_ll.reset_ll()
            self.currently_playing = self.playlist_ll.start
            self.piece_id_value_list.clear()

        def create_linked_list(chosen_index, chosen_playlist_id):
            """Create the Playlist Manager's Linked List and input Music Piece objects from the selected playlist."""

            reset()

            counter = 0
            while counter < len(self.playlists[chosen_playlist_id].music_list):
                self.playlist_ll.add_to_end(self.playlists[chosen_playlist_id].music_list[counter])
                counter += 1
                self.piece_id_value_list.append(counter)

            if chosen_index < 1:
                if chosen_index == 0:
                    self.currently_playing = self.currently_playing.next
                    pass
            else:
                counter = 0
                # print(self.piece_id_value_list)
                while counter < chosen_index - 1:
                    counter += 1
                    self.piece_id_value_list.remove(counter)
                    # print(self.piece_id_value_list)

                counter = 0

                while counter < chosen_index:
                    self.currently_playing = self.currently_playing.next
                    counter += 1

        def create_shuffled_linked_list(playlist_id):
            """Create a Shuffled Linked List from the selected playlist."""

            len_of_current_playlist = len(self.playlists[playlist_id].music_list)

            def add_values(len_of_playlist):
                random_value = get_random(len_of_playlist)
                if random_value not in self.piece_id_value_list:
                    self.piece_id_value_list.append(random_value)
                    return random_value
                else:
                    return add_values(len_of_playlist)

            reset()
            for i in range(len_of_current_playlist):
                chosen_index = add_values(len_of_current_playlist)
                val = self.playlists[playlist_id].music_list[chosen_index - 1]
                self.playlist_ll.add_to_end(val)
            self.currently_playing = self.playlist_ll.start.next


        if index < 0:
            # SHUFFLE OPTION
            create_shuffled_linked_list(playlist_id=playlist_id)
            return

        elif index > 0:
            # Specific Index Option
            create_linked_list(chosen_index= index, chosen_playlist_id= playlist_id)
            return
        else:
            # Play from Track 1 Option
            create_linked_list(chosen_index= 0, chosen_playlist_id= playlist_id)
            return

    def next_(self):
        """Return the next Music Piece object in the playlist."""
        if self.currently_playing.next.val == "end":
            self.currently_playing = self.playlist_ll.start.next
            return self.currently_playing
        else:
            self.currently_playing = self.currently_playing.next
            return self.currently_playing

    def previous_(self):
        """Return the previous Music Piece object in the playlist."""
        if self.currently_playing.prev.val == "start":
            self.currently_playing = self.playlist_ll.start.next
            return self.currently_playing
        else:
            self.currently_playing = self.currently_playing.prev
            return self.currently_playing

    def create_shuffle_from_index(self, index, playlist_id):
        """Create a Shuffled Linked List from the selected index."""

        def reset():
            """Reset the shuffled playlist and clear the value list."""
            self.temp_shuffled_playlist_ll.reset_ll()
            self.shuffled_piece_id_value_list.clear()

        def add_unique_value_to_temp_shuffled_value_list(random_val, temp_list, cur_index):
            """Add a unique random value to the temporary shuffled list."""
            if random_val != cur_index and random_val not in temp_list:
                temp_list.append(random_val)

        def add_to_temp_shuffled_ll(value_list):
            """Adds Values to the shuffled linked list."""

            def loop(offset, starting_node):
                """Loop through the original Linked List to obtain the Music Piece Object."""
                cur_piece = starting_node

                for i in range(0, offset):
                    cur_piece = cur_piece.next

                return cur_piece.val

            def add_to_ll(val):
                """Add a piece to the end of the shuffled linked list."""
                self.temp_shuffled_playlist_ll.add_to_end(val)

            start_point = self.playlist_ll.start
            for value in value_list:
                chosen_piece = loop(offset= value, starting_node= start_point)
                add_to_ll(chosen_piece)

            connecting_node = self.temp_shuffled_playlist_ll.start.next
            self.currently_playing.next = connecting_node
            connecting_node.prev = self.currently_playing

        def export_shuffled_value_list():
            """Export the shuffled value list to the JavaScript file for MusicPiece Value control."""
            self.temp_shuffled_playlist_ll.end.prev.next = self.currently_playing
            temp_shuffled_value_list.insert(0, index)
            self.temp_value_list_storage = self.piece_id_value_list
            self.piece_id_value_list = temp_shuffled_value_list

        temp_shuffled_value_list = []
        len_of_selected_playlist = len(self.playlists[playlist_id].music_list)

        reset()
        while len(temp_shuffled_value_list) < len_of_selected_playlist - 1:
            random_value = get_random(len_of_selected_playlist)
            add_unique_value_to_temp_shuffled_value_list(random_val= random_value, temp_list= temp_shuffled_value_list, cur_index= index)

        add_to_temp_shuffled_ll(value_list= temp_shuffled_value_list)
        export_shuffled_value_list()

    def unshuffle_playlist(self, currently_playing_index, playlist_id):
        """Delete the shuffled version of the Playlist Manager's Linked List and return the original Linked List."""
        self.piece_id_value_list = self.temp_value_list_storage
        self.temp_value_list_storage = []
        self.start_playing_playlist(index= currently_playing_index, playlist_id= playlist_id)
