"""Video Processing
====================

Compresses video files previously recorded.
"""
from typing import List
from os.path import dirname, join, exists, isfile, abspath
import os
import subprocess
import itertools
import sys
import traceback
from threading import Thread
import time
from queue import Queue, Empty
import pathlib
import ffpyplayer

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, \
    ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleKVIDsDataViewBehavior
from kivy.uix.gridlayout import GridLayout

from base_kivy_app.app import app_error, report_exception_in_app
from base_kivy_app.utils import pretty_space


class SourcePath(EventDispatcher):

    source_viz = StringProperty('')

    source: pathlib.Path = pathlib.Path()

    name = ''

    parent: pathlib.Path = ''

    is_file = False

    contents: List['MediaContentItem'] = []

    manager: 'CompressionManager' = None

    processing = BooleanProperty(False)

    def __init__(self, manager: 'CompressionManager', **kwargs):
        super(SourcePath, self).__init__(**kwargs)
        self.manager = manager
        self.contents = []
        self.set_source('/')

    def apply_config_properties(self, source, source_viz):
        source = pathlib.Path(source)
        self.source = source = source.expanduser().absolute()
        self.is_file = source.is_file()

        self.name = source.name
        self.parent = source.parent
        self.source_viz = source_viz

    def set_source(self, source):
        """May only be called from Kivy thread.

        :param source: Source file/directory.
        """
        source = pathlib.Path(source)
        self.source = source = source.expanduser().absolute()
        self.is_file = source.is_file()
        if not source.is_file() and not source.is_dir():
            raise ValueError

        self.name = source.name
        self.parent = source.parent
        self.contents = []

    def refresh_contents(self, target_root, target_suffix, match_suffix):
        manager = self.manager
        # tell user we start processing and clear old contents
        manager.setattr_in_kivy_thread(self, 'processing', True)
        self.contents = []

        try:
            if self.is_file:
                item = MediaContentItem(self.source, self.parent)
                item.set_target(target_root, target_suffix)
                self.contents = [item]
            else:
                self.contents = self.walk_content_dir(
                    target_root, target_suffix, match_suffix)
        finally:
            manager.setattr_in_kivy_thread(self, 'processing', False)

    def walk_content_dir(self, target_root, target_suffix, match_suffix):
        source_root = self.parent
        contents = []

        for base in self.source.glob('**'):
            for file in base.glob('*' + match_suffix):
                if not file.is_file():
                    continue

                item = MediaContentItem(file, source_root)
                item.set_target(target_root, target_suffix)
                contents.append(item)

        return contents

    def refresh_contents_target_path(self, target_root, target_suffix):
        manager = self.manager
        # tell user we start processing and clear old contents
        manager.setattr_in_kivy_thread(self, 'processing', True)

        try:
            for item in self.contents:
                item.set_target(target_root, target_suffix)
        finally:
            manager.setattr_in_kivy_thread(self, 'processing', False)

    def refresh_contents_target_suffix(self, target_suffix):
        manager = self.manager
        # tell user we start processing and clear old contents
        manager.setattr_in_kivy_thread(self, 'processing', True)

        try:
            for item in self.contents:
                item.set_target_suffix(target_suffix)
        finally:
            manager.setattr_in_kivy_thread(self, 'processing', False)


class MediaContentItem(object):

    filename: pathlib.Path = None

    file_size = 0

    source_root: pathlib.Path = None
    """The parent directory of the selected directory or file.
    """

    target_filename: pathlib.Path = None

    target_file_size = 0

    exists = False

    command = ''

    result = ''

    skip = False

    status = ''
    """Can be one of ``''``, ``'processing'``, ``'failed'``, or ``'done'``.
    """

    item_index = None

    _cmd = []

    def __init__(self, filename: pathlib.Path, source_root: pathlib.Path):
        super(MediaContentItem, self).__init__()
        self.filename = filename
        self.source_root = source_root
        self.file_size = filename.stat().st_size

    def set_target(self, target_root: pathlib.Path, suffix):
        self.target_filename = target = target_root.joinpath(
            self.filename.relative_to(self.source_root)).with_suffix(suffix)
        self.exists = target.exists()
        if self.exists:
            self.target_file_size = target.stat().st_size
        else:
            self.target_file_size = 0

    def set_target_suffix(self, suffix):
        self.target_filename = target = self.target_filename.with_suffix(
            suffix)
        self.exists = target.exists()
        if self.exists:
            self.target_file_size = target.stat().st_size
        else:
            self.target_file_size = 0

    def check_target_exists(self):
        self.exists = self.target_filename.exists()
        if self.exists:
            self.target_file_size = self.target_filename.stat().st_size
        else:
            self.target_file_size = 0

    def get_gui_data(self):
        size = self.target_file_size
        target_size = pretty_space(size) if size else ''

        return {
            'filename.text': str(self.filename),
            'target_filename.text': str(self.target_filename),
            'exists': self.exists,
            'file_size.text': pretty_space(self.file_size),
            'command': self.command,
            'result': self.result,
            'status': self.status,
            'media_item': self,
            'skip.state': 'down' if self.skip else 'normal',
            'target_file_size.text': target_size,
        }

    def prepare_process_file(self, ffmpeg_binary, ffmpeg_opts: list):
        self.status = 'processing'
        self._cmd = []
        self.command = ''
        self.result = ''

        try:
            assert not self.skip
            self._cmd = [ffmpeg_binary, '-i', str(self.filename)] + \
                list(map(str, ffmpeg_opts)) + [str(self.target_filename)]
            self.command = ' '.join(self._cmd)
        except BaseException as e:
            self.status = 'failed'
            self.result = 'Error: {}\n\n'.format(e)
            self.result += ''.join(traceback.format_exception(*sys.exc_info()))

    def process_file(self):
        if self.status == 'failed':
            return

        try:
            parent: pathlib.Path = self.target_filename.parent
            if not parent.exists():
                os.makedirs(str(parent))
            proc = subprocess.run(
                self._cmd, capture_output=True, text=True,
                stdin=subprocess.PIPE)
        except BaseException as e:
            self.status = 'failed'
            self.result = 'Error: {}\n\n'.format(e)
            self.result += ''.join(traceback.format_exception(*sys.exc_info()))
            self.check_target_exists()
            return

        self.result = 'Output:\n{}\n\n:\n{}'.format(
            proc.stdout, proc.stderr)
        self.status = 'failed' if proc.returncode else 'done'
        self.check_target_exists()


class CompressionManager(EventDispatcher):

    _config_props_ = (
        'target_root', 'target_suffix', 'match_suffix', 'ffmpeg_vcodec',
        'ffmpeg_vcodec_opts', 'ffmpeg_disable_audio', 'ffmpeg_num_threads',
        'sources')

    target_root = StringProperty('')

    target_suffix = StringProperty('.mkv')

    match_suffix = StringProperty('.mkv')

    ffmpeg_vcodec = StringProperty('libx264')

    ffmpeg_vcodec_opts = ListProperty(['-preset', 'medium', '-crf', '17'])

    ffmpeg_disable_audio = BooleanProperty(True)

    ffmpeg_num_threads = NumericProperty(0)

    num_files = NumericProperty(0)

    total_size = NumericProperty(0)

    num_processed_files = NumericProperty(0)

    num_failed_files = NumericProperty(0)

    num_skipped_files = NumericProperty(0)

    processed_size = NumericProperty(0)

    fraction_done = NumericProperty(0)
    """By memory.
    """

    elapsed_time = NumericProperty(0)

    total_estimated_time = NumericProperty(0)

    recycle_view = None

    sources: List[SourcePath] = []

    ffmpeg_binary = ''

    trigger_run_in_kivy = None

    kivy_thread_queue = None

    internal_thread_queue = None

    thread = None

    thread_has_job = NumericProperty(0)

    currently_processing = BooleanProperty(False)

    currently_crawling = NumericProperty(0)

    stop_processing = False

    _start_processing_time = 0

    _elapsed_time_trigger = None

    def __init__(self, **kwargs):
        super(CompressionManager, self).__init__(**kwargs)
        self.sources = []
        self._elapsed_time_trigger = Clock.create_trigger(
            self._update_elapsed_time, timeout=.25, interval=True)

        def _update_fraction_done(*largs):
            if self.total_size:
                self.fraction_done = self.processed_size / self.total_size
            else:
                self.fraction_done = 0
        self.fbind('processed_size', _update_fraction_done)
        self.fbind('total_size', _update_fraction_done)

        def _update_total_estimated_time(*largs):
            if self.fraction_done:
                self.total_estimated_time = \
                    self.elapsed_time / self.fraction_done
            else:
                self.total_estimated_time = 0
        # self.fbind('elapsed_time', _update_total_estimated_time)
        self.fbind('fraction_done', _update_total_estimated_time)

        self.locate_ffmpeg()

        self.kivy_thread_queue = Queue()
        self.internal_thread_queue = Queue()
        self.trigger_run_in_kivy = Clock.create_trigger(
            self.process_queue_in_kivy_thread)
        self.thread = Thread(
            target=self.run_thread,
            args=(self.kivy_thread_queue, self.internal_thread_queue))
        self.thread.start()

    def _update_elapsed_time(self, *largs):
        self.elapsed_time = time.perf_counter() - self._start_processing_time

    def get_config_property(self, name):
        """(internal) used by the config system to get the list of config
        sources.
        """
        if name == 'sources':
            return [{
                'source': str(source.source), 'source_viz': source.source_viz}
                for source in self.sources]
        return getattr(self, name)

    def apply_config_property(self, name, value):
        """(internal) used by the config system to set the sources.
        """
        if name == 'sources':
            for data in value:
                source = self.create_source()
                source.apply_config_properties(
                    data.get('source', ''), data.get('source_viz', ''))
        else:
            setattr(self, name, value)

    def locate_ffmpeg(self):
        paths = []
        if hasattr(sys, '_MEIPASS'):
            paths.append(sys._MEIPASS)
        paths.extend(ffpyplayer.dep_bins)
        paths.append(os.path.abspath(os.path.dirname(sys.executable)))

        ffmpeg = ''
        for p in paths:
            if exists(join(p, 'ffmpeg.exe')):
                ffmpeg = join(p, 'ffmpeg.exe')
                break
            if exists(join(p, 'ffmpeg.so')):
                ffmpeg = join(p, 'ffmpeg.so')
                break

        if not ffmpeg:
            raise ValueError(
                'Cannot find ffmpeg at {}'.format(', '.join(paths)))
        self.ffmpeg_binary = ffmpeg

    def request_process_files(self):
        if self.thread_has_job:
            raise TypeError('Cannot start processing while already processing')
        # the thread is not currently processing, so it's safe to reset it
        self.stop_processing = False
        self.currently_processing = True
        self.thread_has_job += 1

        self.num_processed_files = 0
        self.processed_size = 0
        self.fraction_done = 0
        self.elapsed_time = 0
        self.total_estimated_time = 0
        self.num_skipped_files = 0
        self._start_processing_time = 0
        self.num_failed_files = 0
        self.internal_thread_queue.put(('process_files', None))

    def create_source(self, source_path=None):
        source = SourcePath(manager=self)
        self.sources.append(source)
        if source_path:
            self.request_set_source(source, source_path)
        app = App.get_running_app()
        if app is not None:
            app.compression_widget.source_container.add_widget(
                SourceWidget(source_obj=source, manager=self))

        return source

    def request_set_source(self, obj: SourcePath, source: str):
        self.thread_has_job += 1
        source = pathlib.Path(source)
        obj.source_viz = source = str(source.expanduser().absolute())
        self.internal_thread_queue.put(('set_source', (obj, source)))

    def request_check_target_exists(self):
        self.thread_has_job += 1
        self.internal_thread_queue.put(('check_target_exists', ()))

    def delete_source(self, source: SourcePath):
        self.sources.remove(source)
        app = App.get_running_app()
        if app is not None:
            source_container = app.compression_widget.source_container
            for widget in source_container.children:
                if widget.source_obj is source:
                    source_container.remove_widget(widget)
                    return
            assert False

    def request_set_skip(self, obj, skip):
        self.thread_has_job += 1
        self.internal_thread_queue.put(('set_skip', (obj, skip)))

    def request_refresh_contents(self, obj=None):
        self.thread_has_job += 1
        self.currently_crawling += 1
        self.internal_thread_queue.put(('refresh_contents', (obj, )))

    def request_refresh_target_path(self, paths):
        if not paths or not exists(paths[0]):
            return
        f = paths[0]
        if isfile(f):
            f = dirname(f)

        self.target_root = f
        self.thread_has_job += 1
        self.internal_thread_queue.put(('refresh_target_path', ()))

    def request_refresh_target_suffix(self, suffix: str):
        self.target_suffix = suffix
        self.thread_has_job += 1
        self.internal_thread_queue.put(('refresh_target_suffix', ()))

    def run_thread(self, kivy_queue, read_queue):
        kivy_queue_put = kivy_queue.put
        trigger = self.trigger_run_in_kivy
        Logger.info('Filers2: Starting thread for CompressionManager')

        while True:
            msg = ''
            try:
                msg, value = read_queue.get(block=True)
                if msg == 'eof':
                    Logger.info('Filers2: Exiting CompressionManager thread')
                    return

                if msg == 'set_source':
                    obj, source = value
                    obj.set_source(source)
                elif msg == 'set_skip':
                    obj, skip = value
                    obj.skip = skip
                    kivy_queue_put(
                        ('update_media_item',
                         (obj.item_index, obj.get_gui_data()))
                    )
                elif msg == 'refresh_contents':
                    self.refresh_sources_contents(value[0])
                elif msg == 'refresh_target_path':
                    self.refresh_sources_contents_target()
                elif msg == 'refresh_target_suffix':
                    self.refresh_sources_contents_suffix()
                elif msg == 'check_target_exists':
                    self.check_target_exists()
                elif msg == 'process_files':
                    self._start_processing_time = time.perf_counter()
                    self._elapsed_time_trigger()
                    self.compute_size_not_done()
                    self.process_files()
            except BaseException as e:
                kivy_queue_put(
                    ('exception',
                     (str(e),
                      ''.join(traceback.format_exception(*sys.exc_info()))))
                )
                trigger()
            finally:
                kivy_queue_put(
                    ('increment', (self, 'thread_has_job', -1)))
                if msg in ('process_files', ):
                    self._elapsed_time_trigger.cancel()
                    kivy_queue_put(
                        ('setattr', (self, 'currently_processing', False)))
                if msg in ('refresh_contents', ):
                    kivy_queue_put(
                        ('increment', (self, 'currently_crawling', -1)))
                trigger()

    def process_queue_in_kivy_thread(self, *largs):
        """Method that is called in the kivy thread when
        :attr:`trigger_run_in_kivy` is triggered. It reads messages from the
        thread.
        """
        while self.kivy_thread_queue is not None:
            try:
                msg, value = self.kivy_thread_queue.get(block=False)

                if msg == 'exception':
                    e, exec_info = value
                    report_exception_in_app(e, exc_info=exec_info)
                elif msg == 'setattr':
                    obj, prop, val = value
                    setattr(obj, prop, val)
                elif msg == 'increment':
                    obj, prop, val = value
                    setattr(obj, prop, getattr(obj, prop) + val)
                elif msg == 'update_contents':
                    self.num_files, self.total_size, self.recycle_view.data = \
                        value
                elif msg == 'update_media_items':
                    self.recycle_view.data = value
                elif msg == 'update_media_item':
                    i, item = value
                    self.recycle_view.data[i] = item
                else:
                    print('Got unknown CompressionManager message', msg, value)
            except Empty:
                break

    def setattr_in_kivy_thread(self, obj, prop, value):
        """Schedules kivy to set the property of the object to the specified
        value in the kivy thread.

        :param obj: The object with the property to be set.
        :param prop: The object property name to set.
        :param value: The value the property will be set to.
        """
        self.kivy_thread_queue.put(('setattr', (obj, prop, value)))
        self.trigger_run_in_kivy()

    def increment_in_kivy_thread(self, obj, prop, value=1):
        """Schedules kivy to increment the property by the specified value in
        the kivy thread.

        :param obj: The object with the property to increment
        :param prop: The object property name to increment.
        :param value: The value by which it will be incremented.
        """
        self.kivy_thread_queue.put(('increment', (obj, prop, value)))
        self.trigger_run_in_kivy()

    def refresh_sources_contents(self, source=None):
        target_root = pathlib.Path(self.target_root).expanduser().absolute()
        if not target_root.is_dir():
            raise ValueError
        target_suffix = self.target_suffix
        match_suffix = self.match_suffix

        if source is None:
            for source in self.sources:
                source.refresh_contents(
                    target_root, target_suffix, match_suffix)
        else:
            source.refresh_contents(target_root, target_suffix, match_suffix)

        total_size = 0
        num_files = 0
        for source in self.sources:
            for item in source.contents:
                num_files += 1
                total_size += item.file_size

        items = self.flatten_files(set_index=True)
        self.kivy_thread_queue.put(
            ('update_contents', (num_files, total_size, items))
        )
        self.trigger_run_in_kivy()

    def flatten_files(self, set_index=False) -> List[dict]:
        items = list((
            item.get_gui_data() for source in self.sources
            for item in source.contents))

        if set_index:
            for i, item in enumerate(items):
                item['media_item'].item_index = i
        return items

    def refresh_sources_contents_target(self):
        target_root = pathlib.Path(self.target_root).expanduser().absolute()
        if not target_root.is_dir():
            raise ValueError
        target_suffix = self.target_suffix

        for source in self.sources:
            source.refresh_contents_target_path(target_root, target_suffix)
        self.reset_file_status()

        self.kivy_thread_queue.put(
            ('update_media_items', self.flatten_files())
        )
        self.trigger_run_in_kivy()

    def refresh_sources_contents_suffix(self):
        target_suffix = self.target_suffix
        for source in self.sources:
            source.refresh_contents_target_suffix(target_suffix)
        self.reset_file_status()

        self.kivy_thread_queue.put(
            ('update_media_items', self.flatten_files())
        )
        self.trigger_run_in_kivy()

    def compute_size_not_done(self):
        total_size = 0
        num_files = 0
        for source in self.sources:
            for item in source.contents:
                # we don't include skipped files or those that exist
                if item.exists or item.skip:
                    continue
                num_files += 1
                total_size += item.file_size

        self.setattr_in_kivy_thread(self, 'num_files', num_files)
        self.setattr_in_kivy_thread(self, 'total_size', total_size)

    def reset_file_status(self):
        for source in self.sources:
            for item in source.contents:
                item.status = ''

    def check_target_exists(self):
        for source in self.sources:
            for item in source.contents:
                item.check_target_exists()
        self.reset_file_status()

        self.kivy_thread_queue.put(
            ('update_media_items', self.flatten_files())
        )
        self.trigger_run_in_kivy()

    def process_files(self):
        queue_put = self.kivy_thread_queue.put
        trigger = self.trigger_run_in_kivy
        ffmpeg_binary = self.ffmpeg_binary

        ffmpeg_opts = ['-nostdin', '-vcodec', self.ffmpeg_vcodec]
        ffmpeg_opts.extend(self.ffmpeg_vcodec_opts)
        if self.ffmpeg_disable_audio:
            ffmpeg_opts.append('-an')
        ffmpeg_opts.extend(['-threads', self.ffmpeg_num_threads])

        for source in self.sources:
            for item in source.contents:
                if self.stop_processing:
                    return
                if item.exists or item.skip:
                    queue_put(('increment', (self, 'num_skipped_files', 1)))
                    trigger()
                    continue

                if not item.skip:
                    item.prepare_process_file(ffmpeg_binary, ffmpeg_opts)
                    queue_put(
                        ('update_media_item',
                         (item.item_index, item.get_gui_data()))
                    )

                    item.process_file()
                    queue_put(
                        ('update_media_item',
                         (item.item_index, item.get_gui_data()))
                    )
                    if item.status != 'done':
                        queue_put(('increment', (self, 'num_failed_files', 1)))
                queue_put(('increment', (self, 'num_processed_files', 1)))
                queue_put(
                    ('increment', (self, 'processed_size', item.file_size)))
                trigger()

    def stop(self):
        if self.internal_thread_queue:
            self.internal_thread_queue.put(('eof', None))
        if self.thread is not None:
            self.thread.join()


class CompressionWidget(BoxLayout):

    manager: CompressionManager = ObjectProperty(None)

    source_container = ObjectProperty(None)


class SourceWidget(BoxLayout):

    def __init__(self, source_obj=None, manager=None, **kwargs):
        self.source_obj = source_obj
        self.manager = manager
        super(SourceWidget, self).__init__(**kwargs)

    source_obj: SourcePath = None

    manager: CompressionManager = None

    def set_source(self, paths):
        """Called by the GUI to set the filename.
        """
        if not paths:
            return
        # set this source
        self.manager.request_set_source(self.source_obj, paths[0])
        for item in paths[1:]:
            self.manager.create_source(item)


class MediaItemView(RecycleKVIDsDataViewBehavior, GridLayout):
    pass


Builder.load_file(join(dirname(__file__), 'compression_style.kv'))
