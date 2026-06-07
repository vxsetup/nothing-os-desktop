# ╔══════════════════════════════════════════════════════════════╗
# ║   Nothing OS — Fish Prompt v2.0                              ║
# ╚══════════════════════════════════════════════════════════════╝

function fish_prompt
    set -l last_status $status

    # Colors
    set -l red    (set_color FF3030)
    set -l white  (set_color FFFFFF)
    set -l gray   (set_color 999999)
    set -l dim    (set_color 4a4a4a)
    set -l green  (set_color 00e676)
    set -l yellow (set_color ffab00)
    set -l blue   (set_color 448aff)
    set -l reset  (set_color normal)

    # Newline before prompt
    echo ""

    # SSH indicator
    if set -q SSH_CONNECTION
        echo -n "$gray"(whoami)"$dim@$gray"(hostname -s)"$reset  "
    end

    # CWD
    echo -n "$white"(prompt_pwd --full-length-dirs 2 --dir-length 1)"$reset"

    # Git
    set -l branch (command git symbolic-ref --short HEAD 2>/dev/null; or command git describe --tags --exact-match 2>/dev/null)
    if test -n "$branch"
        set -l staged    (command git diff --cached --numstat 2>/dev/null | wc -l | string trim)
        set -l modified  (command git diff --numstat 2>/dev/null | wc -l | string trim)
        set -l untracked (command git ls-files --others --exclude-standard 2>/dev/null | wc -l | string trim)

        set -l git_color $gray
        set -l symbols ""

        if test "$staged" -gt 0
            set git_color $green
            set symbols "$symbols+"
        end
        if test "$modified" -gt 0
            set git_color $yellow
            set symbols "$symbols~"
        end
        if test "$untracked" -gt 0; and test -z "$symbols"
            set git_color $red
            set symbols "?"
        end

        echo -n "  $dim on $git_color$branch$reset"
        test -n "$symbols" && echo -n " $red$symbols$reset"
    end

    # Virtualenv
    if set -q VIRTUAL_ENV
        echo -n "  $dim($blue"(basename $VIRTUAL_ENV)"$dim)$reset"
    end

    # Duration
    if test -n "$CMD_DURATION"; and test "$CMD_DURATION" -gt 2000
        set -l secs (math --scale=1 "$CMD_DURATION / 1000")
        echo -n "  $dim$yellow{$secs}s$reset"
    end

    echo ""

    # Prompt symbol
    if test $last_status -eq 0
        echo -n "$red●$reset "
    else
        echo -n "$yellow○$reset "
    end
end
