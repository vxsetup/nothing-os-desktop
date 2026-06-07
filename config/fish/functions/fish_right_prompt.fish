function fish_right_prompt
    set -l dim (set_color 4a4a4a)
    set -l reset (set_color normal)
    echo -n "$dim"(date "+%H:%M")"$reset"
end
