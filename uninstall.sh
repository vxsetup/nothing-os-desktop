#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Uninstaller
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/scripts/_common.sh"

confirm_uninstall() {
    cat <<'EOF'

  This will remove:
    · ~/.local/bin/nothing-*           (all helper scripts)
    · ~/.local/lib/nothing-os/         (Python modules)
    · /usr/share/plymouth/themes/nothing-os/  (boot theme)

  This will NOT touch:
    · ~/.config/hypr/                  (your Hyprland config)
    · ~/.config/waybar/                (your waybar config)
    · ~/.config/fish/                  (your fish config)
    · GTK themes
    · Wallpapers
    · Default shell (fish)

  To fully revert, restore from backup at ~/.config-backup-*/
  To change shell back: chsh -s /bin/bash

EOF
    if [[ "${NOTHING_AUTO_YES:-0}" != "1" ]]; then
        read -rp "$(prompt 'Continue? [y/N]: ')" answer
        [[ "$answer" =~ ^[Yy]$ ]] || die "Cancelled."
    fi
}

remove_bin() {
    section "Removing scripts from ~/.local/bin/"
    for f in "$HOME/.local/bin/"nothing-*; do
        [[ -f "$f" ]] && rm -f "$f" && ok "removed $(basename "$f")"
    done
}

remove_lib() {
    section "Removing ~/.local/lib/nothing-os/"
    if [[ -d "$HOME/.local/lib/nothing-os" ]]; then
        rm -rf "$HOME/.local/lib/nothing-os"
        ok "removed nothing-os/"
    fi
}

remove_plymouth() {
    section "Removing Plymouth theme"
    if [[ -d /usr/share/plymouth/themes/nothing-os ]]; then
        sudo rm -rf /usr/share/plymouth/themes/nothing-os
        sudo plymouth-set-default-theme -R bgrt 2>/dev/null || true
        ok "Plymouth theme removed"
    fi
}

stop_running() {
    section "Stopping running Nothing OS daemons"
    for p in nothing-glyph-wallpaper nothing-widgets; do
        pkill -f "$p" 2>/dev/null && ok "stopped $p" || true
    done
}

main() {
    info "Nothing OS Desktop — Uninstaller"
    confirm_uninstall
    stop_running
    remove_bin
    remove_lib
    remove_plymouth
    echo
    ok "Uninstall complete."
    info "Your backup is at: ~/.config-backup-*/"
}

main "$@"
