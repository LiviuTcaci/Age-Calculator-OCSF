from datetime import datetime

class Person:
    def __init__(self, birth_date_str):
        self.birth_date = self._parse_date(birth_date_str)

    def _parse_date(self, birth_date_str):
        """Parsează și validează data de naștere."""
        try:
            return datetime.strptime(birth_date_str, '%Y-%m-%d')
        except ValueError:
            return None

    def get_age(self):
        if not self.birth_date:
            return None  # Data este invalidă
        today = datetime.today()
        if self.birth_date > today:
            return None  # Data este în viitor
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age
