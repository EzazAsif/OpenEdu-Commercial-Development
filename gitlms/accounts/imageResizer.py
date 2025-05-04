from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
import uuid
import os

class ImageResizeMixin:
    """Mixin to auto-resize and compress ImageField uploads."""
    MAX_WIDTH = 800      # Maximum width in pixels
    MAX_SIZE_KB = 400    # Maximum file size in kilobytes

    def save(self, *args, **kwargs):
        for field in self._meta.fields:
            if isinstance(field, models.ImageField):
                image_field = getattr(self, field.name)
                if not image_field:
                    continue  # No image uploaded for this field

                # Check if image is new or changed
                process_required = False
                if not image_field.name:
                    process_required = True
                elif self.pk:
                    try:
                        old_image = self.__class__.objects.get(pk=self.pk).__getattribute__(field.name)
                        if old_image and old_image.name != image_field.name:
                            process_required = True
                    except self.__class__.DoesNotExist:
                        process_required = True
                else:
                    process_required = True

                if not process_required:
                    continue

                # Try to open and validate the image
                try:
                    image_field.file.seek(0)
                    img = Image.open(image_field.file)
                    img.verify()  # Validate image
                    image_field.file.seek(0)
                    img = Image.open(image_field.file)
                except Exception as e:
                    print(f"[ImageResizeMixin] Skipping invalid image for '{field.name}': {e}")
                    continue

                original_format = img.format or 'JPEG'

                # Resize if needed
                if img.width > self.MAX_WIDTH:
                    new_height = int(img.height * (self.MAX_WIDTH / float(img.width)))
                    img = img.resize((self.MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

                # Prepare image for saving
                img_io = BytesIO()
                output_format = original_format

                if original_format.upper() in ["JPEG", "JPG", "JPEG2000"]:
                    quality = 85
                    img.save(img_io, format='JPEG', optimize=True, quality=quality)
                    while img_io.tell() > self.MAX_SIZE_KB * 1024 and quality > 20:
                        img_io.seek(0); img_io.truncate(0)
                        quality -= 5
                        img.save(img_io, format='JPEG', optimize=True, quality=quality)
                    output_format = 'JPEG'

                elif original_format.upper() == "PNG":
                    img.save(img_io, format='PNG', optimize=True, compress_level=9)
                    if img_io.tell() > self.MAX_SIZE_KB * 1024:
                        if img.mode in ("RGBA", "LA"):
                            background = Image.new("RGB", img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[3])
                            img = background
                        else:
                            img = img.convert("RGB")
                        img_io.seek(0); img_io.truncate(0)
                        quality = 85
                        img.save(img_io, format='JPEG', optimize=True, quality=quality)
                        while img_io.tell() > self.MAX_SIZE_KB * 1024 and quality > 20:
                            img_io.seek(0); img_io.truncate(0)
                            quality -= 5
                            img.save(img_io, format='JPEG', optimize=True, quality=quality)
                        output_format = 'JPEG'
                    else:
                        output_format = 'PNG'

                else:
                    img = img.convert("RGB")
                    img.save(img_io, format='JPEG', optimize=True, quality=85)
                    output_format = 'JPEG'

                # Generate safe file name
                ext = output_format.lower()
                unique_name = f"{uuid.uuid4().hex}.{ext}"
                if callable(field.upload_to):
                    upload_to_path = field.upload_to(self, unique_name)
                else:
                    upload_to_path = os.path.join(field.upload_to, unique_name)
                upload_to_path = os.path.normpath(upload_to_path)

                # Save compressed image to field
                image_content = ContentFile(img_io.getvalue())
                getattr(self, field.name).save(upload_to_path, image_content, save=False)

        # Final save
        super().save(*args, **kwargs)
