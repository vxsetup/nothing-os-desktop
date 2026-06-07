# ╔══════════════════════════════════════════════════════════════╗
# ║           Nothing OS — Fish Prompt v1.1                      ║
# ║   Промпт использует NType 82 Mono (терминальный шрифт)       ║
# ║   Символы ● ○ ◉ идеально рендерятся в NType 82 Mono         ║
# ╚══════════════════════════════════════════════════════════════╝

# Цвета
set -g __n_red    (set_color ff0000)
set -g __n_white  (set_color ffffff)
set -g __n_gray   (set_color 8a8a8a)
set -g __n_green  (set_color 00e676)
set -g __n_yellow (set_color ffab00)
set -g __n_blue   (set_color 448aff)
set -g __n_dim    (set_color 4a4a4a)
set -g __n_reset  (set_color normal)

function __n_git
    set -l branch (git branch --show-current 2>/dev/null)
    test -z "$branch" && return

    set -l staged    (git diff --cached --numstat 2>/dev/null | wc -l | string trim)
    set -l modified  (git diff --numstat 2>/dev/null | wc -l | string trim)
    set -l untracked (git ls-files --others --exclude-standard 2>/dev/null | wc -l | string trim)

    set -l color $__n_gray
    set -l symbols ""

    if test "$staged" -gt 0
        set color $__n_green; set symbols "$symbols+"
    end
    if test "$modified" -gt 0
        set color $__n_yellow; set symbols "$symbols~"
    end
    if test "$untracked" -gt 0; and test -z "$symbols"
        set color $__n_red; set symbols "?"
    end

    echo -n " $__n_dim on $color $branch"
    test -n "$symbols" && echo -n " $__n_red$symbols"
    echo -n $__n_reset
end

function __n_venv
    set -q VIRTUAL_ENV || return
    echo -n " $__n_dim($__n_blue"(basename $VIRTUAL_ENV)"$__n_dim)$__n_reset"
end

function __n_dur
    test -z "$CMD_DURATION" || test "$CMD_DURATION" -lt 3000 && return
    set -l s (math --scale=1 "$CMD_DURATION / 1000")
    echo -n " $__n_dim$__n_yellow${s}s$__n_reset"
end

function __n_ssh
    set -q SSH_CONNECTION || return
    echo -n "$__n_gray$USER$__n_dim@$__n_gray"(hostname -s)" $__n_reset"
end

# ── Prompt: NType 82 Mono рендерит всё корректно ─────────────
function fish_prompt
    set -l s $status
    echo ""
    __n_ssh
    # Путь — NType 82 Mono (моноширинный = идеальное выравнивание)
    echo -n "$__n_white"(prompt_pwd --full-length-dirs 2 --dir-length 1)"$__n_reset"
    __n_git
    __n_venv
    __n_dur
    echo ""
    # ● / ○ — Nothing-style индикатор статуса
    if test $s -eq 0
        echo -n "$__n_red●$__n_reset "
    else
        echo -n "$__n_yellow○$__n_reset "
    end
end

function fish_right_prompt
    # Время — справа, subtle
    echo -n "$__n_dim"(date "+%H:%M")"$__n_reset"
end

function fish_mode_prompt; end
