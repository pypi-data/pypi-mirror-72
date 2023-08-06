'''
Little graphic to show user that something is waited for when
a progress bar is overkill, or the progress is unknown.
'''
import asyncio
import colorama
import cursor
colorama.init()
from . import styles

_DOTS = ('   ', '.  ', '.. ', '...')

def _on_line_below(s):
    return f'\n{s}{colorama.Cursor.UP(1)}\r\033[K'

class Spinner:
    '''
    Options:

    message -- Text to show besides spinner (default '')

    style -- indexable collection of animation frames (default asyncspinner.styles.STRETCHING_SQUARE)
    fps -- how many animation frames to display per second (default 12)
    show_dots -- whether to 0 counting to 3 dots to the right of the animation and message
                 (default False if message is '' else True)
    dots_slowdown -- how many animation frames each number of dots should last for (default 6)
    '''

    def __init__(self, message='', *,
                 style=styles.STRETCHING_SQUARE,
                 fps=12,
                 show_dots=None,
                 dots_slowdown=6):
        self.message = message
        self.fps = fps
        self.frames = style

        if show_dots is None:
            show_dots = bool(message)
        self.dots = _DOTS if show_dots else ['']
        self.dots_slowdown = dots_slowdown

        self.stopper = asyncio.Event()
        self.frame_gen = self.get_frame_gen()

    def get_frame_gen(self):
        '''Make generator that gets each animation frame.'''
        i = 0
        while True:
            frame = self.frames[i%len(self.frames)]
            dot = self.dots[(i//self.dots_slowdown)%len(self.dots)]
            yield f'{frame} {self.message}{dot}'
            i += 1


    async def loop(self):
        '''Print animation frames as long as the context is active.'''
        while True:
            print(_on_line_below(next(self.frame_gen)), end='')
            try:
                await asyncio.wait_for(
                    self.stopper.wait(),
                    timeout=1/self.fps
                )
            except asyncio.exceptions.TimeoutError:
                continue
            break

    async def __aenter__(self):
        cursor.hide()
        self.stopper.clear()
        asyncio.create_task(self.loop())

    async def __aexit__(self, *_):
        cursor.show()
        self.stopper.set()
