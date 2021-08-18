# -*- coding: utf-8 -*-


def log_errors(error_data):
    def log_errors_wrap(func):
        with open(error_data, mode='w+', encoding="utf-8") as error_data_file:
            error_data_file.write(
                f'{"function name":^15}| {"type of error":^20}| {"error description":^50} | call parameters  \n')
            error_data_file.write('-' * 15 + '+' + '-' * 21 + '+' + '-' * 52 + '+' + '-' * 35 + '\n')

        def surrogate(*args, **kwargs):
            try:
                execution_result = func(*args, **kwargs)
            except Exception as exc:
                with open(error_data, mode='a', encoding="utf-8") as error_data_file:
                    error_data_file.write(
                        f'{str(func.__name__):<15}| {str(exc.__class__)[7:-1]:<20}| '
                        f'{str(exc):<50} | {args}, {kwargs}\n')
                raise exc
            else:
                return execution_result

        return surrogate

    return log_errors_wrap


@log_errors('function_errors.log')
def perky(param):
    return param / 0


@log_errors('function_errors.log')
def check_line(line):
    name, email, age = line.split(' ')
    if not name.isalpha():
        raise ValueError("it's not a name")
    if '@' not in email or '.' not in email:
        raise ValueError("it's not a email")
    if not 10 <= int(age) <= 99:
        raise ValueError('Age not in 10..99 range')


lines = [
    'Ярослав bxh@ya.ru 600',
    'Земфира tslzp@mail.ru 52',
    'Тролль nsocnzas.mail.ru 82',
    'Джигурда wqxq@gmail.com 29',
    'Земфира 86',
    'Равшан wmsuuzsxi@mail.ru 35',
]
for line in lines:
    try:
        check_line(line)
    except Exception as exc:
        print(f'Invalid format: {exc}')

perky(param=42)
