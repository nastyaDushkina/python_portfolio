# -*- coding: utf-8 -*-
import unittest
from bowling import Game


class BowlingTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_idle(self):
        game_score = self.game.go('------')
        self.assertEqual(game_score, 0)

    def test_strikes(self):
        game_score = self.game.go('XХXХXХX')
        self.assertEqual(game_score, 140)

    def test_spares(self):
        game_score = self.game.go('-/-/-/-/-/')
        self.assertEqual(game_score, 75)

    def test_1(self):
        game_score = self.game.go('Х4/34-4')
        self.assertEqual(game_score, 46)

    def test_2(self):
        game_score = self.game.go('--3/-/54X')
        self.assertEqual(game_score, 59)

    def test_3(self):
        game_score = self.game.go('Х-37/X--1-54')
        self.assertEqual(game_score, 68)

    def test_4(self):
        game_score = self.game.go('8/XX27-/--31')
        self.assertEqual(game_score, 83)

    def test_5(self):
        with self.assertRaises(Exception) as context:
            self.game.go('--X-/84XX-36-')
        self.assertTrue('за один фрейм не может быть сбито больше 10 кегель', str(context.exception))

    def test_6(self):
        with self.assertRaises(Exception) as context:
            self.game.go('-7-/3Х45--2/')
        self.assertTrue('нельзя выбить strike со второго броска во фрейме', str(context.exception))

    def test_8(self):
        with self.assertRaises(Exception) as context:
            self.game.go('732/--/3Х56')
        self.assertTrue('нельзя выбить spare со первого броска во фрейме', str(context.exception))

    def test_9(self):
        with self.assertRaises(Exception) as context:
            self.game.go('--5/6/23-9Х-')
        self.assertTrue('во фрейме должно быть два броска', str(context.exception))

    def test_10(self):
        with self.assertRaises(Exception) as context:
            self.game.go('8--/37/Х-6')
        self.assertTrue('некорректная запись. Количество очков во фрейме '
                        'не може равняться 10. Это SPARE!', str(context.exception))

class BowlingTestsForProduction(unittest.TestCase):
    def setUp(self):
        self.game = Game(production=True)

    def test_1(self):
        game_score = self.game.go('153/--X6/126/X')
        self.assertEqual(game_score, 80)

    def test_2(self):
        game_score = self.game.go('XXXX--1/X6/5/-3')
        self.assertEqual(game_score, 158)

    def test_3(self):
        game_score = self.game.go('-/XX-/81262/X12')
        self.assertEqual(game_score, 131)

    def test_4(self):
        game_score = self.game.go('36X12-/618/9-XX')
        self.assertEqual(game_score, 106)

    def test_5(self):
        game_score = self.game.go('X34--3/4353-5--629/')
        self.assertEqual(game_score, 76)

    def test_6(self):
        game_score = self.game.go('7/817/2/--9/8---3/21')
        self.assertEqual(game_score, 90)

if __name__ == '__main__':
    unittest.main()
