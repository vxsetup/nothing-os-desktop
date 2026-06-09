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
    · ~/.local/bin/nothing-*
    · ~/.local/lib/nothing-os/
    · Plymouth theme (if installed)

  This will NOT touch:
    · ~/.config/ (your configs)
    · Wallpapers
    · Fonts
    · Shell settings

  Restore from backup: ~/.config-backup-*/

EOF
    if [[ "${NOTHING_AUTO_YES:-0}" != "1" ]]; then
        read -rp "$(prompt 'Continue? [y/N]: ')" answer
        [[ "$answer" =~ ^[Yy]$ ]] || die "Cancelled."
    fi
}

stop_running() {
    section "Stopping daemons"
    for p in nothing-control nothing-volume nothing-network \
             nothing-bluetooth nothing-notifications nothing-calendar \
             nothing-launcher nothing-recorder nothing-screenshot \
             nothing-osd nothing-about nothing-workspaces; do
        pkill -f "$p" 2>/dev/null && ok "stopped $p" || true
    done
}

remove_bin() {
    section "Removing scripts"
    for f in "$HOME/.local/bin/"nothing-*; do
        [[ -f "$f" ]] && rm -f "$f" && ok "removed $(basename "$f")"
    done
}

remove_lib() {
    section "Removing Python modules"
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

main() {
    info "Nothing OS Desktop — Uninstaller"
    confirm_uninstall
    stop_running
    remove_bin
    remove_lib
    remove_plymouth
    echo
    ok "Uninstall complete."
    info "Restore configs from: ~/.config-backup-*/"
}

main "$@"
