from unittest.mock import Mock, patch

from PIL import ImageFont
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw

from manga_dl.util.CoverManipulator import CoverManipulator


class TestCoverManipulator:

    def setup_method(self):
        self._under_test = CoverManipulator()

    @patch("manga_dl.util.CoverManipulator.ImageDraw.Draw")
    @patch("manga_dl.util.CoverManipulator.Image.open")
    def test_add_chapter_box_square(self, open_image_mock: Mock, create_draw_mock: Mock):
        self._run_calculations(100, 100, "1", open_image_mock, create_draw_mock)
        self._run_calculations(100, 100, "Text", open_image_mock, create_draw_mock)
        self._run_calculations(100, 100, "Image", open_image_mock, create_draw_mock)
        self._run_calculations(100, 100, "This is a long text", open_image_mock, create_draw_mock)

    @patch("manga_dl.util.CoverManipulator.ImageDraw.Draw")
    @patch("manga_dl.util.CoverManipulator.Image.open")
    def test_add_chapter_box_square_horizontal_rectangle(self, open_image_mock: Mock, create_draw_mock: Mock):
        self._run_calculations(200, 100, "1", open_image_mock, create_draw_mock)
        self._run_calculations(200, 100, "Text", open_image_mock, create_draw_mock)
        self._run_calculations(200, 100, "Image", open_image_mock, create_draw_mock)
        self._run_calculations(200, 100, "This is a long text", open_image_mock, create_draw_mock)

    @patch("manga_dl.util.CoverManipulator.ImageDraw.Draw")
    @patch("manga_dl.util.CoverManipulator.Image.open")
    def test_add_chapter_box_square_vertical_rectangle(self, open_image_mock: Mock, create_draw_mock: Mock):
        self._run_calculations(100, 200, "1", open_image_mock, create_draw_mock)
        self._run_calculations(100, 200, "Text", open_image_mock, create_draw_mock)
        self._run_calculations(100, 200, "Image", open_image_mock, create_draw_mock)
        self._run_calculations(100, 200, "This is a long text", open_image_mock, create_draw_mock)

    def _run_calculations(self, width: int, height: int, text: str, open_image_mock: Mock, create_draw_mock: Mock):
        image_mock = self._create_image_mock(width, height)
        draw_mock = self._create_draw_mock()

        open_image_mock.return_value = image_mock
        create_draw_mock.return_value = draw_mock

        self._under_test.add_chapter_box(b"", text)

        max_text_width = int(width / 5)
        max_text_height = int(max_text_width / 2.5)
        box_padding = int(max_text_width / 5)
        fontsize = min(int(max_text_width / len(text)), max_text_height)

        assert len(draw_mock.textsize.mock_calls) == max_text_width - fontsize + 2
        assert draw_mock.textsize.mock_calls[-1].kwargs["font"].size == fontsize

        expected_box_coords = (
            width - max_text_width - box_padding * 2,
            height - max_text_height - box_padding * 2,
            width + 10,
            height + 10
        )
        expected_text_coords = (
            expected_box_coords[0] + box_padding + int((max_text_width - len(text) * fontsize) / 2),
            expected_box_coords[1] + box_padding + int((max_text_height - fontsize) / 2)
        )

        draw_mock.rounded_rectangle.assert_called_once()
        draw_mock.text.assert_called_once()
        assert draw_mock.rounded_rectangle.call_args[0][0] == expected_box_coords
        assert draw_mock.text.call_args[0][0] == expected_text_coords

    def _create_image_mock(self, width: int, height: int) -> Mock:
        image = Mock(Image)
        image.format = "jpeg"
        image.height = height
        image.width = width
        image.save.return_value = None
        return image

    def _create_draw_mock(self) -> Mock:
        def textsize(text: str, font: ImageFont):
            return len(text) * font.size, font.size

        draw = Mock(ImageDraw)
        draw.textsize.side_effect = textsize
        return draw
