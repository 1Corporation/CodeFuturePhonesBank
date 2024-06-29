import unittest


NOT_ALLOWED_SYMBOLS = "() -+"


def phone_serializer(phone: str) -> str:
    for symbol in NOT_ALLOWED_SYMBOLS:
        phone = phone.replace(symbol, "")

    phone = phone.replace("+7", "")

    if phone[0] == "7" or phone[0] == "8":
        phone = phone[1:]

    return phone


def fsc_serializer(fsc: str) -> str:
    return fsc.lower()


class TestSerializers(unittest.TestCase):

    def test_phone_serializer(self):
        self.assertEqual(phone_serializer("+7 (123) 456-78-90"), "1234567890")
        self.assertEqual(phone_serializer("8 (123) 456-78-90"), "1234567890")
        self.assertEqual(phone_serializer("7 (123) 456-78-90"), "1234567890")
        self.assertEqual(phone_serializer("(123) 456-78-90"), "1234567890")
        self.assertEqual(phone_serializer("123-456-78-90"), "1234567890")
        self.assertEqual(phone_serializer("123 456 78 90"), "1234567890")
        self.assertEqual(phone_serializer("1234567890"), "1234567890")
        self.assertEqual(phone_serializer("+7-812-345-67-89"), "8123456789")

    def test_fsc_serializer(self):
        self.assertEqual(fsc_serializer("ABC123"), "abc123")
        self.assertEqual(fsc_serializer("abc123"), "abc123")
        self.assertEqual(fsc_serializer("AbC123"), "abc123")
        self.assertEqual(fsc_serializer("ABC"), "abc")
        self.assertEqual(fsc_serializer("123"), "123")


if __name__ == "__main__":
    unittest.main()