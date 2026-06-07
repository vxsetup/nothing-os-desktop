"""
Nothing OS — Shared style system
All Nothing modules import CSS from here.
Any change in one place applies everywhere.
"""

import os
from gi.repository import Gtk, Gdk, GLib


# ═══════════════════════════════════════════════════════════
#  DESIGN TOKENS — единственный источник правды
# ═══════════════════════════════════════════════════════════

# Colors
TOKENS = {
    # Brand
    'accent':           '#FF2D2D',
    'accent_hover':     '#FF4747',
    'accent_subtle':    'rgba(255, 45, 45, 0.06)',
    'accent_subtle_2':  'rgba(255, 45, 45, 0.10)',
    'accent_subtle_3':  'rgba(255, 45, 45, 0.16)',
    'accent_border':    'rgba(255, 45, 45, 0.45)',

    # Surfaces
    'bg_primary':       '#0B0B0C',
    'bg_secondary':     '#0E0E10',
    'bg_card':          'rgba(255, 255, 255, 0.025)',
    'bg_card_hover':    'rgba(255, 255, 255, 0.04)',
    'bg_hover':         'rgba(255, 255, 255, 0.04)',
    'bg_hover_strong':  'rgba(255, 255, 255, 0.06)',

    # Borders
    'border_subtle':    'rgba(255, 255, 255, 0.05)',
    'border_card':      'rgba(255, 255, 255, 0.04)',
    'border_hover':     'rgba(255, 255, 255, 0.10)',
    'border_focus':     'rgba(255, 45, 45, 0.50)',
    'border_divider':   'rgba(255, 255, 255, 0.045)',

    # Text
    'text_primary':     '#FFFFFF',
    'text_secondary':   '#C8C8CC',
    'text_tertiary':    '#8E8E93',
    'text_muted':       '#6E6E73',
    'text_disabled':    '#4A4A4F',
    'text_invisible':   '#3A3A3C',
    'text_accent':      '#FF2D2D',

    # Semantic
    'success':          '#30D158',
    'warning':          '#FFD60A',
    'error':            '#FF2D2D',

    # Radii
    'radius_window':    '20px',
    'radius_card':      '10px',
    'radius_button':    '6px',
    'radius_toggle':    '2px',
    'radius_small':     '4px',

    # Spacing
    'pad_card':         '20px',     # card horizontal margin
    'pad_section':      '28px',     # section header horizontal margin
    'pad_row':          '14px 16px',  # standard row padding

    # Fonts
    'font_sans':        '"Inter", "SF Pro Display", "Segoe UI", sans-serif',
    'font_mono':        '"JetBrains Mono", "IBM Plex Mono", monospace',
    'font_dot':         '"Ndot 55", "Ndot", "JetBrains Mono", monospace',

    # Animation
    'transition_fast':  '100ms ease',
    'transition_med':   '150ms ease',
    'transition_slow':  '250ms ease',
}


def t(key):
    """Token getter."""
    return TOKENS[key]


# ═══════════════════════════════════════════════════════════
#  SHARED CSS — included by every module
# ═══════════════════════════════════════════════════════════

SHARED_CSS = f"""
/* ════════════════════════════════════════════════════════
   Nothing OS — Shared style v1
   Applied to ALL Nothing modules. Override locally if needed.
   ════════════════════════════════════════════════════════ */

/* ─── Window base ──────────────────────────────────────── */

window.popup-window {{
    background: transparent;
}}

window.popup-window.background,
window.popup-window > * {{
    background: transparent;
    background-color: transparent;
}}

.outer-wrap {{
    background: transparent;
    padding: 0;
}}

/* ─── Card scroller (rounded clip container) ─────────── */

.card-scroller {{
    background: {t('bg_primary')};
    border-radius: {t('radius_window')};
    border: 1px solid {t('border_subtle')};
}}

.main-card {{
    background: transparent;
    border: none;
    border-radius: 0;
}}

/* Hide scrollbar in scroller */
.card-scroller scrollbar,
.card-scroller scrollbar.vertical,
.card-scroller scrollbar.horizontal,
.card-scroller scrollbar slider {{
    background: transparent;
    border: none;
    min-width: 0;
    min-height: 0;
    opacity: 0;
    -gtk-icon-size: 0;
}}

.card-scroller undershoot,
.card-scroller overshoot {{
    background: none;
    box-shadow: none;
}}

/* ─── Typography — unified ─────────────────────────────── */

.window-title {{
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 11px;
    color: {t('text_muted')};
    letter-spacing: 3px;
}}

.hero-status {{
    font-family: {t('font_mono')};
    font-weight: 600;
    font-size: 11px;
    color: {t('text_secondary')};
    letter-spacing: 2px;
}}

.hero-sub {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 10px;
    color: {t('text_muted')};
    letter-spacing: 1px;
    margin-top: 2px;
}}

.section-header {{
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 10px;
    color: {t('text_muted')};
    letter-spacing: 2px;
}}

.section-subheader {{
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 9px;
    color: {t('text_disabled')};
    letter-spacing: 2px;
}}

.section-counter {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 10px;
    color: {t('text_accent')};
    letter-spacing: 1px;
}}

/* ─── Group card (sections grouping) ──────────────────── */

.group-card {{
    background: {t('bg_card')};
    border: 1px solid {t('border_card')};
    border-radius: {t('radius_card')};
}}

.row-divider {{
    background: {t('border_divider')};
    min-height: 1px;
}}

/* ─── List rows — unified ──────────────────────────────── */

.list-row {{
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 12px 16px;
    min-height: 28px;
    box-shadow: none;
    transition: background {t('transition_fast')};
}}

.list-row:hover {{
    background: {t('bg_hover')};
}}

.list-row.active {{
    background: {t('accent_subtle')};
}}

.list-row.active:hover {{
    background: {t('accent_subtle_2')};
}}

/* ─── Row text styles ──────────────────────────────────── */

.row-name {{
    font-family: {t('font_sans')};
    font-weight: 500;
    font-size: 14px;
    color: {t('text_primary')};
    letter-spacing: -0.1px;
}}

.row-secondary {{
    font-family: {t('font_sans')};
    font-weight: 400;
    font-size: 11px;
    color: {t('text_tertiary')};
    margin-top: 1px;
}}

.row-mac {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 9px;
    color: {t('text_disabled')};
    letter-spacing: 1px;
}}

.list-row.active .row-mac {{
    color: {t('text_muted')};
}}

.row-status {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 9px;
    color: {t('text_muted')};
    letter-spacing: 1.5px;
}}

.list-row.active .row-status {{
    color: {t('text_accent')};
}}

.row-action {{
    font-family: {t('font_mono')};
    font-weight: 600;
    font-size: 9px;
    color: {t('text_tertiary')};
    letter-spacing: 1.5px;
}}

.list-row:hover .row-action {{
    color: {t('text_primary')};
}}

.list-row.active .row-action {{
    color: {t('text_accent')};
}}

.row-battery {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 9px;
    color: {t('text_tertiary')};
    letter-spacing: 0.5px;
}}

/* ─── Adapter row (for items in adapter sections) ────── */

.adapter-label {{
    font-family: {t('font_sans')};
    font-weight: 500;
    font-size: 13px;
    color: {t('text_primary')};
    letter-spacing: 0.1px;
}}

/* ─── Close button ─────────────────────────────────────── */

.close-btn {{
    background: transparent;
    border: 1px solid {t('border_hover')};
    border-radius: {t('radius_button')};
    padding: 0;
    min-width: 26px;
    min-height: 26px;
    margin-left: 10px;
    font-family: {t('font_sans')};
    font-size: 16px;
    font-weight: 400;
    color: {t('text_tertiary')};
    transition: all {t('transition_fast')};
}}

.close-btn:hover {{
    background: {t('accent_subtle_2')};
    border-color: {t('accent_border')};
    color: {t('text_accent')};
}}

/* ─── Dismiss button (smaller) ─────────────────────────── */

.dismiss-btn {{
    background: transparent;
    border: 1px solid {t('border_hover')};
    border-radius: {t('radius_small')};
    padding: 0;
    min-width: 22px;
    min-height: 22px;
    font-family: {t('font_sans')};
    font-size: 12px;
    color: {t('text_muted')};
    transition: all {t('transition_fast')};
}}

.dismiss-btn:hover {{
    background: {t('accent_subtle_2')};
    border-color: {t('accent_border')};
    color: {t('text_accent')};
}}

/* ─── Standard buttons ─────────────────────────────────── */

.action-btn {{
    background: transparent;
    border: 1px solid {t('border_hover')};
    border-radius: {t('radius_button')};
    padding: 6px 14px;
    font-family: {t('font_sans')};
    font-size: 10px;
    font-weight: 700;
    color: {t('text_secondary')};
    letter-spacing: 1.5px;
    transition: all {t('transition_fast')};
}}

.action-btn:hover {{
    background: {t('bg_hover')};
    border-color: rgba(255, 255, 255, 0.25);
    color: {t('text_primary')};
}}

.action-btn-accent {{
    background: {t('accent')};
    border-color: {t('accent')};
    color: {t('text_primary')};
}}

.action-btn-accent:hover {{
    background: {t('accent_hover')};
    border-color: {t('accent_hover')};
}}

.action-btn-danger {{
    background: transparent;
    border-color: {t('accent_border')};
    color: #FF6B6B;
}}

.action-btn-danger:hover {{
    background: {t('accent_subtle_2')};
    border-color: {t('accent')};
    color: {t('text_primary')};
}}

/* ─── Wide action button (full-width) ──────────────────── */

.action-btn-wide {{
    background: {t('bg_hover')};
    border: 1px solid {t('border_hover')};
    border-radius: 8px;
    padding: 10px 0;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 10px;
    color: {t('text_secondary')};
    letter-spacing: 2px;
    transition: all {t('transition_fast')};
}}

.action-btn-wide:hover {{
    background: {t('bg_hover_strong')};
    border-color: rgba(255, 255, 255, 0.16);
    color: {t('text_primary')};
}}

.action-btn-wide-active {{
    background: {t('accent_subtle_2')};
    border-color: {t('accent_border')};
    color: #FF6B6B;
}}

.action-btn-wide-active:hover {{
    background: {t('accent_subtle_3')};
    border-color: {t('accent')};
    color: {t('text_primary')};
}}

/* ─── Big primary action button (CAPTURE / START) ─────── */

.action-btn-big {{
    background: {t('accent')};
    border: 1px solid {t('accent')};
    border-radius: 10px;
    padding: 14px 0;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 12px;
    color: {t('text_primary')};
    letter-spacing: 3px;
    transition: all {t('transition_fast')};
}}

.action-btn-big:hover {{
    background: {t('accent_hover')};
    border-color: {t('accent_hover')};
}}

.action-btn-big-secondary {{
    background: {t('bg_hover')};
    border: 1px solid {t('border_hover')};
    border-radius: 10px;
    padding: 14px 0;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 12px;
    color: {t('text_primary')};
    letter-spacing: 3px;
    transition: all {t('transition_fast')};
}}

.action-btn-big-secondary:hover {{
    background: {t('bg_hover_strong')};
    border-color: rgba(255, 255, 255, 0.20);
}}

/* ─── Nav buttons (‹ › TODAY) ──────────────────────────── */

.nav-btn {{
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: {t('radius_button')};
    padding: 4px 10px;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 10px;
    color: {t('text_secondary')};
    letter-spacing: 1.5px;
    transition: all {t('transition_fast')};
}}

.nav-btn:hover {{
    background: {t('bg_hover')};
    border-color: rgba(255, 255, 255, 0.16);
    color: {t('text_primary')};
}}

.nav-btn-accent {{
    background: {t('accent_subtle_2')};
    border-color: {t('accent_border')};
    color: #FF6B6B;
}}

.nav-btn-accent:hover {{
    background: {t('accent_subtle_3')};
    border-color: {t('accent')};
    color: {t('text_primary')};
}}

/* ─── Text entry ───────────────────────────────────────── */

.text-entry,
.search-entry {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    color: {t('text_primary')};
    padding: 10px 12px;
    font-family: {t('font_sans')};
    font-size: 13px;
    font-weight: 400;
    transition: border-color {t('transition_fast')};
}}

.text-entry:focus,
.search-entry:focus {{
    border-color: {t('border_focus')};
    background: {t('bg_hover')};
    outline: none;
    box-shadow: none;
}}

.text-entry placeholder,
.search-entry placeholder {{
    color: #5A5A5F;
}}

/* ─── Password entry ───────────────────────────────────── */

.pwd-entry {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    color: {t('text_primary')};
    padding: 8px 10px;
    font-family: {t('font_mono')};
    font-size: 12px;
}}

.pwd-entry:focus {{
    border-color: {t('border_focus')};
}}

/* ─── Spin button ──────────────────────────────────────── */

.num-spin {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    color: {t('text_primary')};
    padding: 4px 6px;
    font-family: {t('font_mono')};
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.num-spin:focus {{
    border-color: {t('accent_border')};
}}

.num-spin button {{
    background: transparent;
    color: {t('text_tertiary')};
    border: none;
    padding: 2px 6px;
}}

.num-spin button:hover {{
    color: {t('text_accent')};
    background: {t('accent_subtle_2')};
}}

.spin-sep {{
    font-family: {t('font_mono')};
    font-size: 14px;
    color: {t('text_disabled')};
    font-weight: 700;
    padding: 0 4px;
}}

/* ─── Chip button ──────────────────────────────────────── */

.chip-btn {{
    background: {t('bg_hover')};
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 6px 10px;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 9px;
    color: {t('text_secondary')};
    letter-spacing: 1px;
    transition: all {t('transition_fast')};
}}

.chip-btn:hover {{
    background: {t('accent_subtle_2')};
    border-color: {t('accent_border')};
    color: #FF6B6B;
}}

/* ─── Empty label ──────────────────────────────────────── */

.empty-label {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 10px;
    color: {t('text_invisible')};
    letter-spacing: 2px;
}}

/* ─── Toast (in-card notification) ─────────────────────── */

.toast {{
    font-family: {t('font_mono')};
    font-size: 10px;
    color: {t('text_accent')};
    background: {t('accent_subtle')};
    border: 1px solid rgba(255, 45, 45, 0.3);
    border-radius: 6px;
    padding: 8px 12px;
    letter-spacing: 1px;
}}

/* ─── Tooltip ──────────────────────────────────────────── */

tooltip {{
    background: {t('bg_primary')};
    border: 1px solid {t('border_hover')};
    border-radius: 10px;
    padding: 10px 14px;
}}

tooltip label {{
    color: {t('text_secondary')};
    font-family: {t('font_sans')};
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 0.1px;
}}

/* ─── Hint label (small help text) ─────────────────────── */

.hint-label {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 8px;
    color: {t('text_disabled')};
    letter-spacing: 2px;
}}

/* ─── Slider value display ─────────────────────────────── */

.slider-val {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 11px;
    color: {t('text_secondary')};
    letter-spacing: 0.5px;
    min-width: 28px;
}}

/* ─── System buttons (LOCK / SETTINGS / POWER row) ─────── */

.system-btn {{
    background: {t('bg_card')};
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 0;
    transition: all 120ms ease;
}}

.system-btn:hover {{
    background: {t('bg_hover')};
    border-color: rgba(255, 255, 255, 0.12);
}}

.system-btn-label {{
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 9px;
    color: {t('text_secondary')};
    letter-spacing: 1.5px;
}}

.system-btn:hover .system-btn-label {{
    color: {t('text_primary')};
}}

/* ─── Power menu rows ──────────────────────────────────── */

.power-row {{
    background: transparent;
    border: none;
    border-bottom: 1px solid {t('border_card')};
    border-radius: 0;
    padding: 0;
    transition: background {t('transition_fast')};
}}

.power-row:hover {{
    background: rgba(255, 255, 255, 0.03);
}}

.power-row-danger:hover {{
    background: {t('accent_subtle')};
}}

.power-row-label {{
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 12px;
    color: {t('text_primary')};
    letter-spacing: 2px;
}}

.power-row-danger .power-row-label {{
    color: {t('text_accent')};
}}

.power-row-arrow {{
    font-family: {t('font_sans')};
    font-size: 16px;
    color: {t('text_muted')};
    padding-right: 4px;
}}

.power-row:hover .power-row-arrow {{
    color: {t('text_primary')};
}}

.power-row-danger:hover .power-row-arrow {{
    color: {t('text_accent')};
}}

/* ─── Event time/date (calendar) ───────────────────────── */

.event-time {{
    font-family: {t('font_mono')};
    font-weight: 700;
    font-size: 13px;
    color: {t('text_primary')};
    letter-spacing: 0.5px;
}}

.event-date {{
    font-family: {t('font_mono')};
    font-weight: 500;
    font-size: 9px;
    color: {t('text_accent')};
    letter-spacing: 1px;
}}

/* ─── Notification card ────────────────────────────────── */

.notif-card {{
    background: {t('bg_card')};
    border: 1px solid {t('border_card')};
    border-radius: {t('radius_card')};
    transition: background {t('transition_fast')},
                border-color {t('transition_fast')};
}}

.notif-card:hover {{
    background: {t('bg_card_hover')};
    border-color: rgba(255, 255, 255, 0.07);
}}

.notif-body {{
    font-family: {t('font_sans')};
    font-weight: 400;
    font-size: 11px;
    color: {t('text_tertiary')};
    margin-top: 2px;
}}

/* ─── Action pills (inline action buttons in notifications) ─ */

.action-pill {{
    background: {t('bg_hover')};
    border: 1px solid {t('border_hover')};
    border-radius: 6px;
    padding: 6px 14px;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 10px;
    color: {t('text_secondary')};
    letter-spacing: 1.5px;
    min-height: 0;
    transition: all {t('transition_fast')};
}}

.action-pill:hover {{
    background: {t('bg_hover_strong')};
    border-color: rgba(255, 255, 255, 0.20);
    color: {t('text_primary')};
}}

.action-pill-accent {{
    background: {t('accent_subtle_2')};
    border: 1px solid {t('accent_border')};
    border-radius: 6px;
    padding: 6px 14px;
    font-family: {t('font_sans')};
    font-weight: 700;
    font-size: 10px;
    color: #FF6B6B;
    letter-spacing: 1.5px;
    min-height: 0;
    transition: all {t('transition_fast')};
}}

.action-pill-accent:hover {{
    background: {t('accent_subtle_3')};
    border-color: {t('accent')};
    color: {t('text_primary')};
}}

/* ─── Preview / device list ────────────────────────────── */

.preview-box {{
    background: rgba(0, 0, 0, 0.35);
    border-radius: {t('radius_button')};
}}

/* ─── Layer-shell popup fix (no shadow bleed) ──────────── */

window.popup-window decoration,
window.popup-window > decoration,
window.popup-window.solid-csd,
window.popup-window.csd {{
    background: transparent;
    box-shadow: none;
    border: none;
    margin: 0;
    padding: 0;
}}
"""


def install_css(extra_css=''):
    """
    Install shared CSS + optional module-specific CSS.
    Call this once in do_startup() of each module's Application.
    """
    provider = Gtk.CssProvider()
    css = SHARED_CSS + '\n\n' + extra_css
    provider.load_from_data(css.encode())
    display = Gdk.Display.get_default()
    if display:
        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
    return provider


# ═══════════════════════════════════════════════════════════
#  Animation helpers (fade + slide on open/close)
# ═══════════════════════════════════════════════════════════

def fade_in(widget, duration_ms=180):
    """Fade widget in from opacity 0 → 1."""
    widget.set_opacity(0.0)
    widget.set_visible(True)

    steps = max(1, duration_ms // 16)
    step_delta = 1.0 / steps

    def tick():
        op = widget.get_opacity()
        new_op = op + step_delta
        if new_op >= 1.0:
            widget.set_opacity(1.0)
            return False
        widget.set_opacity(new_op)
        return True

    GLib.timeout_add(16, tick)


def fade_out(widget, duration_ms=140, on_done=None):
    """Fade widget out and optionally call on_done."""
    steps = max(1, duration_ms // 16)
    step_delta = 1.0 / steps

    def tick():
        op = widget.get_opacity()
        new_op = op - step_delta
        if new_op <= 0.0:
            widget.set_opacity(0.0)
            widget.set_visible(False)
            if on_done:
                on_done()
            return False
        widget.set_opacity(new_op)
        return True

    GLib.timeout_add(16, tick)
