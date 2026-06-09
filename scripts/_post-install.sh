#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Post-install tasks
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# ─── Enable systemd services ────────────────────────────────

section "Enabling services"

# NetworkManager
if systemctl list-unit-files NetworkManager.service &>/dev/null 2>&1; then
    sudo systemctl enable --now NetworkManager.service &>/dev/null || true
    ok "NetworkManager enabled"
fi

# Bluetooth
if systemctl list-unit-files bluetooth.service &>/dev/null 2>&1; then
    sudo systemctl enable --now bluetooth.service &>/dev/null || true
    ok "Bluetooth enabled"
fi

# PipeWire user services
systemctl --user enable --now pipewire.service &>/dev/null || true
systemctl --user enable --now pipewire-pulse.service &>/dev/null || true
systemctl --user enable --now wireplumber.service &>/dev/null || true
ok "PipeWire services enabled"

# ─── Set cursor theme ────────────────────────────────────────

section "Cursor theme"

if [[ -d /usr/share/icons/Bibata-Modern-Classic ]]; then
    mkdir -p "$HOME/.icons/default"
    cat > "$HOME/.icons/default/index.theme" 2>/dev/null <<EOF || true
[Icon Theme]
Name=Default
Comment=Default Cursor Theme
Inherits=Bibata-Modern-Classic
EOF
    ok "Bibata cursor theme set"
else
    info "Bibata cursor not installed — using default"
fi

# ─── Set fish as default shell ───────────────────────────────

section "Default shell"

if has_cmd fish; then
    current_shell="$(getent passwd "$USER" | cut -d: -f7)"
    fish_bin="$(command -v fish)"

    if [[ "$current_shell" != "$fish_bin" ]]; then
        # Ensure fish is in /etc/shells
        if ! grep -qx "$fish_bin" /etc/shells 2>/dev/null; then
            echo "$fish_bin" | sudo tee -a /etc/shells >/dev/null
        fi
        if sudo chsh -s "$fish_bin" "$USER" 2>/dev/null; then
            ok "Default shell changed to fish"
        else
            warn "Failed to change shell — run manually: chsh -s $fish_bin"
        fi
    else
        ok "fish already default shell"
    fi

    # Add starship init if not present
    fish_config="$HOME/.config/fish/config.fish"
    if [[ -f "$fish_config" ]] && has_cmd starship; then
        if ! grep -q "starship init" "$fish_config"; then
            echo "" >> "$fish_config"
            echo "# Starship prompt" >> "$fish_config"
            echo "starship init fish | source" >> "$fish_config"
            ok "Starship init added to fish config"
        fi
    fi
else
    warn "fish not installed"
fi

# ─── Generate wallpapers ────────────────────────────────────

section "Wallpapers"

if has_cmd nothing-wallpaper-gen; then
    WP_DIR="$HOME/Pictures/wallpapers"
    mkdir -p "$WP_DIR"

    if [[ ! -f "$WP_DIR/glyph.png" ]]; then
        nothing-wallpaper-gen --output "$WP_DIR/glyph.png" \
                              --variant glyph --palette dark &>/dev/null || true
        ok "Generated glyph.png"
    fi

    if [[ ! -f "$WP_DIR/minimal.png" ]]; then
        nothing-wallpaper-gen --output "$WP_DIR/minimal.png" \
                              --variant minimal --palette dark &>/dev/null || true
        ok "Generated minimal.png"
    fi

    if [[ ! -f "$WP_DIR/concentric.png" ]]; then
        nothing-wallpaper-gen --output "$WP_DIR/concentric.png" \
                              --variant concentric --palette dark &>/dev/null || true
        ok "Generated concentric.png"
    fi
else
    info "nothing-wallpaper-gen not available — skipping wallpaper generation"
fi

# ─── Font cache ──────────────────────────────────────────────

section "Font cache"

if has_cmd fc-cache; then
    fc-cache -f "$HOME/.local/share/fonts" &>/dev/null || true
    ok "Font cache refreshed"
fi

# ─── Create state directories ────────────────────────────────

section "State directories"

STATE_DIRS=(
    "$HOME/.local/state/nothing-os"
    "$HOME/.local/state/nothing-control"
    "$HOME/.local/state/nothing-notifications"
    "$HOME/.local/state/nothing-launcher"
    "$HOME/.local/share/nothing-calendar"
)

for d in "${STATE_DIRS[@]}"; do
    mkdir -p "$d"
done
ok "State directories created"

# ─── Reload if running ───────────────────────────────────────

section "Reload"

if pgrep -x Hyprland &>/dev/null && has_cmd hyprctl; then
    hyprctl reload &>/dev/null || true
    ok "Hyprland config reloaded"
else
    info "Hyprland not running — will load on next session"
fi

if pgrep -x waybar &>/dev/null; then
    pkill waybar 2>/dev/null || true
    sleep 0.5
    nohup waybar &>/dev/null &
    disown 2>/dev/null || true
    ok "Waybar restarted"
fi

if pgrep -x mako &>/dev/null; then
    makoctl reload &>/dev/null || true
    ok "Mako reloaded"
fi
