from asciimatics.widgets import Frame, Layout, Label, Divider
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import StopApplication
from asciimatics.event import KeyboardEvent

class LevelTransitionFrame(Frame):
    def __init__(self, screen, old_lvl, new_lvl, score):
        # Full screen, no border for a "cinematic" feel
        super(LevelTransitionFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="Transition"
        )
        self.set_theme("bright")
        
        # [1, 2, 1] Layout keeps everything perfectly centered
        layout = Layout([1, 2, 1], fill_frame=True)
        self.add_layout(layout)

        # Top Spacing (Replaced Blank with Label)
        layout.add_widget(Label(""), 1)
        layout.add_widget(Label(""), 1)

        """ # Big "STAGE CLEAR" header
        header = FigletText("STAGE CLEAR", font="slant")
        layout.add_widget(Label(header, height=header.max_height), 1) """
        
        layout.add_widget(Divider(), 1)
        
        # Stats Section
        layout.add_widget(Label(f"COMPLETED: LEVEL {old_lvl}", align="^"), 1)
        layout.add_widget(Label(f"SCORE: {score}", align="^"), 1)
        layout.add_widget(Label(""), 1) # Spacer
        
        # Big "NEXT LEVEL" highlight
        next_lvl = FigletText(f"LEVEL {new_lvl}", font="small")
        layout.add_widget(Label(next_lvl, height=next_lvl.max_height), 1)
        
        layout.add_widget(Divider(), 1)
        layout.add_widget(Label("Press [ SPACE ] to begin next stage", align="^"), 1)

        self.fix()

    def process_event(self, event):
        # Handle the spacebar to continue
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord(' '): 
                raise StopApplication("Next Level")
        return super(LevelTransitionFrame, self).process_event(event)

def play_transition(screen, old_lvl, new_lvl, score):
    scene = Scene([LevelTransitionFrame(screen, old_lvl, new_lvl, score)], -1)
    try:
        screen.play([scene], stop_on_resize=True, repeat=False)
    except StopApplication:
        pass

def main(score, correct, total):
    try:
        Screen.wrapper(lambda s: play_transition(s, 1, 2, f"%{score} ({correct}/{total})"))
    except StopApplication:
        return

if __name__ == "__main__":
    # Test call: Moving from Level 1 to Level 2 with 500 points
    Screen.wrapper(lambda s: play_transition(s, 1, 2, 500))
    
    print("\n" * 2)
    print("--- LEVEL 2 STARTED ---")