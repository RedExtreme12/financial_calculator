from flask import Flask, request, render_template

from decimal import Decimal
import re

app = Flask(__name__)

UPPER_BOUND = Decimal("1000000000000000.00")
LOWER_BOUND = Decimal("-1000000000000000.00")


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

    first_number = Decimal(first_number)
    second_number = Decimal(second_number)

    if (first_number.compare(LOWER_BOUND) == Decimal('-1') or first_number.compare(UPPER_BOUND) == Decimal('1')) \
            or (second_number.compare(LOWER_BOUND) == Decimal('-1') or second_number.compare(UPPER_BOUND) == Decimal('1')):
        return render_template('error_exp.html',
                               first_number=first_number,
                               second_number=second_number)

    if request.form.get('sum') is not None:
        result = first_number + second_number

    if request.form.get('diff') is not None:
        result = first_number - second_number

    if result.compare(LOWER_BOUND) == Decimal('-1') or result.compare(UPPER_BOUND) == Decimal('1'):
        return render_template('error_res_range.html',
                               result=result)

    return render_template('result.html',
                           first_number=first_number,
                           second_number=second_number,
                           result=result)


if __name__ == '__main__':
    app.run()
