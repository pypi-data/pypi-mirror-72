"""
Home to the entry point for ConWech's command line interface.
"""

# future imports
from __future__ import print_function

# built-in modules
import sys
import pyperclip
import colorama
import argparse

# project modules
import conwech


def read(text, copy=False):
    """ For internal use only! """
    result = conwech.text2number(text=text)

    if copy:
        pyperclip.copy(result)

    print(result)


def spell(number, copy=False):
    """ For internal use only! """
    result = conwech.number2text(number=number)

    if copy:
        pyperclip.copy(result)

    message = list()
    for word in result.split(' '):
        if word in ('hundred',) + conwech.NATURAL_NUMBERS_LT_100:
            message.append(colorama.Fore.LIGHTBLACK_EX + word)
        elif word in ('negative', 'and'):
            message.append(colorama.Fore.YELLOW + word)
        else: # (period names)
            message.append(colorama.Fore.RESET + word)

    message = ' '.join(message)
    print(message)


def four(number, copy=False):
    """ For internal use only! """
    result = spelling = str()

    while spelling != 'four':
        try:
            spelling = conwech.number2text(number)
            number = len(spelling.replace('-', '').replace(' ', ''))
            print('There are ', colorama.Fore.CYAN, str(number), colorama.Fore.RESET,
                  ' letters in ', colorama.Fore.LIGHTBLACK_EX, spelling, colorama.Fore.RESET, sep='')
        except ValueError as error:
            print(error)
            break

    if copy:
        pyperclip.copy(result)


# because Windows is just the wrong kind of special
if sys.platform == 'win32':
    colorama.init()

# reusable copy option
copy_option = argparse.ArgumentParser(add_help=False)
copy_option.add_argument(
    '-c', '--copy', action='store_true',
    help='copy output to clipboard')

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(metavar='SUBCOMMAND')

read_command = commands.add_parser(
    'read', parents=[copy_option],
    help='convert text to number')
read_command.add_argument(
    'text', type=str,
    help='text of a number to read')
read_command.set_defaults(func=read)

spell_command = commands.add_parser(
    'spell', parents=[copy_option],
    help='convert number to text')
spell_command.add_argument(
    'number', type=str,
    help='a number to be spelled')
spell_command.add_argument(
    '-r', '--recursive', action='store_const', const=four, dest='func',
    help="spell recursively to 'four'")
spell_command.set_defaults(func=spell)


def main():
    # call func with parsed args
    inputs = vars(parser.parse_args())
    inputs.pop('func', parser.print_help)(**inputs)


if __name__ == '__main__':
    main()
