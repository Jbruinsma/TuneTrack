from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PlaylistForm(FlaskForm):
    # The image field allows only image formats (jpg, png, jpeg)
    playlist_image = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # Playlist name is required
    playlist_name = StringField(validators=[DataRequired()])
    # Submit button
    submit = SubmitField('Create Playlist')

class EditingForm(FlaskForm):
        # The image field allows only image formats (jpg, png, jpeg)
        playlist_image = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
        # Playlist name is required
        playlist_name = StringField(validators=[DataRequired()])
        # Submit button
        submit = SubmitField('Edit Playlist')
    
