from asciimatics.widgets import Frame, Layout, Label, Divider, Text, CheckBox, Button, PopUpDialog
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import StopApplication
import copy

class AdminConfigFrame(Frame):
    def __init__(self, screen, current_config, default_config):
        super(AdminConfigFrame, self).__init__(
            screen, screen.height, screen.width, has_border=True, name="Admin Panel", can_scroll=True
        )
        # We use a copy so we only apply changes if "Save" is pressed
        self._temp_config = copy.deepcopy(current_config)
        self._default_config = default_config

        # --- UI LAYOUT ---
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        
        layout.add_widget(Label("--- ADMIN CONTROL PANEL ---", align="^"))
        layout.add_widget(Divider())

        # Generate widgets for every config item
        for key, value in self._temp_config.items():
            default_val = self._default_config.get(key)
            
            if isinstance(value, bool):
                # Checkbox for Booleans
                layout.add_widget(CheckBox(f"{key} (Default: {default_val})", label=key, name=key))
            else:
                # Text for Integers/Strings
                layout.add_widget(Text(label=f"{key} (Default: {default_val}): ", name=key))

        layout.add_widget(Divider())

        # --- BUTTONS (Your original commands) ---
        button_layout = Layout([1, 1, 1])
        self.add_layout(button_layout)
        
        button_layout.add_widget(Button("SAVE (set)", self._save), 0)
        button_layout.add_widget(Button("RESET (dset)", self._reset_to_default), 1)
        button_layout.add_widget(Button("CANCEL", self._quit), 2)

        # Load data into widgets
        self._load_data(self._temp_config)
        self.fix()

    def _load_data(self, config_source):
        # Convert ints to strings for the Text widgets
        display_data = {}
        for k, v in config_source.items():
            display_data[k] = str(v) if not isinstance(v, bool) else v
        self.data = display_data

    def _reset_to_default(self):
        # Logic for your old 'dset' command: Reset the UI to factory defaults
        self._load_data(self._default_config)

    def _save(self):
        self.save() # Pull data from widgets into self.data
        # Logic for your old 'set' command: Convert back to proper types
        for key in self._temp_config:
            val = self.data[key]
            if isinstance(val, str) and val.strip().isdigit():
                self._temp_config[key] = int(val)
            else:
                self._temp_config[key] = val
        
        # Update the actual config being used by the game
        self.current_game_config = self._temp_config
        raise StopApplication("Settings Saved")

    def _quit(self):
        self.current_game_config = None # Signal that we cancelled
        raise StopApplication("User Cancelled")

def open_admin_tui(screen, quiz_config, default_config):
    admin_frame = AdminConfigFrame(screen, quiz_config, default_config)
    scene = Scene([admin_frame], -1)
    screen.play([scene], stop_on_resize=True)
    
    # Return the config back to the main program
    return admin_frame.current_game_config

# --- Main Game Integration ---
if __name__ == "__main__":
    # 1. Your original data structures
    default_quiz_config = {"hard_mode": False, "timer": 30, "lives": 3, "admin_mode": True}
    active_config = copy.deepcopy(default_quiz_config)

    # 2. Open the TUI
    # Note: Screen.wrapper returns the result of the function passed to it
    updated_config = Screen.wrapper(open_admin_tui, arguments=[active_config, default_quiz_config])

    # 3. Handle the result
    if updated_config:
        active_config = updated_config
        print("SUCCESS: Config updated with Admin TUI.")
    else:
        print("CANCELLED: Keeping previous config.")

    print(f"Current Config in use: {active_config}")