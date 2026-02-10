from asciimatics.widgets import Frame, Layout, Label, Divider
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import StopApplication
from asciimatics.event import KeyboardEvent

class LevelTransitionFrame(Frame):
    def __init__(self, screen, old_lvl, new_lvl, score):
        # Full screen, no borders to avoid "box-in-a-box" scuffing
        super(LevelTransitionFrame, self).__init__(
            screen, screen.height, screen.width, has_border=False, name="Transition"
        )
        self.set_theme("bright")
        
        # Use one big layout for total control
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        # 1. Top Padding (Move everything down so it's not hugging the top)
        for _ in range(screen.height // 6):
            layout.add_widget(Label(""))

        # 2. Centered Header
        header = FigletText("STAGE CLEAR", font="slant")
        # We explicitly set height so it doesn't overlap the next line
        layout.add_widget(Label(header, height=header.max_height + 1, align="^"))
        
        layout.add_widget(Divider())
        layout.add_widget(Label("")) # Breathing room

        # 3. Stats Section
        layout.add_widget(Label(f"DONE: LEVEL {old_lvl}", align="^"))
        layout.add_widget(Label(f"SCORE: {score}", align="^"))
        
        # 4. Centered "LEVEL 2"
        # We add more vertical space here to make it the focus
        layout.add_widget(Label("")) 
        next_lvl = FigletText(f"LEVEL {new_lvl}", font="small")
        layout.add_widget(Label(next_lvl, height=next_lvl.max_height + 1, align="^"))
        
        # 5. Footer
        layout.add_widget(Label(""))
        layout.add_widget(Divider())
        layout.add_widget(Label("Press [ SPACE ] to continue", align="^"))

        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == ord(' '): 
                raise StopApplication("Next Level")
        return super(LevelTransitionFrame, self).process_event(event)

def play_transition(screen, old_lvl, new_lvl, score):
    scene = Scene([LevelTransitionFrame(screen, old_lvl, new_lvl, score)], -1)
    screen.play([scene], stop_on_resize=True, repeat=False)

if __name__ == "__main__":
    Screen.wrapper(lambda s: play_transition(s, 1, 2, 500))