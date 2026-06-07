# ╔══════════════════════════════════════════════════════════════╗
# ║   Nothing OS — Fish Shell v2.1 · Final                       ║
# ╚══════════════════════════════════════════════════════════════╝

# ── Greeting (отключено) ──────────────────────────────────────

set -g fish_greeting ""

eval "$(starship init fish)"

# ── Environment ───────────────────────────────────────────────

set -gx EDITOR    nvim
set -gx VISUAL    nvim
set -gx PAGER     less
set -gx BROWSER   firefox
set -gx TERMINAL  kitty
set -gx LANG      en_US.UTF-8

set -gx XDG_CONFIG_HOME "$HOME/.config"
set -gx XDG_DATA_HOME   "$HOME/.local/share"
set -gx XDG_CACHE_HOME  "$HOME/.cache"
set -gx XDG_STATE_HOME  "$HOME/.local/state"

set -gx MOZ_ENABLE_WAYLAND 1
set -gx QT_QPA_PLATFORM    wayland
set -gx LESS               "-R"
set -gx LESSHISTFILE       "-"

# ── PATH ──────────────────────────────────────────────────────

fish_add_path -p "$HOME/.local/bin"
fish_add_path -p "$HOME/.config/scripts"
fish_add_path -p "$HOME/.config/hypr/scripts"

# ── FZF — Nothing theme ───────────────────────────────────────

set -gx FZF_DEFAULT_OPTS "
  --color=bg+:#1a1a1a,bg:#000000,spinner:#FF3030,hl:#FF3030
  --color=fg:#FFFFFF,header:#999999,info:#ffab00,pointer:#FF3030
  --color=marker:#FF3030,fg+:#FFFFFF,prompt:#FF3030,hl+:#FF3030
  --color=border:#1C1C1C,label:#FF3030,query:#FFFFFF
  --border=rounded --prompt='● ' --pointer='▶' --marker='◉'
  --layout=reverse --info=inline --height=40%
"

if command -q fd
    set -gx FZF_DEFAULT_COMMAND "fd --type f --hidden --follow --exclude .git"
end

# ── Nothing color palette ─────────────────────────────────────

set -U fish_color_normal         FFFFFF
set -U fish_color_command        FF3030
set -U fish_color_keyword        FF3030
set -U fish_color_quote          999999
set -U fish_color_redirection    FFFFFF
set -U fish_color_end            FF3030
set -U fish_color_error          FF3030
set -U fish_color_param          FFFFFF
set -U fish_color_comment        4a4a4a
set -U fish_color_selection      --background=1a1a1a
set -U fish_color_search_match   --background=1a1a1a
set -U fish_color_operator       FF3030
set -U fish_color_escape         ffab00
set -U fish_color_autosuggestion 4a4a4a
set -U fish_color_cwd            FFFFFF
set -U fish_color_user           FF3030
set -U fish_color_host           999999
set -U fish_color_cancel         FF3030
set -U fish_color_valid_path     --underline

set -U fish_pager_color_progress             FF3030
set -U fish_pager_color_prefix               FF3030
set -U fish_pager_color_completion           FFFFFF
set -U fish_pager_color_description          999999
set -U fish_pager_color_selected_background  --background=FF3030
set -U fish_pager_color_selected_prefix      000000
set -U fish_pager_color_selected_completion  000000

# ╔══════════════════════════════════════════════════════════════╗
# ║   ALIASES                                                    ║
# ╚══════════════════════════════════════════════════════════════╝

# ── Navigation ────────────────────────────────────────────────

alias ..    "cd .."
alias ...   "cd ../.."
alias ....  "cd ../../.."

function \~ --description "Go home"
    cd ~ $argv
end

# ── Listing ───────────────────────────────────────────────────

if command -q eza
    alias ls    "eza --icons --group-directories-first"
    alias ll    "eza --icons --group-directories-first -l --git"
    alias la    "eza --icons --group-directories-first -la --git"
    alias lt    "eza --icons --group-directories-first -T --level=2"
    alias l     "eza --icons -1"
else
    alias ll    "ls -l"
    alias la    "ls -la"
end

# ── Editor ────────────────────────────────────────────────────

alias v     nvim
alias vim   nvim
alias vi    nvim

# ── System ────────────────────────────────────────────────────

if command -q bat
    alias cat   bat
end

if command -q btop
    alias top   btop
end

alias grep  "grep --color=auto"
alias df    "df -h"
alias du    "du -sh"
alias free  "free -h"

# ── Git ───────────────────────────────────────────────────────

alias g     git
alias gs    "git status -sb"
alias ga    "git add"
alias gaa   "git add -A"
alias gc    "git commit"
alias gcm   "git commit -m"
alias gca   "git commit --amend"
alias gp    "git push"
alias gpf   "git push --force-with-lease"
alias gl    "git log --oneline --graph --decorate --all"
alias gd    "git diff"
alias gds   "git diff --staged"
alias gb    "git branch"
alias gco   "git checkout"
alias gcb   "git checkout -b"
alias gpl   "git pull"
alias gf    "git fetch"
alias gst   "git stash"
alias gstp  "git stash pop"

# ── Package management ────────────────────────────────────────

alias pacs  "sudo pacman -S"
alias pacr  "sudo pacman -Rns"
alias pacu  "sudo pacman -Syu"
alias pacq  "pacman -Q | grep"
alias ys    "yay -S"
alias yu    "yay -Syu"
alias yr    "yay -Rns"

# ── Clipboard (Wayland) ───────────────────────────────────────

alias copy  "wl-copy"
alias paste "wl-paste"

# ── Safety ────────────────────────────────────────────────────

alias rm    "rm -i"
alias cp    "cp -i"
alias mv    "mv -i"

# ── Shortcuts ─────────────────────────────────────────────────

alias cfg       "cd ~/.config"
alias reload    "source ~/.config/fish/config.fish"
alias hyprconf  "nvim ~/.config/hypr/hyprland.conf"
alias wayconf   "nvim ~/.config/waybar/config"
alias fishconf  "nvim ~/.config/fish/config.fish"
alias nvimconf  "nvim ~/.config/nvim/init.lua"
alias kittyconf "nvim ~/.config/kitty/kitty.conf"

# ╔══════════════════════════════════════════════════════════════╗
# ║   FUNCTIONS                                                  ║
# ╚══════════════════════════════════════════════════════════════╝

# ── mkcd ─────────────────────────────────────────────────────

function mkcd --description "mkdir and cd"
    mkdir -p $argv[1]; and cd $argv[1]
end

# ── extract ───────────────────────────────────────────────────

function extract --description "Extract any archive"
    if not test -f $argv[1]
        echo "File not found: $argv[1]"
        return 1
    end
    switch $argv[1]
        case "*.tar.gz" "*.tgz";   tar xzf $argv[1]
        case "*.tar.bz2" "*.tbz";  tar xjf $argv[1]
        case "*.tar.xz" "*.txz";   tar xJf $argv[1]
        case "*.tar.zst";          tar --zstd -xf $argv[1]
        case "*.tar";              tar xf  $argv[1]
        case "*.gz";               gunzip  $argv[1]
        case "*.bz2";              bunzip2 $argv[1]
        case "*.zip";              unzip   $argv[1]
        case "*.7z";               7z x    $argv[1]
        case "*.rar";              unrar x $argv[1]
        case "*";                  echo "Unknown archive: $argv[1]"
    end
end

# ── backup ────────────────────────────────────────────────────

function backup --description "Create backup of file"
    cp -r $argv[1] "$argv[1].bak."(date +%Y%m%d_%H%M%S)
    echo "● Backup created"
end

# ── ff — fuzzy find file ──────────────────────────────────────

function ff --description "Fuzzy find file and open in nvim"
    if not command -q fzf
        echo "fzf not installed"
        return 1
    end

    set -l file
    if command -q fd
        set file (fd --type f --hidden --follow --exclude .git \
            | fzf --preview 'bat --color=always --style=numbers {}' \
                  --preview-window 'right:60%:border-left' \
                  --prompt '● ' --query "$argv")
    else
        set file (find . -type f -not -path '*/\.git/*' \
            | fzf --prompt '● ' --query "$argv")
    end

    test -n "$file" && nvim "$file"
end

# ── fcd — fuzzy cd ────────────────────────────────────────────

function fcd --description "Fuzzy find directory and cd"
    if not command -q fzf
        echo "fzf not installed"
        return 1
    end

    set -l dir
    if command -q fd
        set dir (fd --type d --hidden --follow --exclude .git \
            | fzf --preview 'eza --icons --color=always {}' \
                  --preview-window 'right:40%:border-left' \
                  --prompt '● ' --query "$argv")
    else
        set dir (find . -type d -not -path '*/\.git/*' \
            | fzf --prompt '● ' --query "$argv")
    end

    test -n "$dir" && cd "$dir"
end

# ── sysinfo ───────────────────────────────────────────────────

function sysinfo --description "Show system info"
    set -l red    (set_color FF3030)
    set -l white  (set_color FFFFFF)
    set -l gray   (set_color 999999)
    set -l dim    (set_color 4a4a4a)
    set -l reset  (set_color normal)

    echo ""
    echo "$red●$reset Nothing OS $dim·$reset Arch Linux"
    echo ""
    printf "$dim  %-8s$reset %s\n" "OS"     (uname -r)
    printf "$dim  %-8s$reset %s\n" "Shell"  "fish $FISH_VERSION"
    printf "$dim  %-8s$reset %s\n" "Uptime" (uptime -p | sed 's/up //')
    printf "$dim  %-8s$reset %s\n" "CPU"    (grep 'model name' /proc/cpuinfo | head -1 | awk -F': ' '{print $2}')
    printf "$dim  %-8s$reset %s\n" "RAM"    (free -h | awk '/^Mem:/ {print $3 " / " $2}')
    printf "$dim  %-8s$reset %s\n" "Disk"   (df -h / | awk 'NR==2 {print $3 " / " $2}')
    echo ""
end

# ── weather ───────────────────────────────────────────────────

function weather --description "Get weather"
    curl -sL "wttr.in/$argv[1]?format=3"
end

# ╔══════════════════════════════════════════════════════════════╗
# ║   TOOLS INIT                                                 ║
# ╚══════════════════════════════════════════════════════════════╝

if command -q zoxide
    zoxide init fish | source
end

# ╔══════════════════════════════════════════════════════════════╗
# ║   STARTUP                                                    ║
# ╚══════════════════════════════════════════════════════════════╝

if status is-interactive
    and not set -q TMUX
    if command -q fastfetch
        fastfetch
    end
end

# ── Local config ──────────────────────────────────────────────

if test -f ~/.config/fish/local.fish
    source ~/.config/fish/local.fish
end

# Added by LM Studio CLI (lms)
set -gx PATH $PATH /home/vxs/.lmstudio/bin
# End of LM Studio CLI section


fish_add_path /home/vxs/.spicetify


set -gx LS_COLORS "di=31;1:ln=35:so=32:pi=33:ex=32;1:bd=34:cd=34:su=31:sg=31:tw=31:ow=31:*.py=36:*.js=33:*.ts=36:*.rs=33:*.go=36:*.c=36:*.cpp=36:*.h=35:*.sh=32:*.bash=32:*.zsh=32:*.fish=32:*.json=33:*.yaml=33:*.yml=33:*.toml=33:*.xml=33:*.conf=33:*.ini=33:*.md=37:*.txt=37:*.log=90:*.lock=90:*.bak=90:*.tmp=90:*.png=33:*.jpg=33:*.jpeg=33:*.gif=33:*.svg=33:*.webp=33:*.mp4=91:*.mkv=91:*.avi=91:*.mov=91:*.mp3=35:*.flac=35:*.wav=35:*.ogg=35:*.zip=32:*.tar=32:*.gz=32:*.xz=32:*.7z=32:*.rar=32:*.deb=32:*.rpm=32:*.pdf=91:*.doc=36:*.docx=36"
