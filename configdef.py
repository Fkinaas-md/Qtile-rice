import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "st"

# Цветовая схема (как в твоем примере)
colors = {
    "bg": "#212121",
    "fg": "#ABABAB",
    "accent1": "#999694",
    "accent2": "#757575",
    "dim": "#404040",
}

keys = [
    # --- УПРАВЛЕНИЕ ОКНАМИ ---
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    
    # --- СИСТЕМА ---
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod, "control"], "r", lazy.reload_config()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # --- СМЕНА ЯЗЫКА (Alt + Shift) ---
    # Примечание: Это команда для X11
    Key(["mod1"], "Shift_L", lazy.spawn("setxkbmap -layout us,ru -option grp:alt_shift_toggle")),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layouts = [
    layout.Columns(border_focus=colors["accent2"], border_normal=colors["dim"], margin=6, border_width=2),
    layout.Max(),
]

widget_defaults = dict(
    font="sans bold",
    fontsize=12,
    padding=3,
    foreground=colors["fg"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                # ЛЕВАЯ ЧАСТЬ
                widget.GroupBox(
                    highlight_method='line',
                    highlight_color=[colors["bg"], colors["dim"]],
                    this_current_screen_border=colors["accent1"],
                ),
                widget.Prompt(),
                widget.WindowName(foreground=colors["accent2"]),

                # --- ЦЕНТРИРОВАНИЕ ---
                widget.Spacer(), # Первый растягивающийся разделитель
                
                # Загрузка CPU
                widget.CPU(
                    format='CPU {load_percent}%',
                    foreground=colors["accent1"],
                    padding=10
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["dim"]),
                
                # Оперативная память (как в твоем примере)
                widget.Memory(
                    format='{MemUsed: .0f}M/{MemTotal: .0f}M',
                    foreground=colors["fg"],
                    padding=10
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["dim"]),

                # Батарея
                widget.Battery(
                    format='BAT {percent:2.0%}',
                    notify_below=15,
                    foreground=colors["accent1"],
                    padding=10
                ),

                widget.Spacer(), # Второй растягивающийся разделитель
                # ---------------------

                # ПРАВАЯ ЧАСТЬ
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %H:%M", foreground=colors["accent1"]),
                widget.QuickExit(default_text='[X]', countdown_format='[{}]'),
            ],
            28,
            background=colors["bg"],
        ),
    ),
]

# Автозагрузка
@hook.subscribe.startup_once
def autostart():
    # Установка раскладки и переключателя при старте
    subprocess.Popen(["setxkbmap", "-layout", "us,ru", "-option", "grp:alt_shift_toggle"])

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
