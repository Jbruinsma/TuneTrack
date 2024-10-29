from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, ValidationError

class PlaylistForm(FlaskForm):
    # The image field allows only image formats (jpg, png, jpeg)
    playlist_image = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    # Playlist name is required
    playlist_name = StringField(validators=[DataRequired()])
    # At least one song must be selected
    selected_music = SelectMultipleField('Select Music', choices=[], validators=[DataRequired()])
    submit = SubmitField('Create Playlist')

    # Custom validation to ensure at least one song is selected
    def validate_selected_music(self, field):
        if not field.data:
            raise ValidationError('You must select at least one song for the playlist.')
