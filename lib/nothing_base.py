import os
import sys

def ensure_layer_shell():
    lib_paths = [
        '/usr/lib/libgtk4-layer-shell.so',
        '/usr/lib64/libgtk4-layer-shell.so',
        '/usr/lib/x86_64-linux-gnu/libgtk4-layer-shell.so',
    ]

    lib = next((p for p in lib_paths if os.path.exists(p)), None)

    if lib and lib not in os.environ.get('LD_PRELOAD', ''):
        os.environ['LD_PRELOAD'] = lib + ':' + os.environ.get('LD_PRELOAD', '')
        os.execv(sys.executable, [sys.executable] + sys.argv)
