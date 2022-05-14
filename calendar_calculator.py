class DateCalculator:
    _MAX_MONTHS = 12
    _MAX_DAYS = 31
    _MONTH_MAP_DAYS_NOT_LEAP_YAR = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    _MONTH_MAP_DAYS_LEAP_YAR = {**_MONTH_MAP_DAYS_NOT_LEAP_YAR, 2: 29}

    def __init__(self, date):
        self._day, self._month, self._year = self._validate_parse_input_date(date)

    @classmethod
    def _validate_parse_input_date(cls, date):
        if not isinstance(date, str) or not date.replace(".", "").isdigit() or len(date.split(".")) != 3:
            raise TypeError()
        day, month, year = (int(el) for el in date.split("."))
        return day, month, year

    @staticmethod
    def __user_friendly_number(val):
        return f"0{val}" if val < 10 else val

    @property
    def date(self):
        return f"{self.__user_friendly_number(self._day)}.\
            {self.__user_friendly_number(self._month)}.{self._year}"

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, month):
        self._month = int(month)
        if self._month > self._MAX_MONTHS:
            self._month = 1
            self.__increase_one_year()

    def _days_in_month(self, month):
        return self._MONTH_MAP_DAYS_LEAP_YAR[month] \
            if self.is_leap_year \
            else self._MONTH_MAP_DAYS_NOT_LEAP_YAR[month]

    def _days_in_year(self, year):
        return 366 if self.__is_leap_year(year) else 365

    def __increase_one_year(self):
        self._year += 1

    def __increase_one_month(self):
        self.month += 1

    def __increase_days(self, val):
        pool = self._day + val
        while pool > self._days_in_year(self._year):
            pool -= self._days_in_year(self._year)
            self.__increase_one_year()
        else:
            while pool > self._days_in_month(self.month):
                pool -= self._days_in_month(self.month)
                self.__increase_one_month()
                self._day = 0
            else:
                self._day = pool

    @staticmethod
    def __is_leap_year(year):
        if year % 400 == 0:
            return True
        elif year % 100 == 0:
            return False
        elif year % 4 == 0:
            return True
        else:
            return False

    @property
    def is_leap_year(self):
        return self.__is_leap_year(self._year)

    def _concat_days(self, days):
        self.__increase_days(days)

    def __add__(self, add_value):
        if isinstance(add_value, int):
            self._concat_days(add_value)
            return self.date.replace(" ", "")
        raise NotImplemented()


if __name__ == '__main__':
    import datetime
    import unittest

    class TestDateCalculator(unittest.TestCase):
        date = "01.12.2020"
        expected_date = (
                datetime.datetime.strptime(date, "%d.%m.%Y") + datetime.timedelta(days=300)
        ).strftime("%d.%m.%Y")
        d = DateCalculator(date)

        def test_correct_calculation(self):
            self.assertEqual(self.d + 300, self.expected_date)

        def test_incorrect_calculation(self):
            self.assertNotEqual(self.d + 30, self.expected_date)

        def test_incorrect_input(self):
            with self.assertRaises(TypeError):
                d = DateCalculator("-1.13.2020")

    unittest.main()
