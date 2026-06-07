"""
Nothing OS — Notification helper
Unified interface wrapping notify-send with extras like actions and listening.
"""

import os
import subprocess
import threading
import time
import shutil
import re


def _has_notify_send():
    return shutil.which('notify-send') is not None


def _build_cmd(summary, body='', app='nothing-os', icon=None,
               urgency='normal', timeout=4000, actions=None,
               replace_id=None):
    """Construct notify-send arguments."""
    cmd = ['notify-send']

    # App name
    if app:
        cmd += ['-a', app]

    # Icon
    if icon:
        cmd += ['-i', str(icon)]

    # Urgency: low / normal / critical
    if urgency in ('low', 'normal', 'critical'):
        cmd += ['-u', urgency]

    # Timeout in ms
    if timeout is not None:
        cmd += ['-t', str(int(timeout))]

    # Actions — list of (key, label) tuples
    # notify-send adds them via -A key=label
    if actions:
        for key, label in actions:
            cmd += ['-A', f'{key}={label}']

    # Return ID via stdout (for listening to actions)
    if actions:
        cmd += ['-p']  # print id

    # Replace existing notification
    if replace_id is not None:
        cmd += ['-r', str(replace_id)]

    cmd += [str(summary)]
    if body:
        cmd += [str(body)]

    return cmd


def notify(summary, body='', app='nothing-os', icon=None,
           urgency='normal', timeout=4000, actions=None,
           replace_id=None):
    """
    Send a notification.
    Returns notification ID (int) if actions were specified, else None.
    """
    if not _has_notify_send():
        return None

    cmd = _build_cmd(summary, body, app, icon, urgency, timeout,
                     actions, replace_id)
    try:
        if actions:
            # Need ID for action listening — capture stdout
            r = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=3)
            if r.returncode == 0 and r.stdout.strip():
                try:
                    return int(r.stdout.strip())
                except ValueError:
                    pass
            return None
        else:
            # Fire and forget
            subprocess.Popen(cmd,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             start_new_session=True)
            return None
    except Exception as e:
        print(f"[notify] error: {e}", flush=True)
        return None


def notify_success(summary, body='', app='nothing-os', icon=None,
                   timeout=3000):
    """Green-tinted notification (uses 'normal' urgency)."""
    return notify(summary, body, app=app,
                  icon=icon or 'emblem-ok',
                  urgency='normal', timeout=timeout)


def notify_error(summary, body='', app='nothing-os', icon=None,
                 timeout=5000):
    """Critical notification (red)."""
    return notify(summary, body, app=app,
                  icon=icon or 'dialog-error',
                  urgency='critical', timeout=timeout)


def notify_info(summary, body='', app='nothing-os', icon=None,
                timeout=2500):
    """Low-urgency informational notification."""
    return notify(summary, body, app=app,
                  icon=icon or 'dialog-information',
                  urgency='low', timeout=timeout)


def notify_warning(summary, body='', app='nothing-os', icon=None,
                   timeout=4000):
    """Warning notification."""
    return notify(summary, body, app=app,
                  icon=icon or 'dialog-warning',
                  urgency='normal', timeout=timeout)


def listen_for_action(notif_id, callback, timeout=15):
    """
    Wait for a user to click an action button on notification.
    Calls callback(action_key) when action invoked, or returns silently
    on timeout/dismiss.

    Uses dbus-monitor to watch ActionInvoked signal.
    """
    if notif_id is None or not callback:
        return
    if not shutil.which('dbus-monitor'):
        return

    def worker():
        try:
            proc = subprocess.Popen(
                ['dbus-monitor', '--session',
                 "interface='org.freedesktop.Notifications',"
                 "member='ActionInvoked'"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=1)

            start = time.monotonic()
            buffer = []
            target_id = str(notif_id)

            while time.monotonic() - start < timeout:
                line = proc.stdout.readline()
                if not line:
                    break

                buffer.append(line.strip())
                if len(buffer) > 6:
                    buffer.pop(0)

                # ActionInvoked signal looks like:
                #   signal sender=... member=ActionInvoked
                #   uint32 <id>
                #   string "<action_key>"
                if 'ActionInvoked' in line:
                    # Read next 2 lines: uint32 id + string action
                    nid_line = proc.stdout.readline().strip()
                    action_line = proc.stdout.readline().strip()

                    nid_match = re.search(r'uint32\s+(\d+)', nid_line)
                    action_match = re.search(r'string\s+"([^"]+)"',
                                              action_line)

                    if nid_match and action_match:
                        nid = nid_match.group(1)
                        action = action_match.group(1)
                        if nid == target_id:
                            try:
                                callback(action)
                            except Exception as e:
                                print(f"[notify] action cb: {e}",
                                      flush=True)
                            break

            proc.terminate()
        except Exception as e:
            print(f"[notify] listen error: {e}", flush=True)

    threading.Thread(target=worker, daemon=True).start()
