#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Backup existing configs
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$HOME/.config-backup-$TIMESTAMP"

DIRS_TO_BACKUP=(
    "hypr"
    "waybar"
    "mako"
    "kitty"
    "gtk-3.0"
    "gtk-4.0"
    "fish"
    "fastfetch"
)

FILES_TO_BACKUP=(
    "starship.toml"
)

mkdir -p "$BACKUP_DIR"

any_backed=0

for d in "${DIRS_TO_BACKUP[@]}"; do
    if [[ -e "$HOME/.config/$d" ]]; then
        cp -r "$HOME/.config/$d" "$BACKUP_DIR/"
        ok "backed up ~/.config/$d"
        any_backed=1
    fi
done

for f in "${FILES_TO_BACKUP[@]}"; do
    if [[ -e "$HOME/.config/$f" ]]; then
        cp "$HOME/.config/$f" "$BACKUP_DIR/"
        ok "backed up ~/.config/$f"
        any_backed=1
    fi
done

if [[ $any_backed -eq 0 ]]; then
    info "Nothing to back up — clean install."
    rmdir "$BACKUP_DIR" 2>/dev/null || true
else
    ok "Backup location: $BACKUP_DIR"
fi
