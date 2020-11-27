from math import ceil, floor

from flask import Flask, request, render_template

from decimal import Decimal
from decimal import InvalidOperation
import re

app = Flask(__name__)

UPPER_BOUND = Decimal("1000000000000000.00")
LOWER_BOUND = Decimal("-1000000000000000.00")


def check_format(number: str) -> bool:
    """If is match return True else False."""
    count_space = 0  # Количество пробелов

    if number.replace(' ', '') == number:
        return True

    index_of_comma = number.find('.')

    if number[index_of_comma - 1] == ' ' or number[index_of_comma + 1] == ' ':
        return False

    for digit in number:
        if digit == '\t' or count_space >= 2:
            return False
        elif digit == ' ':
            count_space += 1
        else:
            count_space = 0

    number = number.split('.')

    try:
        digits_number_after_comma = number[1].split(' ')
        digits_number_before_comma = number[0].split(' ')
    except IndexError:
        for i, group in enumerate(number):
            if i == 0:  # first rank
                if len(group) > 3:
                    return False
            else:
                if len(group) != 3:
                    return False

        return True

    for i, group in enumerate(digits_number_before_comma):
        if i == 0:  # first rank
            if len(group) > 3:
                return False
        else:
            if len(group) != 3:
                return False

    if len(digits_number_after_comma) > 1:
        return False

    return True



@app.route('/')
def main_page():
    return render_template('entry.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    first_number = ((request.form['first number']).replace(',', '.'))
    second_number = ((request.form['second number']).replace(',', '.'))

    exp_form = "^([0-9]+[.]?[0-9]*|[0-9]*[.][0-9]+)[eE][+-]?[0-9]+$"

    comp = re.compile(exp_form)

    if comp.match(first_number) or comp.match(second_number):
        return render_template('error_exp.html',
                               first_number=first_number,
                               second_number=second_number)

    if not check_format(first_number) or not check_format(second_number):
        return render_template('error_res_range.html',
                               error_message='INVALID FORMAT!',
                               result='Error')
    else:
        first_number = first_number.replace(' ', '')
        second_number = second_number.replace(' ', '')

    try:
        first_number = Decimal(first_number)
        second_number = Decimal(second_number)
    except InvalidOperation:
        return render_template('error_res_range.html',
                               error_message='You need to enter numbers!',
                               result='Error')

    # check format with spaces!

    if (first_number.compare(LOWER_BOUND) == Decimal('-1') or first_number.compare(UPPER_BOUND) == Decimal('1')) \
            or (second_number.compare(LOWER_BOUND) == Decimal('-1') or second_number.compare(UPPER_BOUND) == Decimal('1')):
        return render_template('error_exp.html',
                               first_number=first_number,
                               second_number=second_number)

    if request.form.get('sum') is not None:
        result = first_number + second_number

    if request.form.get('diff') is not None:
        result = first_number - second_number

    if request.form.get('composition') is not None:
        result = first_number * second_number

    if request.form.get('division') is not None:
        try:
            result = first_number / second_number
        except ZeroDivisionError:
            return render_template('error_res_range.html',
                                   error_message='You cannot divide by zero!',
                                   result='Error')

    if result.compare(LOWER_BOUND) == Decimal('-1') or result.compare(UPPER_BOUND) == Decimal('1'):
        return render_template('error_res_range.html',
                               error_message='Error! Result must be between 1 000 000 000 000 000.00 and -1 000 000 '
                                             '000 000 000.00',
                               result=result)

    # result = "%.6f" % result
    result = ceil(result * 1000000) / 1000000.0

    result = f'{result:,}'.replace(',', ' ')

    # result = re.sub(r'((\d)[ ]*(\d))*', r'\1\2', result)

    return render_template('result.html',
                           first_number=first_number,
                           second_number=second_number,
                           result=result)


if __name__ == '__main__':
    app.run()
