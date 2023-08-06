from kivy.animation import Animation
from kivy.properties import NumericProperty, BooleanProperty
from kivy.factory import Factory
from kivy.clock import Clock


class LoadingAnim(object):

    anim_active = BooleanProperty(False)

    angle = NumericProperty(0)

    _anim = None

    _anim_trigger = None

    def __init__(self, **kwargs):
        super(LoadingAnim, self).__init__(**kwargs)
        self.fbind('anim_active', self._anim_active)
        self._anim_trigger = Clock.create_trigger(self._handle_anim_done)

    def _handle_anim_done(self, *largs):
        if self.anim_active:
            self.angle = 0
            self._anim.start(self)

    def _anim_active(self, *largs):
        if self.anim_active:
            if self._anim is None:
                self._anim = Animation(angle=360, duration=1)
                self._anim.fbind('on_complete', self._anim_trigger)

            self.angle = 0
            self._anim.start(self)
        else:
            self._anim.cancel(self)
            self.angle = 0
            self._anim_trigger.cancel()


Factory.register(classname='LoadingAnim', cls=LoadingAnim)
