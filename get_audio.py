
from telegram import ReplyKeyboardMarkup


import os

path = './files/audio'


def getMainButtons():

    buttons = [[i] for i in os.listdir(path)]
    # buttons.insert(0, ['🔝 Asosiy menyu'])

    return buttons


def getAudiosName(dirname):
    buttons = sorted([[i] for i in os.listdir(
        os.path.join(path, dirname))], key=lambda x: x[0].split('.')[0][-2:])

    buttons.insert(0, ['🔝 Asosiy menyu'])

    return buttons
