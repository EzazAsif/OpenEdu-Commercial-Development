import os
from abc import ABC, abstractmethod

class UploadStrategy(ABC):
    """
    Abstract Strategy class that defines the upload behavior for file fields.
    """
    @abstractmethod
    def get_upload_to(self, instance, filename):
        pass


# Strategy for Slide model (Base)
class SlideUploadStrategy(UploadStrategy):
    def get_upload_to(self, instance, filename):
        return os.path.join(
            'contents',
            instance.faculty.course.department.institute.name,
            instance.faculty.course.department.name,
            instance.faculty.course.course_name,
            instance.faculty.name,
            'slides',  # Folder for regular slides
            filename
        )

# Strategy for Video model (Base)
class VideoUploadStrategy(UploadStrategy):
    def get_upload_to(self, instance, filename):
        return os.path.join(
            'contents',
            instance.faculty.course.department.institute.name,
            instance.faculty.course.department.name,
            instance.faculty.course.course_name,
            instance.faculty.name,
            'videos',  # Folder for regular videos
            filename
        )

# Strategy for Note model (Base)
class NoteUploadStrategy(UploadStrategy):
    def get_upload_to(self, instance, filename):
        return os.path.join(
            'contents',
            instance.faculty.course.department.institute.name,
            instance.faculty.course.department.name,
            instance.faculty.course.course_name,
            instance.faculty.name,
            'notes',  # Folder for regular notes
            filename
        )

import os

class TempSlideUploadStrategy(UploadStrategy):
    def get_upload_to(self, instance, filename):
        if hasattr(instance, 'real') and instance.real:
            try:
                # Construct the file upload path using the 'real' instance
                return os.path.join(
                    'contents',
                    instance.faculty.course.department.institute.name,
                    instance.real.faculty.course.department.name,
                    instance.real.faculty.course.course_name,
                    instance.real.faculty.name,
                    'temp_slides',  # Temporary folder for slides
                    filename
                )
            except AttributeError:
                raise ValueError("Real instance is not linked properly for temp_Slide.")
        else:
            # If 'real' is not linked, use a default upload path
            return os.path.join(
                'contents', 
                'temp', 
                'slides',  # Default folder for slides
                filename
            )



# Strategy for Temporary Video model
class TempVideoUploadStrategy(UploadStrategy):
    def get_upload_to(self, instance, filename):
        if hasattr(instance, 'real') and instance.real:
            return os.path.join(
                'contents',
                instance.faculty.course.department.institute.name,
                instance.real.faculty.course.department.name,
                instance.real.faculty.course.course_name,
                instance.real.faculty.name,
                'temp_videos',  # Temporary folder for videos
                filename
            )
        else:
            # Default path when 'real' is not linked
            return os.path.join(
                'contents', 
                'temp', 
                'videos',  # Default folder for videos
                filename
            )

# Strategy for Temporary Note model
class TempNoteUploadStrategy(UploadStrategy):
    def get_upload_to(self, instance, filename):
        if hasattr(instance, 'real') and instance.real:
            return os.path.join(
                'contents',
                instance.faculty.course.department.institute.name,
                instance.real.faculty.course.department.name,
                instance.real.faculty.course.course_name,
                instance.real.faculty.name,
                'temp_notes',  # Temporary folder for notes
                filename
            )
        else:
            # Default path when 'real' is not linked
            return os.path.join(
                'contents', 
                'temp', 
                'notes',  # Default folder for notes
                filename
            )