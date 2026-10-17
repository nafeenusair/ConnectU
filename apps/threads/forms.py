from PIL import Image
from django import forms


ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}
MAX_PHOTO_SIZE = 5 * 1024 * 1024


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        return [super().clean(uploaded_file, initial) for uploaded_file in data]


class ThreadMessageUploadForm(forms.Form):
    photos = MultipleFileField(
        required=False,
    )

    def clean_photos(self):
        files = self.files.getlist("photos")
        cleaned_files = []

        for uploaded_file in files:
            if uploaded_file.size > MAX_PHOTO_SIZE:
                raise forms.ValidationError(
                    "Each image must be 5 MB or smaller."
                )

            if uploaded_file.content_type not in {
                "image/jpeg",
                "image/png",
                "image/webp",
                "image/gif",
            }:
                raise forms.ValidationError(
                    "Only JPEG, PNG, WEBP, and GIF images are allowed."
                )

            try:
                image = Image.open(uploaded_file)
                image.verify()
                if image.format not in ALLOWED_IMAGE_FORMATS:
                    raise forms.ValidationError(
                        "Only JPEG, PNG, WEBP, and GIF images are allowed."
                    )
            except (
                Image.DecompressionBombError,
                Image.UnidentifiedImageError,
                OSError,
                SyntaxError,
            ):
                raise forms.ValidationError(
                    "One of the uploaded files is not a valid image."
                )
            finally:
                uploaded_file.seek(0)

            cleaned_files.append(uploaded_file)

        return cleaned_files
