#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Install dependencies
# ═══════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_common.sh"

# ─── Compositor ──────────────────────────────────────────────

section "Compositor & session"

pacman_install \
    hyprland \
    hyprlock \
    hypridle \
    xdg-desktop-portal-hyprland

# ─── Bar & notifications ────────────────────────────────────

section "Bar & notifications"

pacman_install \
    waybar \
    mako \
    libnotify

# ─── Screenshot / recording ─────────────────────────────────

section "Screenshot & recording"

pacman_install \
    grim \
    slurp \
    wf-recorder \
    wl-clipboard

# ─── Audio ───────────────────────────────────────────────────

section "Audio"

pacman_install \
    pipewire \
    pipewire-pulse \
    wireplumber \
    pavucontrol

# ─── Brightness / media ─────────────────────────────────────

section "Brightness & media"

pacman_install \
    brightnessctl \
    playerctl

# ─── Network / bluetooth ────────────────────────────────────

section "Network & bluetooth"

pacman_install \
    networkmanager \
    bluez \
    bluez-utils

# ─── GTK + Python ────────────────────────────────────────────

section "GTK4 + Python"

pacman_install \
    gtk3 \
    gtk4 \
    python \
    python-gobject \
    python-cairo

# gtk4-layer-shell
if ! pacman -Qi gtk4-layer-shell &>/dev/null 2>&1; then
    if pacman -Si gtk4-layer-shell &>/dev/null 2>&1; then
        pacman_install gtk4-layer-shell
    else
        info "gtk4-layer-shell not in repos — trying AUR..."
        aur_install gtk4-layer-shell || warn "gtk4-layer-shell failed"
    fi
else
    ok "gtk4-layer-shell installed"
fi

# ─── Shell + terminal ────────────────────────────────────────

section "Shell & terminal"

pacman_install \
    fish \
    kitty \
    starship

# ─── CLI tools ───────────────────────────────────────────────

section "CLI tools"

pacman_install \
    eza \
    bat \
    fastfetch \
    jq \
    dbus

# ─── Fonts ───────────────────────────────────────────────────

section "Fonts"

pacman_install ttf-jetbrains-mono-nerd || true
pacman_install ttf-jetbrains-mono || true

# Inter font — try all known names
if ! pacman -Qi inter-font &>/dev/null 2>&1 && \
   ! pacman -Qi ttf-inter &>/dev/null 2>&1; then
    if pacman -Si inter-font &>/dev/null 2>&1; then
        pacman_install inter-font
    elif pacman -Si ttf-inter &>/dev/null 2>&1; then
        pacman_install ttf-inter
    else
        aur_install inter-font || aur_install ttf-inter || \
            warn "Inter font not found — install manually"
    fi
else
    ok "Inter font installed"
fi

# ─── System utilities ────────────────────────────────────────

section "System utilities"

pacman_install polkit-gnome || true
pacman_install python-pip || true

# ─── Optional ────────────────────────────────────────────────

section "Optional packages"

pacman_install plymouth || true
pacman_install imv || true
pacman_install nautilus || true

# ─── AUR helper ──────────────────────────────────────────────

section "AUR packages"

if ! has_cmd yay && ! has_cmd paru; then
    warn "No AUR helper — installing yay..."
    pacman_install base-devel git
    tmp=$(mktemp -d)
    git clone --depth=1 https://aur.archlinux.org/yay-bin.git "$tmp/yay"
    pushd "$tmp/yay" >/dev/null
    makepkg -si --noconfirm
    popd >/dev/null
    rm -rf "$tmp"
    ok "yay installed"
fi

aur_install bibata-cursor-theme || warn "Bibata cursor failed (optional)"

# ─── Python pip fallback ─────────────────────────────────────

section "Python verification"

if python3 -c "import cairo" &>/dev/null 2>&1; then
    ok "python-cairo works"
else
    warn "python-cairo not working — trying pip..."
    pip install --user --break-system-packages pycairo 2>/dev/null || \
        pip install --user pycairo 2>/dev/null || \
        warn "pycairo install failed"
fi

# ─── Final check ─────────────────────────────────────────────

section "Final verification"

all_ok=true

for cmd in hyprland hyprlock waybar grim slurp python3 fish kitty starship jq notify-send; do
    if has_cmd "$cmd"; then
        ok "$cmd"
    else
        warn "MISSING: $cmd"
        all_ok=false
    fi
done

if python3 -c "import gi; gi.require_version('Gtk','4.0')" &>/dev/null 2>&1; then
    ok "GTK4 Python bindings"
else
    warn "MISSING: GTK4 Python bindings"
    all_ok=false
fi

if python3 -c "import cairo" &>/dev/null 2>&1; then
    ok "Cairo Python bindings"
else
    warn "MISSING: Cairo Python bindings"
    all_ok=false
fi

echo
if $all_ok; then
    ok "All dependencies installed!"
else
    warn "Some dependencies missing — check warnings above"
fi
