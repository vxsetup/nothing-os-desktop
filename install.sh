#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Installer
#  Arch Linux + Hyprland
# ═══════════════════════════════════════════════════════════

set -euo pipefail

# ─── Paths ───────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/scripts/_common.sh"

# ─── Banner ──────────────────────────────────────────────────

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

# ─── Pre-flight checks ──────────────────────────────────────

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
        warn "Wayland not currently active — that's OK for first install."
    else
        ok "Wayland session active"
    fi
}

check_compositor() {
    if [[ "${XDG_CURRENT_DESKTOP:-}" != "Hyprland" ]] && \
       ! pgrep -x Hyprland &>/dev/null; then
        warn "Hyprland not running. Some live operations will be skipped."
        SKIP_LIVE_OPS=1
    else
        ok "Hyprland active"
        SKIP_LIVE_OPS=0
    fi
}

# ─── Install steps ───────────────────────────────────────────

confirm_install() {
    echo
    info "This installer will:"
    echo "  · Install Arch packages via pacman + yay"
    echo "  · Backup existing configs to ~/.config-backup-<timestamp>/"
    echo "  · Copy Nothing OS configs to ~/.config/"
    echo "  · Install scripts to ~/.local/bin/"
    echo "  · Install Python modules to ~/.local/lib/nothing-os/"
    echo "  · Install fish shell config + set as default shell"
    echo "  · Install Plymouth theme (requires sudo)"
    echo "  · Install wallpapers to ~/Pictures/wallpapers/"
    echo
    info "After install, log out and log back into Hyprland."
    echo
    if [[ "${NOTHING_AUTO_YES:-0}" != "1" ]]; then
        read -rp "$(prompt 'Continue? [y/N]: ')" answer
        [[ "$answer" =~ ^[Yy]$ ]] || die "Cancelled by user."
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
    section "Installing user configs"

    local SRC="$SCRIPT_DIR/config"
    local DST="$HOME/.config"

    mkdir -p "$DST"

    local items=(
        "hypr"
        "waybar"
        "mako"
        "kitty"
        "starship.toml"
        "gtk-3.0"
        "gtk-4.0"
        "fish"
    )

    for item in "${items[@]}"; do
        if [[ -e "$SRC/$item" ]]; then
            cp -r "$SRC/$item" "$DST/"
            ok "config/$item → ~/.config/$item"
        else
            warn "Skipped (missing in repo): config/$item"
        fi
    done
}

install_bin() {
    section "Installing scripts to ~/.local/bin/"

    mkdir -p "$HOME/.local/bin"

    for script in "$SCRIPT_DIR/bin/"*; do
        if [[ -f "$script" ]]; then
            local name="$(basename "$script")"
            cp "$script" "$HOME/.local/bin/$name"
            chmod +x "$HOME/.local/bin/$name"
            ok "bin/$name"
        fi
    done

    if ! echo "$PATH" | tr ':' '\n' | grep -qx "$HOME/.local/bin"; then
        warn "~/.local/bin is not in your PATH"
        warn "Add to your shell rc:  set -gx PATH \$HOME/.local/bin \$PATH"
    fi
}

install_lib() {
    section "Installing Python modules"

    local DST="$HOME/.local/lib/nothing-os"
    mkdir -p "$DST"

    for f in "$SCRIPT_DIR/lib/"*.py; do
        if [[ -f "$f" ]]; then
            cp "$f" "$DST/"
            ok "lib/$(basename "$f")"
        fi
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

    if [[ ! -f "$DST/glyph.png" ]] && \
       command -v nothing-wallpaper-gen &>/dev/null; then
        info "Generating default wallpaper..."
        nothing-wallpaper-gen --output "$DST/glyph.png" \
                              --variant glyph --palette dark || true
        ok "Generated wallpapers/glyph.png"
    fi
}

install_fonts() {
    section "Setting up fonts"

    local FONT_DIR="$HOME/.local/share/fonts"
    mkdir -p "$FONT_DIR"

    warn "NDot font is NOT included (Nothing's IP)."
    warn "Download manually: https://github.com/Lemmmy/Ndot"
    warn "Save Ndot-55.otf and Ndot-57.otf to:"
    warn "  $FONT_DIR/"

    if command -v fc-cache &>/dev/null; then
        fc-cache -f "$FONT_DIR" &>/dev/null || true
        ok "Font cache refreshed"
    fi
}

install_fish_config() {
    section "Setting up fish shell"

    if ! command -v fish &>/dev/null; then
        warn "fish not installed — skipping"
        return
    fi

    # Make fish the default shell if it isn't
    local current_shell
    current_shell="$(getent passwd "$USER" | cut -d: -f7)"
    local fish_bin
    fish_bin="$(command -v fish)"

    if [[ "$current_shell" != "$fish_bin" ]]; then
        info "Changing default shell to fish..."
        # Ensure fish is in /etc/shells
        if ! grep -qx "$fish_bin" /etc/shells; then
            echo "$fish_bin" | sudo tee -a /etc/shells >/dev/null
        fi
        if sudo chsh -s "$fish_bin" "$USER" 2>/dev/null; then
            ok "Default shell changed to fish (takes effect on next login)"
        else
            warn "Failed to change shell automatically"
            warn "Run manually:  chsh -s $fish_bin"
        fi
    else
        ok "fish already the default shell"
    fi

    # Install starship init in fish config (if not present)
    local fish_config="$HOME/.config/fish/config.fish"
    if [[ -f "$fish_config" ]] && \
       command -v starship &>/dev/null && \
       ! grep -q "starship init" "$fish_config"; then
        echo "" >> "$fish_config"
        echo "# Starship prompt" >> "$fish_config"
        echo "starship init fish | source" >> "$fish_config"
        ok "Starship init added to fish config"
    fi
}

install_plymouth() {
    section "Installing Plymouth boot theme"

    if ! command -v plymouth &>/dev/null; then
        warn "plymouth not installed — skipping boot theme"
        warn "Install: sudo pacman -S plymouth"
        return
    fi

    local SRC="$SCRIPT_DIR/system/plymouth/nothing-os"
    local DST="/usr/share/plymouth/themes/nothing-os"

    if [[ ! -d "$SRC" ]]; then
        warn "Plymouth theme files not found in repo, generating..."
        if command -v nothing-plymouth-gen &>/dev/null; then
            nothing-plymouth-gen
            SRC="/tmp/nothing-plymouth"
        else
            warn "Skipping Plymouth (theme files missing)"
            return
        fi
    fi

    info "Copying Plymouth theme (requires sudo)..."
    sudo mkdir -p "$DST"
    sudo cp -r "$SRC"/* "$DST/"

    info "Setting nothing-os as default Plymouth theme..."
    sudo plymouth-set-default-theme -R nothing-os 2>/dev/null || \
        warn "plymouth-set-default-theme failed (may need GRUB regenerate)"

    ok "Plymouth theme installed"
    warn "For boot theme to work, ensure /etc/default/grub has:"
    warn '  GRUB_CMDLINE_LINUX_DEFAULT="quiet splash loglevel=3"'
    warn "And rebuild: sudo grub-mkconfig -o /boot/grub/grub.cfg"
}

post_install() {
    section "Post-install steps"
    bash "$SCRIPT_DIR/scripts/_post-install.sh"
}

print_summary() {
    cat <<'EOF'

═══════════════════════════════════════════════════════════
  ✓ Nothing OS Desktop installed successfully
═══════════════════════════════════════════════════════════

Next steps:

  1. Download NDot font (REQUIRED for proper visuals):
     → https://github.com/Lemmmy/Ndot
     Save Ndot-55.otf + Ndot-57.otf to ~/.local/share/fonts/

  2. Restart Hyprland (or log out/in):
     hyprctl reload

  3. (If installed Plymouth) Rebuild GRUB:
     sudo grub-mkconfig -o /boot/grub/grub.cfg

  4. Reboot to see the full experience.

Key bindings:
  Super + Space      Launcher
  Super + Tab        Workspace switcher
  Super + L          Lock screen
  PrintScreen        Screenshot
  Super + N          Notifications

Live config:
  ~/.config/hypr/        Hyprland setup
  ~/.config/fish/        Fish shell config
  ~/.config/nothing-os/  Per-popup config

Logs:
  /tmp/nothing-*.log

Documentation:
  https://github.com/vxsetup/nothing-os-desktop

EOF
}

# ─── Main ────────────────────────────────────────────────────

main() {
    clear
    print_banner

    info "Starting Nothing OS Desktop installation..."
    echo

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
    install_fish_config
    install_plymouth
    post_install

    print_summary
}

main "$@"
