#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Installer
#  Arch Linux + Hyprland
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/scripts/_common.sh"

print_banner() {
    cat <<'EOF'

    ● ● ● ● ●
   ●         ●
  ●           ●
  ●           ●        N O T H I N G   O S
  ●     ●     ●        for desktop
  ●           ●
  ●           ●        v1.0 · MIT · Arch Linux + Hyprland
   ●         ●
    ● ● ● ● ●

EOF
}

check_arch() {
    if [[ ! -f /etc/arch-release ]]; then
        die "This installer requires Arch Linux."
    fi
    ok "Arch Linux detected"
}

check_not_root() {
    if [[ $EUID -eq 0 ]]; then
        die "Don't run as root. Script will sudo when needed."
    fi
    ok "Running as user: $USER"
}

check_wayland() {
    if [[ -z "${WAYLAND_DISPLAY:-}" ]] && \
       [[ "${XDG_SESSION_TYPE:-}" != "wayland" ]]; then
        warn "Wayland not active — OK for first install"
    else
        ok "Wayland session active"
    fi
}

check_compositor() {
    if ! pgrep -x Hyprland &>/dev/null; then
        warn "Hyprland not running — live reload will be skipped"
    else
        ok "Hyprland active"
    fi
}

confirm_install() {
    echo
    info "This installer will:"
    echo "  · Install Arch packages via pacman + yay"
    echo "  · Backup existing configs to ~/.config-backup-<timestamp>/"
    echo "  · Copy Nothing OS configs to ~/.config/"
    echo "  · Install scripts to ~/.local/bin/"
    echo "  · Install Python modules to ~/.local/lib/nothing-os/"
    echo "  · Set fish as default shell"
    echo "  · Install wallpapers to ~/Pictures/wallpapers/"
    echo
    if [[ "${NOTHING_AUTO_YES:-0}" != "1" ]]; then
        read -rp "$(prompt 'Continue? [y/N]: ')" answer
        [[ "$answer" =~ ^[Yy]$ ]] || die "Cancelled."
    fi
}

install_deps() {
    section "Installing dependencies"
    bash "$SCRIPT_DIR/scripts/_deps.sh"
}

backup_configs() {
    section "Backing up existing configs"
    bash "$SCRIPT_DIR/scripts/_backup.sh"
}

install_configs() {
    section "Installing configs"

    local SRC="$SCRIPT_DIR/config"
    local DST="$HOME/.config"
    mkdir -p "$DST"

    for item in "$SRC"/*; do
        [[ -e "$item" ]] || continue
        local name="$(basename "$item")"
        if [[ -d "$item" ]]; then
            cp -r "$item" "$DST/"
        else
            cp "$item" "$DST/"
        fi
        ok "config/$name"
    done
}

install_bin() {
    section "Installing scripts"

    mkdir -p "$HOME/.local/bin"
    for script in "$SCRIPT_DIR/bin/"*; do
        [[ -f "$script" ]] || continue
        local name="$(basename "$script")"
        cp "$script" "$HOME/.local/bin/$name"
        chmod +x "$HOME/.local/bin/$name"
        ok "bin/$name"
    done

    if ! echo "$PATH" | tr ':' '\n' | grep -qx "$HOME/.local/bin"; then
        warn "~/.local/bin not in PATH"
        warn "Fish should handle this via fish_add_path"
    fi
}

install_lib() {
    section "Installing Python modules"

    local DST="$HOME/.local/lib/nothing-os"
    mkdir -p "$DST"

    for f in "$SCRIPT_DIR/lib/"*.py; do
        [[ -f "$f" ]] || continue
        cp "$f" "$DST/"
        ok "lib/$(basename "$f")"
    done
}

install_wallpapers() {
    section "Installing wallpapers"

    local DST="$HOME/Pictures/wallpapers"
    mkdir -p "$DST"

    if [[ -d "$SCRIPT_DIR/wallpapers" ]]; then
        for f in "$SCRIPT_DIR/wallpapers/"*.png; do
            [[ -f "$f" ]] || continue
            cp "$f" "$DST/"
            ok "wallpapers/$(basename "$f")"
        done
    fi
}

install_fonts() {
    section "Fonts"

    local FONT_DIR="$HOME/.local/share/fonts"
    mkdir -p "$FONT_DIR"

    # Copy any fonts included in repo
    if [[ -d "$SCRIPT_DIR/fonts" ]]; then
        for f in "$SCRIPT_DIR/fonts/"*.otf "$SCRIPT_DIR/fonts/"*.ttf; do
            [[ -f "$f" ]] || continue
            cp "$f" "$FONT_DIR/"
            ok "fonts/$(basename "$f")"
        done
    fi

    warn "NDot font NOT included (Nothing's IP)"
    warn "Download: https://github.com/Lemmmy/Ndot"
    warn "Place Ndot-55.otf + Ndot-57.otf in $FONT_DIR/"

    fc-cache -f "$FONT_DIR" &>/dev/null || true
    ok "Font cache refreshed"
}

install_plymouth() {
    section "Plymouth boot theme"

    if ! has_cmd plymouth; then
        warn "Plymouth not installed — skipping"
        return
    fi

    local SRC="$SCRIPT_DIR/system/plymouth/nothing-os"
    local DST="/usr/share/plymouth/themes/nothing-os"

    if [[ ! -d "$SRC" ]]; then
        # Try generating assets
        if has_cmd nothing-plymouth-gen; then
            info "Generating Plymouth assets..."
            nothing-plymouth-gen
            SRC="/tmp/nothing-plymouth"
        else
            warn "Plymouth theme files missing — skipping"
            return
        fi
    fi

    if [[ -d "$SRC" ]]; then
        sudo mkdir -p "$DST"
        sudo cp -r "$SRC"/* "$DST/"
        sudo plymouth-set-default-theme -R nothing-os 2>/dev/null || \
            warn "Could not set Plymouth theme"
        ok "Plymouth theme installed"
    fi
}

post_install() {
    section "Post-install"
    bash "$SCRIPT_DIR/scripts/_post-install.sh"
}

print_summary() {
    cat <<'EOF'

═══════════════════════════════════════════════════════════
  ✓ Nothing OS Desktop installed
═══════════════════════════════════════════════════════════

Next steps:

  1. Download NDot font:
     https://github.com/Lemmmy/Ndot
     Save to ~/.local/share/fonts/

  2. Reload or reboot:
     hyprctl reload

  3. If Plymouth installed:
     sudo grub-mkconfig -o /boot/grub/grub.cfg

Keybindings:
  Super + Space      Launcher
  Super + Tab        Workspaces
  Super + L          Lock screen
  PrintScreen        Screenshot

Docs:
  https://github.com/vxsetup/nothing-os-desktop

EOF
}

# ─── Main ────────────────────────────────────────────────────

main() {
    clear
    print_banner

    check_arch
    check_not_root
    check_wayland
    check_compositor

    confirm_install

    install_deps
    backup_configs
    install_configs
    install_bin
    install_lib
    install_wallpapers
    install_fonts
    install_plymouth
    post_install

    print_summary
}

main "$@"
