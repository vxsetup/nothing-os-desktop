"""
Nothing OS — Window show/hide helpers
Instant show/hide — snappy like real OS
"""


def animate_show(window, **kwargs):
    """Instant show."""
    window.set_visible(True)
    window.present()


def animate_hide(window, on_done=None, **kwargs):
    """Instant hide."""
    window.set_visible(False)
    if on_done:
        on_done()
