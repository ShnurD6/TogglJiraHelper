import unittest

from common import format_time, get_key_by_description


class CommonTests(unittest.TestCase):
    def test_format_time(self):
        self.assertEqual(format_time(0), "0s")
        self.assertEqual(format_time(1), "1s")
        self.assertEqual(format_time(59), "59s")
        self.assertEqual(format_time(61), "1m 1s")
        self.assertEqual(format_time(121), "2m 1s")
        self.assertEqual(format_time(12345), "3h 25m 45s")

    def test_get_key_by_description(self):
        self.assertEqual(get_key_by_description("Dev Status"), "ORG-7")
        self.assertEqual(get_key_by_description("1n1 с Петром"), "ORG-7")
        self.assertEqual(get_key_by_description("COR StandUP"), "ORG-7")
        self.assertEqual(get_key_by_description("DEMO и подготовка к нему"), "ORG-7")
        self.assertEqual(get_key_by_description("Готовился к ретро"), "ORG-7")
        self.assertEqual(get_key_by_description("Готовился к retro"), "ORG-7")
        self.assertEqual(get_key_by_description("COR Week Retro"), "ORG-7")
        self.assertEqual(get_key_by_description("Подготовка к 1n1 с Борисом"), "ORG-7")
        self.assertEqual(get_key_by_description("Mob Status"), "ORG-7")
        self.assertEqual(get_key_by_description("Разбор беклога"), "ORG-7")
        self.assertEqual(get_key_by_description("Смотрели с Валерой беклог"), "ORG-7")

        self.assertEqual(get_key_by_description("Собес с Алексеем"), "ORG-2")
        self.assertEqual(get_key_by_description("Вечернее собеседование"), "ORG-2")
        self.assertEqual(get_key_by_description("Коммент по собесу"), "ORG-2")
        self.assertEqual(get_key_by_description("Смотрел отклики"), "ORG-2")
        self.assertEqual(get_key_by_description("Обсуждали отклик"), "ORG-2")

        self.assertEqual(get_key_by_description("BUS-4132 Ревью ПР"), "BUS-4132")
        self.assertEqual(get_key_by_description("Ревью ПР SUP-431"), "SUP-431")
        self.assertEqual(get_key_by_description("Делал FRONT-12345 задачу"), "FRONT-12345")


if __name__ == '__main__':
    unittest.main()
