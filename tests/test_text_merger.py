from unittest import TestCase
from text_merger import TextMerger


SOURCE_ONE = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "Donec ut maximus ante.",
    "Nam nec mattis diam.",
    "Etiam lacinia massa dui, pretium iaculis risus ultrices in.",
    "Ut mi urna, fringilla vel justo sed, fringilla pellentesque nulla.",
    "Ut condimentum facilisis lorem, ac eleifend tortor varius et.",
    "Integer porttitor orci nec porttitor ullamcorper.",
    "Nullam non molestie nibh, varius rutrum mi."
    "Aliquam ut purus eu leo aliquam sodales.",
    "Aliquam ut purus lui leo aliquam sodales.",
]
SOURCE_TWO = [
    "Ut quis elementum nisi.",
    "Nam nec mattis diam.",
    "Etiam bibendum placerat laoreet.",
    "Sed nulla risus, imperdiet ut lacus sed, fermentum sodales ipsum.",
    "Vestibulum dapibus, magna nec mollis hendrerit, neque nunc mattis erat, id vestibulum arcu enim ut justo.",
    "Vivamus nec mi ac augue finibus placerat vel et felis.",
    "Vestibulum a magna facilisis, interdum orci sed, efficitur nibh.",
    "Aliquam ut purus eu leo aliquam sodales.",
    "Nulla et metus efficitur tellus tristique tincidunt."
]


class TextMergerTests(TestCase):
    def test_initialize(self):
        text_merger = TextMerger(3, SOURCE_ONE, SOURCE_TWO)

    def test_get_bias(self):
        text_merger = TextMerger(3, SOURCE_ONE, SOURCE_TWO)
        self.assertAlmostEqual(text_merger.get_bias('Ut', ' ','quis'), -1.0)
        self.assertAlmostEqual(text_merger.get_bias('Donec', ' ','ut'), 1.0)
        self.assertAlmostEqual(text_merger.get_bias('mattis', ' ','diam'), 0.5)
        self.assertAlmostEqual(text_merger.get_bias('ut', ' ','purus'), 1 / 3)
        self.assertAlmostEqual(text_merger.get_bias('Nam', ' ', 'nec'), 0.0)

    def test_get_properties(self):
        text_merger = TextMerger(3, SOURCE_ONE, SOURCE_TWO)
        sequence = ('', '', 'Donec', ' ', 'ut', ' ', 'purus', ' ', 'eu', ' ',
                    'leo', ' ', 'aliquam', ' ', 'sodales', '.', '')
        properties = text_merger.get_properties(*sequence)
        print(properties)
