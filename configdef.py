import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


mod = "mod4"  
alt = "mod1" 
terminal = "st" 


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

keys = [
  
    Key([mod], "h", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Run Launcher"),

   
    Key([alt], "r", lazy.spawn("xfce4-screenshooter -r"), desc="Screenshot region"),

    
    Key([mod], "space", lazy.spawn("setxkbmap -layout us,ru -option grp:alt_shift_toggle")),
]


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layout_theme = {
    "border_width": 3,
    "margin": 6,
    "border_normal": colors["border_inactive"],
    "border_focus": colors["border_active"],
}

layouts = [
    layout.Columns(**layout_theme, border_focus_stack=colors["accent_1"]),
    layout.Max(),
    layout.MonadTall(**layout_theme),
]

widget_defaults = dict(
    font="sans bold",
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
               
                widget.GroupBox(
                    active=colors["border_active"],
                    inactive=colors["text_dim"],
                    highlight_method="line",
                    this_current_screen_border=colors["border_active"],
                    padding_x=5,
                ),
                widget.CurrentLayoutIcon(scale=0.7),
                widget.WindowName(max_chars=30),

                
                widget.Spacer(),
                
                
                widget.CPU(
                    format="CPU {load_percent}%",
                    foreground=colors["accent_1"],
                    padding=10
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["border_inactive"]),
                
               
                widget.Memory(
                    format="{MemUsed: .0f}M/{MemTotal: .0f}M",
                    foreground=colors["text_main"],
                    padding=10
                ),
                widget.Sep(linewidth=1, padding=10, foreground=colors["border_inactive"]),
                
               
                widget.Battery(
                    format="BAT {percent:2.0%}",
                    foreground=colors["accent_2"],
                    padding=10,
                    low_foreground="#ff5555",
                ),
                
                widget.Spacer(),
               

                
                widget.Systray(),
                widget.Volume(
                    padding=10,
                    mouse_callbacks={'Button1': lambda: lazy.spawn("pavucontrol")}
                ),
                widget.Clock(format="%Y-%m-%d %a %H:%M", foreground=colors["border_active"]),
                widget.QuickExit(default_text='[logout]', foreground=colors["text_dim"]),
            ],
            28,
            background=colors["bg_bar"],
            border_width=[2, 0, 0, 0],
            border_color=colors["border_active"]
        ),
    ),
]


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    
   
    subprocess.Popen(["setxkbmap", "-layout", "us,ru", "-option", "grp:alt_shift_toggle"])
    
    
    subprocess.Popen(["xfce4-clipman"])
    
  
    wallpaper = os.path.join(home, "wallp.png")
    if os.path.exists(wallpaper):
        subprocess.Popen(["feh", "--bg-scale", wallpaper])
    
  
    os.system("xset s off && xset --dpms && xset s nonblank")

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=colors["border_active"],
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="pinentry"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
wl_input_rules = None
wmname = "LG3D"
