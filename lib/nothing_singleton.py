"""
Nothing OS — Single-popup behavior
When opening a Nothing app, close all other Nothing popups
to mimic real OS panel behavior.
"""

import subprocess
import os


# All Nothing OS namespaces we manage
NOTHING_NAMESPACES = {
    'nothing-bluetooth',
    'nothing-volume',
    'nothing-network',
    'nothing-control',
    'nothing-about',
    'nothing-notifications',
    'nothing-calendar',
    'nothing-recorder',
    'nothing-screenshot',
    'nothing-launcher',
}


def close_other_popups(self_namespace):
    """
    Close all Nothing popups except the one with given namespace.
    Uses hyprctl to dispatch close commands targeted at layer namespaces.
    """
    if not _has_hyprctl():
        return

    # Method 1: through hyprland clients/layers
    # Each Nothing popup has a unique application_id matching its namespace
    try:
        for ns in NOTHING_NAMESPACES:
            if ns == self_namespace:
                continue
            # Send a custom signal via IPC file so the running app hides itself
            _signal_hide(ns)
    except Exception as e:
        print(f"[singleton] close_other: {e}", flush=True)


def _has_hyprctl():
    try:
        subprocess.run(['which', 'hyprctl'], capture_output=True,
                       check=True, timeout=1)
        return True
    except Exception:
        return False


def _signal_hide(namespace):
    """
    Trigger 'hide' on a running Nothing app instance.
    Uses Gio.Application's command line interface via gapplication.
    """
    # The app_id pattern: tech.nothing.<name>
    name = namespace.replace('nothing-', '')
    app_id = f'tech.nothing.{name}'

    # Try gapplication first (cleanest — uses dbus activation)
    try:
        subprocess.Popen(
            ['gapplication', 'launch', app_id, '--', '--hide'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            timeout=1,
        )
        return
    except Exception:
        pass

    # Fallback: directly invoke the binary with --hide
    bin_path = os.path.expanduser(f'~/.local/bin/{namespace}')
    if os.path.exists(bin_path):
        try:
            subprocess.Popen(
                [bin_path, '--hide'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception:
            pass
