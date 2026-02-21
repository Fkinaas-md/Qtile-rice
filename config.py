# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

mod = "mod4"
terminal = "gnome-terminal"

colors = {
    "bg_bar": "#212121",
    "bg_inactive": "#5C5C5C",

    "border_active": "#757575",
    "border_inactive": "#424242",

    "text_main": "#ABABAB",
    "text_dim": "#404040",

    "accent_1": "#999694",
    "accent_2": "#999694",
}
# ==========================================================

# global settings for layout :p
layout_theme = {
    "border_width": 3,
    "margin": 6,
    "border_normal": colors["border_inactive"],
    "border_focus": colors["border_active"],
    "border_on_single": colors["border_active"],
}

keys = [

    Key([], "Super_L", lazy.spawn("setxkbmap -layout 'us,ru' -option 'grp:alt_shift_toggle'"), desc="Set keyboard layout"),


    Key([mod], "h", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "space", lazy.layout.next(), desc="Next layout"),


    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),


    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset sizes"),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([mod], "w", lazy.window.kill(), desc="Kill window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Rofi launcher"),


    Key([mod], "p", lazy.spawn("xfce4-screenshooter -r -c"), desc="Xfce4 screenshooter"),
    Key(["mod1"], "r", lazy.spawn("import -silent png:- | xclip -selection clipboard -t image/png -quiet"), desc="Screenshot region Imagemagick"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Move to group {i.name}"),
    ])

# Layouts
layouts = [
    layout.Columns(
        **layout_theme,
        border_focus_stack=[colors["border_active"], colors["accent_1"]]
    ),
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Bsp(**layout_theme),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
    foreground=colors["text_main"],
    background=colors["bg_bar"]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                # left sode
                widget.GroupBox(
                    foreground=colors["text_main"],
                    background=colors["bg_bar"],
                    active=colors["border_active"],
                    inactive=colors["text_dim"],
                    highlight_color=[colors["bg_inactive"], colors["bg_bar"]],
                    highlight_method="line",
                    this_current_screen_border=colors["border_active"],
                    margin_y=3,
                    padding_y=5,
                    padding_x=5,
                ),
                widget.WindowName(foreground=colors["text_main"], max_chars=40),

                # center CPU, RAM
                widget.Spacer(),
                widget.CPU(
                    format="CPU {load_percent}%",
                    foreground=colors["accent_1"],
                    padding=8
                ),
                widget.Sep(
                    linewidth=1,
                    foreground=colors["border_inactive"],
                    padding=10
                ),
                widget.Memory(
                    format="{MemUsed: .0f}M/{MemTotal: .0f}M",
                    foreground=colors["accent_2"],
                    padding=8
                ),
                widget.Spacer(),

                # right side
                widget.Systray(),
                widget.Volume(
                    foreground=colors["text_main"],
                    padding=8,
                    mouse_callbacks={
                        'Button1': lambda: lazy.spawn("pavucontrol"),
                        'Button4': lambda: lazy.spawn("amixer set Master 5%+"),
                        'Button5': lambda: lazy.spawn("amixer set Master 5%-"),
                        'Button3': lambda: lazy.spawn("amixer set Master toggle"),
                    }
                ),
                widget.Clock(format="%Y-%m-%d %a %H:%M:%S", foreground=colors["border_active"]),
                widget.QuickExit(foreground=colors["text_dim"]),
            ],
            28,
            background=colors["bg_bar"],

            border_width=[2, 0, 0, 0],
            border_color=[colors["border_active"], colors["bg_bar"], colors["bg_bar"], colors["bg_bar"]]
        ),
    ),
]

# Mouse
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    border_width=3,
    margin=6,
    border_normal=colors["border_inactive"],
    border_focus=colors["border_active"],
    border_on_single=colors["border_active"],
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

wmii = True
auto_fullscreen = True
follow_mouse_focus = False
bring_front_click = True
floats_kept_above = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    os.system("xset s off && xset --dpms && xset s nonblank")
    subprocess.Popen(["xfce4-clipman"])

    wallpaper = os.path.join(home, "wallp.png")
    if os.path.exists(wallpaper):
        subprocess.Popen(["feh", "--bg-scale", wallpaper])

    subprocess.Popen(["sh", "-c", "sleep 2 && xrandr --output HDMI-0 --mode 1920x1080 --rate 180"])

wmname = "Qtile"
