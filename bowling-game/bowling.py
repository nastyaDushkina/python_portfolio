from abc import abstractmethod, ABC


class Throw(ABC):
    def __init__(self, game):
        self.game = game
        self.result = self.game.game_result[0] if self.game.game_result else None

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def additional_process_throw(self):
        pass

    def get_next_throw(self):
        self.game.game_result = self.game.game_result[1:]
        if self.game.current_frame:
            self.game.throw(SecondThrowInFrame(self.game))
        else:
            self.game.throw(FirstThrowInFrame(self.game))

    def process_throw_not_spare(self, next_result):
        if next_result in ['X', 'Х']:
            self.game.sum_of_points += 10
        elif next_result.isnumeric():
            self.game.sum_of_points += int(next_result)


class FirstThrowInFrame(Throw):
    def get_score(self):
        if not self.result:
            return
        elif self.result == '/':
            raise ValueError('нельзя выбить spare с первого броска во фрейме')

        if self.result in ['X', 'Х']:
            self.process_throw_result(strike=True)
        else:
            self.process_throw_result()

    def process_throw_result(self, strike=False):
        if strike:
            if self.game.production:
                self.game.sum_of_points += 10
                self.additional_process_throw()
            else:
                self.game.sum_of_points += 20
            self.game.frame_list.append('STRIKE')
        else:
            self.game.current_frame = self.result

        self.get_next_throw()

    def additional_process_throw(self):
        try:
            next_result = self.game.game_result[1:3]
            if next_result[-1] == '/':
                self.game.sum_of_points += 10
            elif 'X' or 'Х' in next_result:
                for element in next_result:
                    self.process_throw_not_spare(element)
            else:
                self.game.sum_of_points += sum(int(symbol) for symbol in self.game.current_frame if symbol.isnumeric())
        except Exception:
            try:
                next_result = self.game.game_result[1]
                self.process_throw_not_spare(next_result)
            except Exception:
                return


class SecondThrowInFrame(Throw):
    def get_score(self):
        if not self.result:
            raise ValueError('во фрейме должно быть два броска')

        if self.result in ['X', 'Х']:
            raise ValueError('нельзя выбить strike со второго броска во фрейме')

        self.game.current_frame += self.result

        if self.result == '/':
            if self.game.production:
                sum_frame_points = 10
                self.additional_process_throw()
            else:
                sum_frame_points = 15
            frame_result = 'SPARE'
        else:
            frame_result = self.game.current_frame
            sum_frame_points = sum(int(symbol) for symbol in self.game.current_frame if symbol.isnumeric())

            if sum_frame_points > 10:
                raise ValueError('за один фрейм не может быть сбито больше 10 кегель')
            elif sum_frame_points == 10:
                raise ValueError('некорректная запись. Количество очков во фрейме не может равняться 10. Это SPARE!')

        self.game.sum_of_points += sum_frame_points
        self.game.frame_list.append(frame_result)
        self.game.current_frame = ''
        self.get_next_throw()

    def additional_process_throw(self):
        try:
            next_result = self.game.game_result[1]
            self.process_throw_not_spare(next_result)
        except Exception:
            return


class Game:
    def __init__(self, production=False):
        self.frame_list = []
        self.sum_of_points = 0
        self.current_frame = ''
        self.production = production

    def go(self, game_result):
        self.game_result = game_result
        game_score = self.throw(FirstThrowInFrame(self))
        # print(f'Фреймы в игре: {self.frame_list}')
        return game_score

    def throw(self, throw):
        self.frame_throw = throw
        self.frame_throw.get_score()
        return self.sum_of_points
