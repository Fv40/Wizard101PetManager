import tkinter as tk
from pathlib import Path
from typing import Optional

try:
    from PIL import Image, ImageTk
except Exception as exc:
    raise SystemExit(
        "Pillow is required. Please install with: pip install -r requirements.txt\n"
        f"Original error: {exc}"
    )

class BackgroundFrame(tk.Frame):
    """
    Scales the bottom and top background images to the window and adjusts itself on resize. 
    The bottom image is just streched to fill but the top image will be duplicated horizontally to fill new space
    """

    def __init__(
        self,
        master: tk.Misc,
        top_image_path: str | Path,
        bottom_image_path: str | Path,
        background_hex_color: str = "#3058af",
        **kwargs,
    ) -> None:
        super().__init__(master, bg=background_hex_color, bd=0, highlightthickness=0, **kwargs)

        self.background_hex_color = background_hex_color

        self.top_image_path = Path(top_image_path)
        self.bottom_image_path = Path(bottom_image_path)

        self.top_image_original: Image.Image = self._open_image(self.top_image_path)
        self.bottom_image_original: Image.Image = self._open_image(self.bottom_image_path)

        # Create labels for top and bottom banners, and the colored background to blend the images together
        self.top_label = tk.Label(self, bd=0, highlightthickness=0, bg=self.background_hex_color)
        self.bottom_label = tk.Label(self, bd=0, highlightthickness=0, bg=self.background_hex_color)
        self.middle_frame = tk.Frame(self, bg=self.background_hex_color, bd=0, highlightthickness=0)

        # Keep references to the photos to prevent them from being garbage collected
        self._top_photo: Optional[ImageTk.PhotoImage] = None
        self._bottom_photo: Optional[ImageTk.PhotoImage] = None

        # Initial layout and resize handling
        self._relayout()
        self.bind("<Configure>", self._on_window_size_update)
        self._pending_resize_after_id: Optional[str] = None

    @staticmethod
    def _open_image(path: Path) -> Image.Image:
        if not path.exists():
            raise FileNotFoundError(f"Asset not found: {path}")
        img = Image.open(path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        return img

    def _on_window_size_update(self, _event: tk.Event) -> None:
        if self._pending_resize_after_id is not None:
            try:
                self.after_cancel(self._pending_resize_after_id)
            except Exception:
                pass
        self._pending_resize_after_id = self.after(10, self._relayout)

    def _relayout(self) -> None:
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)

        # Top banner height stays as original pixels relative to current height
        top_px_h = self.top_image_original.height
        top_rel_h = min(top_px_h / height, 1.0)

        # Bottom banner height scales with width to preserve aspect ratio
        bottom_scaled_h = self._scaled_height_for_width(self.bottom_image_original, width)
        relheight_bottom = min(bottom_scaled_h / height, 1.0)
        relheight_middle = max(0.0, 1.0 - top_rel_h - relheight_bottom)

        # Prepare images
        top_tiled = self._tile_top_horizontally(self.top_image_original, width)
        bottom_resized = self.bottom_image_original.resize(
            (width, max(int(relheight_bottom * height), 1)), Image.LANCZOS
        )

        self._top_photo = ImageTk.PhotoImage(top_tiled)
        self._bottom_photo = ImageTk.PhotoImage(bottom_resized)

        # Apply to widgets
        self.top_label.configure(image=self._top_photo, bg=self.background_hex_color)
        self.bottom_label.configure(image=self._bottom_photo, bg=self.background_hex_color)

        # Place using relative geometry
        self.top_label.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=top_rel_h)
        self.bottom_label.place(relx=0.0, rely=max(0.0, 1.0 - relheight_bottom), relwidth=1.0, relheight=relheight_bottom)
        self.middle_frame.configure(bg=self.background_hex_color)
        self.middle_frame.place(relx=0.0, rely=top_rel_h, relwidth=1.0, relheight=relheight_middle)

    @staticmethod
    def _scaled_height_for_width(image: Image.Image, target_width: int) -> int:
        width, height = image.size
        if width <= 0:
            return height
        scale = target_width / float(width)
        return max(int(height * scale), 1)

    @staticmethod
    def _tile_top_horizontally(image: Image.Image, target_width: int) -> Image.Image:
        tile_width, tile_height = image.size
        if target_width <= tile_width:
            return image.crop((0, 0, target_width, tile_height))
        canvas = Image.new("RGBA", (target_width, tile_height), (0, 0, 0, 0))
        x = 0
        while x < target_width:
            remaining = target_width - x
            if remaining >= tile_width:
                canvas.paste(image, (x, 0))
                x += tile_width
            else:
                canvas.paste(image.crop((0, 0, remaining, tile_height)), (x, 0))
                x = target_width
        return canvas

    def get_content_frame(self) -> tk.Frame:
        """Expose the middle frame for user content placement."""
        return self.middle_frame


