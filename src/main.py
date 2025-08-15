import tkinter as tk
from pathlib import Path

from background import BackgroundFrame

"""
This file handles the window itself and what is displayed on it.
"""

class PetManager(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("PetManager")
        self.geometry("1000x700")

        # Get assets paths
        self_path = Path(__file__).resolve()
        assets_dir = (self_path.parent / ".." / "assets").resolve()
        top_image_path = assets_dir / "background_top.png"
        bottom_image_path = assets_dir / "background_bottom.png"
        icon_png_path = assets_dir / "icon.png"

        # Set window icon
        try:
            self._icon_image = tk.PhotoImage(file=str(icon_png_path))
            self.iconphoto(True, self._icon_image)
        except Exception:
            # If icon cannot be loaded (might occur on linux, TODO fix on linux pls), continue without failing the app
            pass

        # Create and place background to align with top and bottom images
        self.background = BackgroundFrame(
            self,
            top_image_path=str(top_image_path),
            bottom_image_path=str(bottom_image_path),
            background_hex_color="#3058af",
        )
        self.background.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

def main() -> None:
    app = PetManager()
    app.mainloop()

if __name__ == "__main__":
    main()