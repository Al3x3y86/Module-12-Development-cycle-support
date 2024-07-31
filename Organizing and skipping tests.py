import unittest


class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name
        return False


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants[:]:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


def skip_test_if_frozen(test_func):
    def wrapper(self):
        if getattr(self, 'is_frozen', False):
            self.skipTest('Тесты в этом кейсе заморожены')
        else:
            return test_func(self)
    return wrapper


class RunnerTest(unittest.TestCase):
    is_frozen = False

    @skip_test_if_frozen
    def test_walk(self):
        runner = Runner("TestRunner1")
        for _ in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)

    @skip_test_if_frozen
    def test_run(self):
        runner = Runner("TestRunner2")
        for _ in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    @skip_test_if_frozen
    def test_challenge(self):
        runner1 = Runner("TestRunner1")
        runner2 = Runner("TestRunner2")
        for _ in range(10):
            runner1.run()  # 10 * 10 = 100
            runner2.walk()  # 10 * 5 = 50
        self.assertNotEqual(runner1.distance, runner2.distance)


class TournamentTest(unittest.TestCase):
    is_frozen = True

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.runner_1 = Runner("Усэйн", 10)
        self.runner_2 = Runner("Андрей", 9)
        self.runner_3 = Runner("Ник", 3)

    @classmethod
    def tearDownClass(cls):
        for race, results in cls.all_results.items():
            print(f"{race}: {results}")

    @skip_test_if_frozen
    def test_race_usain_and_nick(self):
        tournament = Tournament(90, self.runner_1, self.runner_3)
        results = tournament.start()
        self.all_results['Усэйн и Ник'] = results
        self.assertEqual(results[len(results)], self.runner_3)

    @skip_test_if_frozen
    def test_race_andrey_and_nick(self):
        tournament = Tournament(90, self.runner_2, self.runner_3)
        results = tournament.start()
        self.all_results['Андрей и Ник'] = results
        self.assertEqual(results[len(results)], self.runner_3)

    @skip_test_if_frozen
    def test_race_usain_andrey_and_nick(self):
        tournament = Tournament(90, self.runner_1, self.runner_2, self.runner_3)
        results = tournament.start()
        self.all_results['Усэйн, Андрей и Ник'] = results
        self.assertEqual(results[len(results)], self.runner_3)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
