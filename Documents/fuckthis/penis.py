import wx
import random
import webbrowser

class DogSprite(wx.Frame):
    def __init__(self, image_path):
        # Loading walking left sprites
        self.sprites_left = [wx.Image(f"tile00{i}.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap() for i in range(4, 8)]
        # Loading walking right sprites
        self.sprites_right = [wx.Image(f"tile{i:03}.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap() for i in range(8, 12)]
        # Loading hover sprite
        self.sprite_hover = wx.Image("tile012.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()

        # Set initial sprite
        self.dog_image = wx.Image(image_path, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.sprite_index = 0

        self.should_move = True
        self.last_direction = None  # Track the last direction of movement

        # Screen dimensions
        #WIDTH, HEIGHT = self.dog_image.GetWidth(), self.dog_image.GetHeight()
        WIDTH, HEIGHT = 50, 50

        # Create the window
        super().__init__(None, -1, size=(WIDTH, HEIGHT), style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP | wx.FRAME_SHAPED)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint) # this draws the cat
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetShape)  # makes the cat not tweak

        # Bind events for mouse hover and click
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_click)

        # Timer for sprite cycling
        self.sprite_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_sprite, self.sprite_timer)
        self.sprite_timer.Start(100)  # update sprite every 100 milliseconds
        
        self.Show()

        # Schedule movement
        self.crawl_along_bottom()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        # Use Graphics Context to support alpha transparency
        gc = wx.GraphicsContext.Create(dc)
        gc.DrawBitmap(self.dog_image, 0, 0, self.dog_image.GetWidth(), self.dog_image.GetHeight())


    def SetShape(self, event=None):
        """Set the shape of the window to match the image's alpha channel."""
        r = wx.RegionFromBitmapTransparency(self.dog_image)
        self.SetBackgroundStyle(wx.BG_STYLE_TRANSPARENT)
        self.SetShape(r)



    def crawl_along_bottom(self):
        """Make the dog crawl along the bottom of the screen."""
        if not self.should_move:
            return
        
        screen_width, screen_height = wx.DisplaySize()
        
        # Current position
        current_x, _ = self.GetPosition()

        # If the sprite is too close to the left edge, force direction to right
        if current_x <= 10:
            direction = 1
        # If the sprite is too close to the right edge, force direction to left
        elif current_x >= screen_width - self.dog_image.GetWidth() - 10:
            direction = -1
        else:
            direction = random.choice([-1, 1])


        if direction == -1:
            self.current_sprites = self.sprites_left
        else:
            self.current_sprites = self.sprites_right

        # Reset the sprite index and update the image immediately
        self.sprite_index = 0
        self.dog_image = self.current_sprites[self.sprite_index]
        self.Refresh()

        # Decide how far to move (e.g., between 10 and 100 pixels)
        total_distance = random.randint(10, 100)

        target_x = current_x + direction * total_distance
        target_x = max(0, min(target_x, screen_width - self.dog_image.GetWidth()))

        distance_per_step = direction * 5

        self.last_direction = direction

        def move_step(_=None):
            current_x, _ = self.GetPosition()
            new_x = current_x + distance_per_step
            if (direction == 1 and new_x < target_x) or (direction == -1 and new_x > target_x):
                y = screen_height - self.dog_image.GetHeight()
                self.SetPosition((new_x, y))
                wx.CallLater(50, move_step)  # move every 50 milliseconds
            else:
                # Once target is reached, set standing sprite based on last direction
                if self.last_direction == -1:
                    self.dog_image = wx.Image("tile006.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                else:
                    self.dog_image = wx.Image("tile010.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                self.Refresh()

                # Schedule the next crawl with a random delay
                delay = random.randint(1000, 4000)  # milliseconds
                wx.CallLater(delay, self.crawl_along_bottom)

                # Reset the current_sprites to idle sprites
                self.current_sprites = [self.dog_image]


        move_step(0)

    def update_sprite(self, event):
        self.sprite_index = (self.sprite_index + 1) % len(self.current_sprites)
        self.dog_image = self.current_sprites[self.sprite_index]
        self.Refresh()  # Trigger a repaint of the window

    def on_mouse_enter(self, event):
        """Pause movement when mouse enters the window."""
        self.should_move = False
        self.dog_image = self.sprite_hover
        self.Refresh()

    def on_mouse_leave(self, event):
        """Resume movement when mouse leaves the window."""
        self.should_move = True
        if self.last_direction == -1:
            self.dog_image = wx.Image("tile006.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        else:
            self.dog_image = wx.Image("tile010.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.Refresh()
        self.crawl_along_bottom()

    def on_mouse_click(self, event):
        """Handle click event to show prompts."""
        dlg = wx.TextEntryDialog(self, "What would you like to search?", "Search Google")
        if dlg.ShowModal() == wx.ID_OK:
            query = dlg.GetValue()
            webbrowser.open(f"https://www.google.com/search?q={query}")
        dlg.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    sprite = DogSprite('tile000.png')
    app.MainLoop()