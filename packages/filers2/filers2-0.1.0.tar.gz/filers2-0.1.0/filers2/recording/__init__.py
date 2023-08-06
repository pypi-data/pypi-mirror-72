"""Video Player
================

Plays and records media from e.g. a camera.
"""
from __future__ import annotations

from typing import List, Dict
from os.path import abspath, isdir, dirname, join, exists, expanduser, split, \
    splitext
import psutil
from ffpyplayer.pic import ImageLoader

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, \
    ObjectProperty, ListProperty, DictProperty
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from base_kivy_app.config import apply_config

from cpl_media.ptgray import PTGrayPlayer, PTGraySettingsWidget
from cpl_media.ffmpeg import FFmpegPlayer, FFmpegSettingsWidget
from cpl_media.thorcam import ThorCamPlayer, ThorCamSettingsWidget
from cpl_media.rtv import RTVPlayer, RTVSettingsWidget
from cpl_media.remote.client import RemoteVideoPlayer, \
    ClientPlayerSettingsWidget
from cpl_media.player import BasePlayer

from cpl_media.recorder import ImageFileRecorder, VideoRecorder, \
    ImageFileRecordSettingsWidget, VideoRecordSettingsWidget
from cpl_media.remote.server import RemoteVideoRecorder, \
    RemoteRecordSettingsWidget
from cpl_media.recorder import BaseRecorder

__all__ = ('FilersPlayer', 'PlayerWidget', 'PlayersContainerWidget')


class FilersPlayer(EventDispatcher):
    """Manages all the possible players and recorders for a single player.

    It opens all the players and recorders and controls which player/recorder
    is used by this player object.
    """

    _config_props_ = (
        'player_name', 'recorder_name', 'display_rotation', 'player_id',
        'records_with')

    _config_children_ = {
        'ffmpeg': 'ffmpeg_player', 'ptgray': 'ptgray_player',
        'thor': 'thor_player', 'network_client': 'client_player',
        'rtv': 'rtv_player', 'image_file_recorder': 'image_file_recorder',
        'video_recorder': 'video_recorder',
        'server_recorder': 'server_recorder',
    }

    player_id = NumericProperty(0)

    records_with = NumericProperty(-1)

    ffmpeg_player: FFmpegPlayer = None

    ffmpeg_settings = None

    ptgray_player: PTGrayPlayer = None

    ptgray_settings = None

    thor_player: ThorCamPlayer = None

    thor_settings = None

    client_player: RemoteVideoPlayer = None

    client_settings = None

    rtv_player: RTVPlayer = None

    rtv_settings = None

    player: BasePlayer = ObjectProperty(None, rebind=True)

    player_settings = ObjectProperty(None)

    player_name = StringProperty('ffmpeg')
    """The name of the underlying player used by this player.
    """

    player_to_raw_name_map = {
        'Webcam/File': 'ffmpeg', 'Network': 'client', 'Thor': 'thor',
        'PointGray': 'ptgray',
    }

    player_to_nice_name_map = {v: k for k, v in player_to_raw_name_map.items()}

    image_file_recorder: ImageFileRecorder = None

    image_file_recorder_settings = None

    video_recorder: VideoRecorder = None

    video_recorder_settings = None

    server_recorder: RemoteVideoRecorder = None

    server_recorder_settings = None

    recorder: BaseRecorder = ObjectProperty(None, rebind=True)

    recorder_settings = ObjectProperty(None)

    recorder_name = StringProperty('video')
    """The name of the underlying recorder used by this player.
    """

    recorder_to_raw_name_map = {
        'Images': 'image_file', 'Video': 'video', 'Server': 'server'}

    recorder_to_nice_name_map = {
        v: k for k, v in recorder_to_raw_name_map.items()}

    last_image = ObjectProperty(None)

    disk_used_percent = NumericProperty(0)
    '''Percent of disk usage space.
    '''

    player_widget: PlayerWidget = None

    display_rotation = NumericProperty(0)

    def __init__(self, open_player_thread=True, **kwargs):
        super(FilersPlayer, self).__init__(**kwargs)

        self.ffmpeg_player = FFmpegPlayer()
        self.ptgray_player = PTGrayPlayer(open_thread=open_player_thread)
        self.thor_player = ThorCamPlayer(open_thread=open_player_thread)
        self.client_player = RemoteVideoPlayer()
        self.rtv_player = RTVPlayer()

        self.image_file_recorder = ImageFileRecorder()
        self.video_recorder = VideoRecorder()
        self.server_recorder = RemoteVideoRecorder()

        self.fbind('player_name', self._update_player)
        self._update_player()

        self.fbind('recorder_name', self._update_recorder)
        self._update_recorder()

        self.ffmpeg_player.display_frame = self.display_frame
        self.ptgray_player.display_frame = self.display_frame
        self.thor_player.display_frame = self.display_frame
        self.client_player.display_frame = self.display_frame
        self.rtv_player.display_frame = self.display_frame

        Clock.schedule_interval(self.update_disk_usage, 0.1)

    def _update_player(self, *largs):
        self.player = getattr(self, '{}_player'.format(self.player_name))
        self.player_settings = getattr(
            self, '{}_settings'.format(self.player_name))

    def _update_recorder(self, *largs):
        self.recorder = getattr(self, '{}_recorder'.format(self.recorder_name))
        self.recorder_settings = getattr(
            self, '{}_recorder_settings'.format(self.recorder_name))

    def create_widgets(self):
        self.ffmpeg_settings = FFmpegSettingsWidget(player=self.ffmpeg_player)
        self.ptgray_settings = PTGraySettingsWidget(player=self.ptgray_player)
        self.thor_settings = ThorCamSettingsWidget(player=self.thor_player)
        self.client_settings = ClientPlayerSettingsWidget(
            player=self.client_player)
        self.rtv_settings = RTVSettingsWidget(player=self.rtv_player)

        self.image_file_recorder_settings = ImageFileRecordSettingsWidget(
            recorder=self.image_file_recorder)
        self.video_recorder_settings = VideoRecordSettingsWidget(
            recorder=self.video_recorder)
        self.server_recorder_settings = RemoteRecordSettingsWidget(
            recorder=self.server_recorder)

        self._update_player()
        self._update_recorder()

    def display_frame(self, image, metadata=None):
        """The displays the new image to the user.
        """
        self.player_widget.image_display.update_img(image)
        self.last_image = image

    def update_disk_usage(self, *largs):
        """Runs periodically to update the disk usage.
        """
        p = self.video_recorder.record_directory
        p = 'C:\\' if not exists(p) else (p if isdir(p) else dirname(p))
        if not exists(p):
            p = '/home'
        self.disk_used_percent = round(psutil.disk_usage(p).percent) / 100.

    def get_screenshot_filename(self):
        recorder = self.recorder
        if recorder is self.video_recorder:
            filename = join(
                recorder.record_directory,
                recorder.record_fname.format(recorder.record_fname_count))
            root, fname = split(filename)
            fname = splitext(fname)[0] + '.bmp'
        elif recorder is self.image_file_recorder:
            root = expanduser(recorder.record_directory)
            fname = recorder.record_prefix + '.bmp'
        else:
            root = expanduser('~')
            fname = ''

        if isdir(root):
            return join(root, fname)
        return join(expanduser('~'), fname)

    def save_screenshot(self, img, paths):
        """Saves the image acquired to a file.
        """
        if not paths:
            return

        if not isdir(dirname(paths[0])):
            raise Exception('Invalid path or filename')
        BaseRecorder.save_image(paths[0], img)

    def stop(self):
        for player in (
                self.ffmpeg_player, self.thor_player, self.client_player,
                self.image_file_recorder, self.video_recorder,
                self.ptgray_player, self.rtv_player, self.server_recorder):
            if player is not None:
                player.stop()

    def clean_up(self):
        for player in (
                self.ffmpeg_player, self.thor_player, self.client_player,
                self.image_file_recorder, self.video_recorder,
                self.ptgray_player, self.rtv_player, self.server_recorder):
            if player is not None:
                player.stop_all(join=True)


class PlayerWidget(BoxLayout):

    player = ObjectProperty(None)

    image_display = None


class PlayersContainerWidget(GridLayout):

    _config_children_ = {'players': 'players'}

    players: List[FilersPlayer] = ListProperty([])

    player_id_mapping: Dict[int, FilersPlayer] = DictProperty({})

    def apply_config_child(self, name, prop, obj, config):
        if prop != 'players':
            apply_config(obj, config)
            return

        while len(config) < len(self.players):
            player = self.players.pop()
            self.remove_widget(player.player_widget)
            player.clean_up()

        while len(config) > len(self.players):
            self.add_player()

        for player, config in zip(self.players, config):
            apply_config(player, config)

        self.recompute_player_id_mapping()

        return True

    def recompute_player_id_mapping(self):
        self.player_id_mapping = {p.player_id: p for p in self.players}

    def start_recording(self, player: FilersPlayer):
        seen = set()
        mapping = self.player_id_mapping

        while player is not None and player not in seen:
            player.recorder.record(player.player)
            seen.add(player)
            player = mapping.get(player.records_with, None)

    def stop_recording(self, player: FilersPlayer):
        seen = set()
        mapping = self.player_id_mapping

        while player is not None and player not in seen:
            player.recorder.stop()
            seen.add(player)
            player = mapping.get(player.records_with, None)

    def add_player(self, player_id=0):
        player = FilersPlayer(player_id=player_id)
        player.create_widgets()

        player.player_widget = widget = PlayerWidget(player=player)
        self.add_widget(widget)
        self.players.append(player)

        self.recompute_player_id_mapping()

    def remove_player(self, player: FilersPlayer):
        self.remove_widget(player.player_widget)
        self.players.remove(player)
        player.clean_up()

        self.recompute_player_id_mapping()

    def clean_up(self):
        for player in self.players:
            player.clean_up()


Builder.load_file(join(dirname(__file__), 'player_style.kv'))
