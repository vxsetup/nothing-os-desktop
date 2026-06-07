#!/usr/bin/env bash
# Install all required + optional dependencies
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# ─── Core (must) ────────────────────────────────────────────

CORE_PACMAN=(
    # Compositor
    hyprland
    hyprlock
    hypridle
    xdg-desktop-portal-hyprland

    # Bar & notifications
    waybar
    mako

    # Screenshot/screen recording
    grim slurp wf-recorder wl-clipboard

    # Audio/brightness
    pavucontrol pipewire pipewire-pulse wireplumber
    brightnessctl playerctl

    # Network/bluetooth
    networkmanager bluez bluez-utils

    # GTK
    gtk3 gtk4 gtk4-layer-shell
    python-gobject python-pycairo

    # Shell + terminal + tools
    fish
    kitty starship eza bat fastfetch

    # Fonts (fallback before NDot)
    ttf-jetbrains-mono ttf-jetbrains-mono-nerd
    inter-font ttf-inter

    # Misc
    jq python python-pip
    polkit-gnome
    libnotify
    dbus
)

OPTIONAL_PACMAN=(
    # Boot
    plymouth

    # Image viewers
    imv

    # File manager
    nautilus
)

AUR_PACKAGES=(
    bibata-cursor-theme
)

# ─── Sanity ─────────────────────────────────────────────────

check_pacman() {
    if ! has_cmd pacman; then
        die "pacman not found — this script is Arch-only"
    fi
}

ensure_aur_helper() {
    if has_cmd yay || has_cmd paru; then
        ok "AUR helper present"
        return 0
    fi

    warn "No AUR helper found, installing yay..."
    pacman_install base-devel git

    local tmp
    tmp=$(mktemp -d)
    git clone --depth=1 https://aur.archlinux.org/yay-bin.git "$tmp/yay"
    pushd "$tmp/yay" >/dev/null
    makepkg -si --noconfirm
    popd >/dev/null
    rm -rf "$tmp"
    ok "yay installed"
}

# ─── Run ────────────────────────────────────────────────────

check_pacman

info "Updating pacman database..."
sudo pacman -Sy --noconfirm
ok "Pacman synced"

info "Installing core dependencies..."
pacman_install "${CORE_PACMAN[@]}"

info "Installing optional dependencies..."
for pkg in "${OPTIONAL_PACMAN[@]}"; do
    pacman_install "$pkg" || warn "Skipped optional: $pkg"
done

ensure_aur_helper
info "Installing AUR packages..."
for pkg in "${AUR_PACKAGES[@]}"; do
    aur_install "$pkg" || warn "Skipped AUR: $pkg"
done

# ─── Python deps ────────────────────────────────────────────

info "Installing Python dependencies..."
if has_cmd pip; then
    pip install --user --break-system-packages pycairo 2>/dev/null || \
        pip install --user pycairo 2>/dev/null || \
        warn "pycairo install failed (may already be present via python-pycairo)"
fi

ok "All dependencies installed"
