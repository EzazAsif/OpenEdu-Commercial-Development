from .models import Slide, Video, Note, temp_Slide, temp_Video, temp_Note
from .contentUploadAdapter import ContentUploadAdapter
from abc import ABC, abstractmethod


class AbstractContentFactory(ABC):
    @abstractmethod
    def create_content( faculty, name, content_file,uploaded_by):
        pass


class SlideFactory(AbstractContentFactory):
    def create_content( faculty, name, content_file,uploaded_by):
        slide_instance = Slide(
            name=name,
            faculty=faculty,
            content=content_file,
            uploaded_by=uploaded_by,
        )
        adapter = ContentUploadAdapter(content_type='slide', is_temp=False)
        upload_strategy = adapter.get_upload_strategy()
        slide_instance.content.upload_to = upload_strategy.get_upload_to
        slide_instance.save()
        return slide_instance


class VideoFactory(AbstractContentFactory):
    def create_content( faculty, name, content_file,uploaded_by):
        video_instance = Video(
            name=name,
            faculty=faculty,
            content=content_file,
            uploaded_by=uploaded_by,
        )
        adapter = ContentUploadAdapter(content_type='video', is_temp=False)
        upload_strategy = adapter.get_upload_strategy()
        video_instance.content.upload_to = upload_strategy.get_upload_to
        video_instance.save()
        return video_instance


class NoteFactory(AbstractContentFactory):
    def create_content( faculty, name, content_file,uploaded_by):
        note_instance = Note(
            name=name,
            faculty=faculty,
            content=content_file,
            uploaded_by=uploaded_by,
        )
        adapter = ContentUploadAdapter(content_type='note', is_temp=False)
        upload_strategy = adapter.get_upload_strategy()
        note_instance.content.upload_to = upload_strategy.get_upload_to
        note_instance.save()
        return note_instance


class AbstractTemporaryContentFactory(ABC):
    @abstractmethod
    def create_temp_content( real_instance, faculty, name, content_file,uploaded_by):
        pass


class TemporarySlideFactory(AbstractTemporaryContentFactory):
    def create_temp_content( real_instance, faculty, name, content_file,uploaded_by):
        temp_slide_instance = temp_Slide(
            name=name,
            real=real_instance,
            faculty=faculty,
            content=content_file,
            uploaded_by=uploaded_by,
        )
        adapter = ContentUploadAdapter(content_type='slide', is_temp=True)
        upload_strategy = adapter.get_upload_strategy()
        temp_slide_instance.content.upload_to = upload_strategy.get_upload_to
        temp_slide_instance.save()
        return temp_slide_instance


class TemporaryVideoFactory(AbstractTemporaryContentFactory):
    def create_temp_content( real_instance, faculty, name, content_file,uploaded_by):
        temp_video_instance = temp_Video(
            name=name,
            real=real_instance,
            faculty=faculty,
            content=content_file,
            uploaded_by=uploaded_by,
        )
        adapter = ContentUploadAdapter(content_type='video', is_temp=True)
        upload_strategy = adapter.get_upload_strategy()
        temp_video_instance.content.upload_to = upload_strategy.get_upload_to
        temp_video_instance.save()
        return temp_video_instance


class TemporaryNoteFactory(AbstractTemporaryContentFactory):
    def create_temp_content( real_instance, faculty, name, content_file,uploaded_by):
        temp_note_instance = temp_Note(
            name=name,
            real=real_instance,
            faculty=faculty,
            content=content_file,
            uploaded_by=uploaded_by,
        )
        adapter = ContentUploadAdapter(content_type='note', is_temp=True)
        upload_strategy = adapter.get_upload_strategy()
        temp_note_instance.content.upload_to = upload_strategy.get_upload_to
        temp_note_instance.save()
        return temp_note_instance
