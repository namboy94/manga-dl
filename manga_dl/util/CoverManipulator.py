from io import BytesIO
from typing import Tuple

from PIL import Image, ImageFont, ImageDraw
from matplotlib import font_manager


class CoverManipulator:
    FONT_NAME = font_manager.FontProperties(family="sans-serif", weight="bold")

    def add_chapter_box(self, image_bytes: bytes, text: str) -> bytes:
        image = Image.open(BytesIO(image_bytes))
        image_format = image.format
        drawing = ImageDraw.Draw(image)

        self._draw_box(image, drawing)
        font_size = self._calculate_font_size(image, drawing, text)
        self._draw_text(image, drawing, text, font_size)

        edited = BytesIO()
        image.save(edited, format=image_format)
        return edited.getvalue()

    @staticmethod
    def _calculate_dimensions(image: Image) -> Tuple[int, int, int, int, int]:
        text_max_width = int(image.width / 5)
        text_max_height = int(text_max_width / 2.5)
        box_padding = int(text_max_width / 5)
        box_width = text_max_width + box_padding * 2
        box_height = text_max_height + box_padding * 2
        return text_max_width, text_max_height, box_padding, box_width, box_height

    def _calculate_font_size(self, image: Image, drawing: ImageDraw, text: str) -> int:
        max_width, max_height, _, _, _ = self._calculate_dimensions(image)
        calculated_font_size = max_width

        width, height = self._calculate_text_size(drawing, text, calculated_font_size)
        while width > max_width or height > max_height:
            calculated_font_size -= 1
            width, height = self._calculate_text_size(drawing, text, calculated_font_size)

        return calculated_font_size

    def _draw_box(self, image: Image, drawing: ImageDraw):
        box_x_anchor, box_y_anchor = self._calculate_box_anchors(image)
        corner_remover = 10

        coordinates = (box_x_anchor, box_y_anchor, image.width + corner_remover, image.height + corner_remover)
        drawing.rounded_rectangle(coordinates, fill="gray", outline="black", width=5, radius=20)

    def _calculate_box_anchors(self, image: Image) -> Tuple[int, int]:
        _, _, _, box_width, box_height = self._calculate_dimensions(image)
        return image.width - box_width, image.height - box_height

    def _draw_text(self, image: Image, drawing: ImageDraw, text: str, font_size: int):
        max_width, max_height, box_padding, _, _ = self._calculate_dimensions(image)
        text_width, text_height = self._calculate_text_size(drawing, text, font_size)
        x_padding = box_padding + int((max_width - text_width) / 2)
        y_padding = box_padding + int((max_height - text_height) / 2)

        box_x_anchor, box_y_anchor = self._calculate_box_anchors(image)
        text_x_anchor = box_x_anchor + x_padding
        text_y_anchor = box_y_anchor + y_padding

        coordinates = (text_x_anchor, text_y_anchor)
        color = (0, 0, 0)
        font = self._create_font(font_size)
        drawing.text(coordinates, text, fill=color, font=font)

    def _create_font(self, font_size: int) -> ImageFont:
        font_file = font_manager.findfont(self.FONT_NAME)
        return ImageFont.truetype(font_file, font_size)

    def _calculate_text_size(self, drawing: ImageDraw, text: str, font_size: int) -> Tuple[int, int]:
        return drawing.textsize(text, font=self._create_font(font_size))
