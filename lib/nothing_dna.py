"""
Nothing OS — Design DNA library
Reusable widgets: dot-matrix glyphs, animations, glyph icons
Import this from all nothing-* apps for visual consistency

PULSE_DISABLED — globally disables decorative pulse rings (default: True).
Recording / critical states have their own visual cues without it.
"""

import math
import os
import sys
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gdk, Pango


# ── GLOBAL TOGGLES ──────────────────────────────────────────────

# Disables all PulseRing animations (decorative red circles around icons)
PULSE_DISABLED = True

# Disables HeartbeatDot animation (header indicators become static)
HEARTBEAT_STATIC = True


# ── COLORS ──────────────────────────────────────────────────────

class Color:
    BG_DEEP     = (0.031, 0.031, 0.031, 1)   # #080808
    BG_CARD     = (0.047, 0.047, 0.047, 1)   # #0C0C0C
    BG_RAISED   = (0.063, 0.063, 0.063, 1)   # #101010
    BORDER      = (0.122, 0.122, 0.122, 1)   # #1F1F1F

    TEXT_HI     = (0.910, 0.902, 0.890, 1)   # #E8E6E3
    TEXT_MID    = (0.533, 0.533, 0.533, 1)   # #888888
    TEXT_LOW    = (0.227, 0.227, 0.227, 1)   # #3A3A3A
    TEXT_DEAD   = (0.122, 0.122, 0.122, 1)   # #1F1F1F

    RED         = (0.839, 0.188, 0.188, 1)   # #D63030
    RED_BRIGHT  = (1.000, 0.314, 0.314, 1)   # #FF5050
    RED_GLOW    = (0.839, 0.188, 0.188, 0.35)

    GREEN       = (0.298, 0.686, 0.314, 1)   # #4CAF50
    AMBER       = (0.850, 0.650, 0.200, 1)


# ── DOT-MATRIX FONT (5x7) ───────────────────────────────────────

DOT_FONT_5x7 = {
    '0': [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    '1': [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    '2': [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b01000, 0b11111],
    '3': [0b11110, 0b00001, 0b00001, 0b01110, 0b00001, 0b00001, 0b11110],
    '4': [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    '5': [0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
    '6': [0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    '7': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    '8': [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    '9': [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100],

    'A': [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'B': [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    'C': [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    'D': [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    'E': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    'F': [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    'G': [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01110],
    'H': [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    'I': [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    'J': [0b00111, 0b00010, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    'K': [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    'L': [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    'M': [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    'N': [0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
    'O': [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'P': [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    'Q': [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    'R': [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    'S': [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    'T': [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    'U': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    'V': [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    'W': [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
    'X': [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    'Y': [0b10001, 0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100],
    'Z': [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],

    ' ': [0, 0, 0, 0, 0, 0, 0],
    '.': [0, 0, 0, 0, 0, 0b00110, 0b00110],
    ':': [0, 0b00110, 0b00110, 0, 0b00110, 0b00110, 0],
    '-': [0, 0, 0, 0b01110, 0, 0, 0],
    '%': [0b11001, 0b11010, 0b00010, 0b00100, 0b01000, 0b01011, 0b10011],
    '/': [0b00001, 0b00010, 0b00010, 0b00100, 0b01000, 0b01000, 0b10000],
    '+': [0, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0],
    '=': [0, 0, 0b11111, 0, 0b11111, 0, 0],
    '°': [0b01100, 0b10010, 0b01100, 0, 0, 0, 0],
    '·': [0, 0, 0, 0b00110, 0, 0, 0],
    '#': [0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010],
}


def _draw_dot(cr, x, y, radius, color):
    cr.set_source_rgba(*color)
    cr.arc(x, y, radius, 0, 6.2832)
    cr.fill()


class DotGlyph(Gtk.DrawingArea):
    """Renders text using 5x7 dot-matrix font in Nothing OS style."""

    def __init__(self, text='', dot_size=4, gap=2, char_gap=2,
                 color=Color.TEXT_HI, dim_color=None,
                 show_grid=True, dim_alpha=0.07):
        super().__init__()
        self._text = text.upper()
        self.dot_size = dot_size
        self.gap = gap
        self.char_gap = char_gap
        self.color = color
        self.show_grid = show_grid
        self.dim_color = dim_color or (color[0], color[1], color[2], dim_alpha)
        self.set_draw_func(self._draw)
        self._update_size()

    def set_text(self, text):
        self._text = text.upper()
        self._update_size()
        self.queue_draw()

    def set_color(self, color):
        self.color = color
        if isinstance(self.dim_color, tuple) and len(self.dim_color) == 4:
            self.dim_color = (color[0], color[1], color[2], self.dim_color[3])
        self.queue_draw()

    def get_text(self):
        return self._text

    def _char_width_dots(self):
        return 5

    def _char_height_dots(self):
        return 7

    def _update_size(self):
        cw = self._char_width_dots()
        ch = self._char_height_dots()
        step = self.dot_size + self.gap
        char_pixel_w = cw * step - self.gap
        char_pixel_h = ch * step - self.gap

        n = max(1, len(self._text))
        total_w = n * char_pixel_w + (n - 1) * self.char_gap if n > 1 else char_pixel_w
        self.set_content_width(int(total_w + self.dot_size))
        self.set_content_height(int(char_pixel_h + self.dot_size))

    def _draw(self, area, cr, w, h):
        cw = self._char_width_dots()
        ch = self._char_height_dots()
        step = self.dot_size + self.gap
        char_pixel_w = cw * step - self.gap

        radius = self.dot_size / 2

        x_offset = radius
        for char in self._text:
            glyph = DOT_FONT_5x7.get(char, DOT_FONT_5x7[' '])
            for row in range(ch):
                bits = glyph[row]
                for col in range(cw):
                    cx = x_offset + col * step
                    cy = radius + row * step
                    if bits & (1 << (4 - col)):
                        _draw_dot(cr, cx, cy, radius, self.color)
                    elif self.show_grid:
                        _draw_dot(cr, cx, cy, radius * 0.6, self.dim_color)
            x_offset += char_pixel_w + self.char_gap


# ── LIVING DOT MATRIX ───────────────────────────────────────────

class LiveDotMatrix(Gtk.DrawingArea):
    """Decorative dots — can pulse or stay static. Hover-wave kept (subtle)."""

    def __init__(self, cols=44, rows=2, dot_size=2, spacing=7,
                 base_alpha=0.18, pulse=True, color=Color.RED):
        super().__init__()
        self.cols = cols
        self.rows = rows
        self.dot_size = dot_size
        self.spacing = spacing
        self.base_alpha = base_alpha
        self.color = color
        # Honor global pulse flag — if PULSE_DISABLED, no animation
        self.pulse = pulse and not PULSE_DISABLED
        self.phase = 0.0
        self.hover_x = -1
        self.hover_y = -1
        self.wave_t = 0.0
        self._wave_active = False

        self.set_content_width(cols * spacing)
        self.set_content_height(rows * spacing)
        self.set_draw_func(self._draw)

        if self.pulse:
            GLib.timeout_add(60, self._tick)

        # Hover-wave controller — keep it (it only animates on user interaction)
        motion = Gtk.EventControllerMotion()
        motion.connect('motion', self._on_motion)
        motion.connect('leave', self._on_leave)
        self.add_controller(motion)

    def _tick(self):
        self.phase = (self.phase + 0.08) % (2 * math.pi)
        if self._wave_active:
            self.wave_t += 0.07
            if self.wave_t > 2.0:
                self._wave_active = False
                self.wave_t = 0
        self.queue_draw()
        return True

    def _on_motion(self, ctrl, x, y):
        self.hover_x = x
        self.hover_y = y
        if not self._wave_active and not PULSE_DISABLED:
            # only trigger wave when pulse is allowed
            self._wave_active = True
            self.wave_t = 0
        self.queue_draw()

    def _on_leave(self, *args):
        self.hover_x = -1
        self.hover_y = -1
        self.queue_draw()

    def trigger_wave(self):
        if PULSE_DISABLED:
            return
        self._wave_active = True
        self.wave_t = 0
        # Need ticker running to animate the wave
        if not self.pulse:
            self.pulse = True
            GLib.timeout_add(60, self._tick)
        self.queue_draw()

    def _draw(self, area, cr, w, h):
        for r in range(self.rows):
            for c in range(self.cols):
                x = c * self.spacing + self.spacing / 2
                y = r * self.spacing + self.spacing / 2

                alpha = self.base_alpha

                # Breathing pulse (only if enabled)
                if self.pulse:
                    pulse_offset = math.sin(self.phase + c * 0.18 + r * 0.4)
                    alpha += pulse_offset * 0.06

                # Hover wave
                if self.hover_x >= 0:
                    dx = x - self.hover_x
                    dy = y - self.hover_y
                    dist = math.sqrt(dx * dx + dy * dy)
                    proximity = max(0, 1 - dist / 60)
                    alpha += proximity * 0.55

                # Radial wave
                if self._wave_active:
                    cx, cy = w / 2, h / 2
                    dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                    wave_r = self.wave_t * 80
                    if abs(dist - wave_r) < 12:
                        intensity = 1 - abs(dist - wave_r) / 12
                        alpha += intensity * 0.7

                alpha = max(0.04, min(1.0, alpha))
                cr.set_source_rgba(self.color[0], self.color[1],
                                   self.color[2], alpha)
                cr.arc(x, y, self.dot_size / 2, 0, 6.2832)
                cr.fill()


# ── PULSE RING ──────────────────────────────────────────────────

class PulseRing(Gtk.DrawingArea):
    """Animated ring around an element. Globally disabled by PULSE_DISABLED."""

    def __init__(self, size=56, color=Color.RED, active=False, speed=0.05):
        super().__init__()
        self.size = size
        self.color = color
        self._active = active
        self.speed = speed
        self.t = 0.0
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)
        if active and not PULSE_DISABLED:
            self._start()

    def set_active(self, active):
        was = self._active
        self._active = active
        if active and not was and not PULSE_DISABLED:
            self._start()
        # When disabled globally — just no-op; nothing draws

    def _start(self):
        if PULSE_DISABLED:
            return
        self.t = 0.0
        GLib.timeout_add(40, self._tick)

    def _tick(self):
        if not self._active or PULSE_DISABLED:
            self.queue_draw()
            return False
        self.t += self.speed
        if self.t > 2.0:
            self.t = 0
        self.queue_draw()
        return True

    def _draw(self, area, cr, w, h):
        # If globally disabled — draw nothing
        if PULSE_DISABLED:
            return
        if not self._active:
            return
        cx = w / 2
        cy = h / 2
        for offset in (0.0, 1.0):
            phase = (self.t + offset) % 2.0
            radius = (self.size * 0.3) + phase * (self.size * 0.45)
            alpha = max(0, 1 - phase / 2) * 0.4
            cr.set_source_rgba(self.color[0], self.color[1],
                               self.color[2], alpha)
            cr.set_line_width(1.5)
            cr.arc(cx, cy, radius, 0, 6.2832)
            cr.stroke()


# ── HEARTBEAT DOT ───────────────────────────────────────────────

class HeartbeatDot(Gtk.DrawingArea):
    """Single dot — animated heartbeat OR static (per HEARTBEAT_STATIC flag)."""

    def __init__(self, size=12, color=Color.RED, active=True):
        super().__init__()
        self.size = size
        self.color = color
        self._active = active
        self.t = 0.0
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)
        # Only animate when allowed
        if not HEARTBEAT_STATIC:
            GLib.timeout_add(50, self._tick)

    def set_active(self, active):
        self._active = active
        self.queue_draw()

    def _tick(self):
        if HEARTBEAT_STATIC:
            return False
        self.t = (self.t + 0.05) % (2 * math.pi)
        self.queue_draw()
        return True

    def _draw(self, area, cr, w, h):
        cx = w / 2
        cy = h / 2

        if not self._active:
            # Static dim dot
            cr.set_source_rgba(0.227, 0.227, 0.227, 1)
            cr.arc(cx, cy, self.size * 0.18, 0, 6.2832)
            cr.fill()
            return

        if HEARTBEAT_STATIC:
            # Static red dot with mild glow — no animation
            # Soft outer ring
            cr.set_source_rgba(self.color[0], self.color[1],
                               self.color[2], 0.2)
            cr.arc(cx, cy, self.size * 0.34, 0, 6.2832)
            cr.fill()
            # Mid ring
            cr.set_source_rgba(self.color[0], self.color[1],
                               self.color[2], 0.4)
            cr.arc(cx, cy, self.size * 0.25, 0, 6.2832)
            cr.fill()
            # Solid core
            cr.set_source_rgba(*self.color)
            cr.arc(cx, cy, self.size * 0.2, 0, 6.2832)
            cr.fill()
            return

        # Animated heartbeat (only if HEARTBEAT_STATIC == False)
        beat = (math.sin(self.t * 2) + 1) / 2
        beat2 = (math.sin(self.t * 2 + 0.6) + 1) / 2
        intensity = max(beat, beat2 * 0.7)

        for i, alpha_mult in enumerate([0.15, 0.25, 0.5]):
            r = self.size * (0.4 - i * 0.08) + intensity * (self.size * 0.15)
            cr.set_source_rgba(self.color[0], self.color[1],
                               self.color[2],
                               alpha_mult * (0.4 + intensity * 0.6))
            cr.arc(cx, cy, r, 0, 6.2832)
            cr.fill()

        cr.set_source_rgba(*self.color)
        cr.arc(cx, cy, self.size * 0.2, 0, 6.2832)
        cr.fill()


# ── RIPPLE BARS ─────────────────────────────────────────────────

class RippleBars(Gtk.DrawingArea):
    """Segmented bars with ripple animation when value changes."""

    def __init__(self, segments=28, height=8):
        super().__init__()
        self.segments = segments
        self.value = 0
        self.target = 0
        self.muted = False
        self.ripple_t = 0
        self._rippling = False
        self.set_content_height(height)
        self.set_hexpand(True)
        self.set_draw_func(self._draw)
        GLib.timeout_add(30, self._tick)

    def set_value(self, val, muted=False, animate=True):
        if val != self.target and animate:
            self.ripple_t = 0
            self._rippling = True
        self.target = val
        self.muted = muted
        self.queue_draw()

    def _tick(self):
        if abs(self.value - self.target) > 0.5:
            self.value += (self.target - self.value) * 0.25
            self.queue_draw()
        else:
            self.value = self.target

        if self._rippling:
            self.ripple_t += 0.08
            if self.ripple_t > 1.5:
                self._rippling = False
                self.ripple_t = 0
            self.queue_draw()
        return True

    def _draw(self, area, cr, w, h):
        gap = 3
        seg_w = (w - gap * (self.segments - 1)) / self.segments
        active = (self.value / 100) * self.segments

        for i in range(self.segments):
            x = i * (seg_w + gap)

            if self.muted:
                cr.set_source_rgba(0.16, 0.16, 0.16, 1)
            elif i < int(active):
                if self._rippling:
                    wave_pos = self.ripple_t * self.segments
                    dist = abs(i - wave_pos)
                    if dist < 3:
                        boost = (1 - dist / 3) * 0.4
                        cr.set_source_rgba(
                            min(1, 0.84 + boost),
                            min(1, 0.19 + boost * 0.5),
                            min(1, 0.19 + boost * 0.5),
                            1
                        )
                    else:
                        cr.set_source_rgba(0.84, 0.19, 0.19, 1)
                else:
                    cr.set_source_rgba(0.84, 0.19, 0.19, 1)
            elif i < active:
                frac = active - int(active)
                cr.set_source_rgba(0.84 * frac + 0.11 * (1 - frac),
                                   0.19 * frac + 0.11 * (1 - frac),
                                   0.19 * frac + 0.11 * (1 - frac), 1)
            else:
                cr.set_source_rgba(0.11, 0.11, 0.11, 1)
            cr.rectangle(x, 0, seg_w, h)
            cr.fill()


# ── REVEAL OVERLAY ──────────────────────────────────────────────

class RevealOverlay(Gtk.DrawingArea):
    """Dot-cascade reveal animation when window opens."""

    def __init__(self):
        super().__init__()
        self.t = 0.0
        self._playing = False
        self.set_can_target(False)
        self.set_draw_func(self._draw)
        self.set_hexpand(True)
        self.set_vexpand(True)

    def play(self):
        if PULSE_DISABLED:
            # Skip dramatic reveal too — keep things calm
            return
        self.t = 0.0
        self._playing = True
        self.queue_draw()
        GLib.timeout_add(16, self._tick)

    def _tick(self):
        if not self._playing:
            return False
        self.t += 0.06
        if self.t > 1.2:
            self._playing = False
            self.queue_draw()
            return False
        self.queue_draw()
        return True

    def _draw(self, area, cr, w, h):
        if not self._playing:
            return
        spacing = 14
        dot_radius = 2
        progress = self.t / 1.2
        wave_y = h - progress * (h + 100)

        for row_y in range(0, h, spacing):
            for col_x in range(0, w, spacing):
                dist = row_y - wave_y
                if dist > -30 and dist < 60:
                    intensity = 1 - abs(dist - 15) / 45
                    intensity = max(0, intensity)
                    alpha = intensity * 0.6 * (1 - progress)
                    if alpha > 0.02:
                        cr.set_source_rgba(0.84, 0.19, 0.19, alpha)
                        cr.arc(col_x, row_y, dot_radius, 0, 6.2832)
                        cr.fill()


# ── FADE / STAGGER HELPERS ──────────────────────────────────────

def fade_in_widget(widget, duration_ms=200, delay_ms=0):
    """Animate widget opacity 0 -> 1."""
    widget.set_opacity(0)

    def start():
        steps = 16
        interval = duration_ms // steps
        step = [0]

        def tick():
            step[0] += 1
            t = step[0] / steps
            eased = 1 - (1 - t) ** 3
            widget.set_opacity(eased)
            if step[0] >= steps:
                widget.set_opacity(1)
                return False
            return True

        GLib.timeout_add(interval, tick)
        return False

    if delay_ms > 0:
        GLib.timeout_add(delay_ms, start)
    else:
        start()


def stagger_children(container, base_delay=0, step_delay=40, duration=200):
    """Fade in all direct children of a container with staggered delay."""
    child = container.get_first_child()
    i = 0
    while child:
        fade_in_widget(child, duration_ms=duration,
                       delay_ms=base_delay + i * step_delay)
        child = child.get_next_sibling()
        i += 1


# ── COMMON CSS ──────────────────────────────────────────────────

SHARED_CSS = """
window.popup-window { background: #080808; }
.outer-wrap { background: #080808; padding: 0; }

.root-box {
    background: #080808;
    border: 1px solid #1F1F1F;
    border-radius: 0;
    box-shadow: none;
}

/* HEADER */
.window-title {
    font-family: "NDot 55", "JetBrains Mono", monospace;
    font-weight: 800;
    font-size: 32px;
    color: #E8E6E3;
    letter-spacing: 6px;
}
.window-title.long {
    font-size: 22px;
    letter-spacing: 3px;
}

.title-accent {
    background: linear-gradient(to right,
        #D63030 0%, #D63030 40px,
        #1F1F1F 40px, #1F1F1F 100%);
    min-height: 2px;
}

/* SECTIONS */
.section-header { margin-top: 2px; margin-bottom: 4px; }
.section-bullet {
    font-family: monospace;
    font-size: 8px;
    color: #D63030;
}
.section-label {
    font-family: "NDot 55", "JetBrains Mono", monospace;
    font-size: 11px;
    color: #E8E6E3;
    font-weight: 700;
    letter-spacing: 4px;
}
.section-line {
    background: linear-gradient(to right, transparent, #1F1F1F);
}

/* DIVIDER */
.div-line {
    background: linear-gradient(to right, transparent, #1A1A1A, transparent);
    min-height: 1px;
}
.div-diamond {
    font-family: monospace;
    font-size: 7px;
    color: #D63030;
}

/* CARD */
.volume-card {
    background: #0C0C0C;
    border: 1px solid #1A1A1A;
    border-radius: 14px;
    padding: 16px 18px;
    transition: all 200ms ease;
}
.volume-card:hover { border-color: #2A2A2A; background: #0E0E0E; }
.volume-card.muted { background: #0A0606; border-color: #1A0808; }

/* ICON BUTTON */
.icon-btn {
    background: #060606;
    border: 1px solid #242424;
    color: #D63030;
    font-family: "NDot 55", "JetBrains Mono", monospace;
    font-size: 18px;
    font-weight: 700;
    border-radius: 12px;
    padding: 0;
    min-width: 46px;
    min-height: 46px;
    transition: all 150ms ease;
}
.icon-btn:hover {
    background: #120606;
    border-color: #D63030;
    color: #FF4040;
}
.icon-btn.muted {
    color: #4A4A4A;
    border-color: #1F0A0A;
    background: #0A0303;
}

/* LABELS */
.row-label {
    font-family: "NDot 55", "JetBrains Mono", monospace;
    font-size: 12px;
    font-weight: 700;
    color: #E8E6E3;
    letter-spacing: 3px;
}
.row-status {
    font-family: "JetBrains Mono", monospace;
    font-size: 9px;
    color: #666666;
    letter-spacing: 2px;
    font-weight: 600;
}
.volume-card.muted .row-label { color: #5A5A5A; }
.volume-card.muted .row-status { color: #D63030; }

/* DEVICE ROW */
.device-row {
    background: #0A0A0A;
    border: 1px solid #161616;
    border-radius: 10px;
    padding: 10px 14px;
    min-height: 26px;
    transition: all 150ms ease;
}
.device-row:hover { background: #111111; border-color: #242424; }
.device-row.active { background: #0E0606; border-color: #3A1010; }
.device-row.active:hover { background: #140909; border-color: #4A1515; }

.device-dot {
    font-family: monospace;
    font-size: 8px;
    color: #2A2A2A;
}
.device-row.active .device-dot {
    color: #D63030;
    text-shadow: 0 0 6px rgba(214, 48, 48, 0.7);
}
.device-name {
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    color: #888888;
    letter-spacing: 0.3px;
}
.device-row.active .device-name { color: #E8E6E3; font-weight: 600; }
.device-row:hover .device-name { color: #D0D0D0; }

.device-active-tag {
    font-family: "JetBrains Mono", monospace;
    font-size: 8px;
    color: #D63030;
    font-weight: 800;
    letter-spacing: 2px;
    background: rgba(214, 48, 48, 0.1);
    border: 1px solid rgba(214, 48, 48, 0.3);
    border-radius: 3px;
    padding: 2px 5px;
}
.device-paired-tag {
    font-family: "JetBrains Mono", monospace;
    font-size: 8px;
    color: #666666;
    font-weight: 700;
    letter-spacing: 2px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid #2A2A2A;
    border-radius: 3px;
    padding: 2px 5px;
}

.empty-label {
    font-family: "JetBrains Mono", monospace;
    font-size: 10px;
    color: #3A3A3A;
    letter-spacing: 2px;
    font-weight: 600;
}

/* SCROLLBAR */
scrollbar { background: transparent; border: none; padding: 0; }
scrollbar slider {
    background: #1A1A1A;
    border-radius: 4px;
    min-width: 4px;
    min-height: 30px;
    margin: 2px;
}
scrollbar slider:hover { background: #D63030; }
scrollbar trough { background: transparent; border: none; }
"""


# ── COMMON HEADER BUILDERS ──────────────────────────────────────

def build_header(title, long=False, indicator_active=True):
    """Returns (header_box, indicator_widget)."""
    header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    header.set_margin_top(20)
    header.set_margin_bottom(2)
    header.set_margin_start(22)
    header.set_margin_end(22)
    header.set_valign(Gtk.Align.END)

    title_lbl = Gtk.Label(label=title, xalign=0)
    title_lbl.add_css_class('window-title')
    if long:
        title_lbl.add_css_class('long')
    header.append(title_lbl)

    spacer = Gtk.Box()
    spacer.set_hexpand(True)
    header.append(spacer)

    indicator = HeartbeatDot(size=14, color=Color.RED,
                             active=indicator_active)
    indicator.set_valign(Gtk.Align.END)
    indicator.set_margin_bottom(10)
    header.append(indicator)

    return header, indicator


def build_accent_bar():
    accent = Gtk.Box()
    accent.add_css_class('title-accent')
    accent.set_margin_start(22)
    accent.set_margin_end(22)
    accent.set_margin_top(6)
    accent.set_margin_bottom(14)
    accent.set_size_request(-1, 1)
    return accent


def build_section_header(text):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    box.add_css_class('section-header')

    bullet = Gtk.Label(label='■')
    bullet.add_css_class('section-bullet')
    box.append(bullet)

    lbl = Gtk.Label(label=text.upper(), xalign=0)
    lbl.add_css_class('section-label')
    box.append(lbl)

    spacer = Gtk.Box()
    spacer.set_hexpand(True)
    box.append(spacer)

    line = Gtk.Box()
    line.add_css_class('section-line')
    line.set_size_request(80, 1)
    line.set_valign(Gtk.Align.CENTER)
    box.append(line)

    return box


def build_divider():
    wrap = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    wrap.set_margin_top(6)
    wrap.set_margin_bottom(2)

    line1 = Gtk.Box()
    line1.add_css_class('div-line')
    line1.set_hexpand(True)
    line1.set_valign(Gtk.Align.CENTER)
    line1.set_size_request(-1, 1)
    wrap.append(line1)

    diamond = Gtk.Label(label='◆')
    diamond.add_css_class('div-diamond')
    wrap.append(diamond)

    line2 = Gtk.Box()
    line2.add_css_class('div-line')
    line2.set_hexpand(True)
    line2.set_valign(Gtk.Align.CENTER)
    line2.set_size_request(-1, 1)
    wrap.append(line2)

    return wrap
