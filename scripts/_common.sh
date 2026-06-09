#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
#  Nothing OS Desktop — Shared helpers
# ═══════════════════════════════════════════════════════════

if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GRN='\033[0;32m'
    YLW='\033[0;33m'
    BLU='\033[0;34m'
    DIM='\033[2m'
    BLD='\033[1m'
    RST='\033[0m'
else
    RED=; GRN=; YLW=; BLU=; DIM=; BLD=; RST=
fi

ACCENT='\033[38;5;196m'

section() {
    echo
    echo -e "${ACCENT}●${RST} ${BLD}$*${RST}"
    echo -e "${DIM}─────────────────────────────────────────────────${RST}"
}

ok()    { echo -e "  ${GRN}✓${RST} $*"; }
info()  { echo -e "  ${BLU}·${RST} $*"; }
warn()  { echo -e "  ${YLW}!${RST} $*"; }
err()   { echo -e "  ${RED}✗${RST} $*" >&2; }
die()   { err "$*"; exit 1; }
prompt(){ echo -e "${ACCENT}●${RST} $* "; }

has_cmd() { command -v "$1" &>/dev/null; }

pacman_install() {
    local missing=()
    for pkg in "$@"; do
        if ! pacman -Qi "$pkg" &>/dev/null 2>&1; then
            # Verify package exists in repos before adding
            if pacman -Si "$pkg" &>/dev/null 2>&1; then
                missing+=("$pkg")
            else
                warn "Package not in repos: $pkg (skipping)"
            fi
        fi
    done

    if [[ ${#missing[@]} -eq 0 ]]; then
        ok "All packages satisfied: $(echo "$*" | head -c 60)..."
        return 0
    fi

    info "Installing: ${missing[*]}"
    sudo pacman -S --noconfirm --needed "${missing[@]}"
    ok "Installed: ${missing[*]}"
}

aur_install() {
    local missing=()
    for pkg in "$@"; do
        if ! pacman -Qi "$pkg" &>/dev/null 2>&1; then
            missing+=("$pkg")
        fi
    done

    if [[ ${#missing[@]} -eq 0 ]]; then
        ok "All AUR packages satisfied: $*"
        return 0
    fi

    if ! has_cmd yay && ! has_cmd paru; then
        warn "No AUR helper (yay/paru) found"
        warn "Manual install needed: ${missing[*]}"
        return 1
    fi

    local aur_helper
    if has_cmd yay; then aur_helper=yay
    else aur_helper=paru; fi

    info "Installing AUR via $aur_helper: ${missing[*]}"
    "$aur_helper" -S --noconfirm --needed "${missing[@]}"
    ok "Installed: ${missing[*]}"
}
