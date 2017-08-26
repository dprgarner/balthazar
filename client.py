# -*- coding: utf-8 -*-
from os import path
import argparse
import hashlib
import json
import numpy as np

from websocket import create_connection


class Client(object):
    def __init__(self):
        self.set_args()
        self.connect()

    def send(self, msg):
        """
        All messages to the server must be JSON-serialisable.
        """
        msg_str = json.dumps(msg)
        self.ws.send(msg_str)

    def recv(self):
        """
        All messages from the server are valid JSON.
        """
        msg = self.ws.recv()
        return (
            json.loads(msg)
            if msg
            else msg
        )

    def set_args(self):
        parser = argparse.ArgumentParser(
            description='Python Client for Aoire'
        )
        parser.add_argument(
            '--hostname',
            type=str,
            required=True,
            help='The location of the server, e.g. "localhost:3000".',
        )
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='The bot name and owner, e.g. "BotName (by David)".',
        )
        parser.add_argument(
            '--room',
            type=str,
            required=True,
            help='Where you agree to meet with another player.',
        )
        parser.add_argument(
            '--ngames',
            type=int,
            default=6,
            help='The number of consecutive games to play.',
        )
        parser.add_argument(
            '--heuristic',
            type=str,
            default='default',
            help='Choose a particular heuristic.',
        )
        args = parser.parse_args()
        for k, v in args._get_kwargs():
            setattr(self, k, v)

    def recv_type(self, *types):
        """
        Assert that the correct message is received.
        """
        msg = self.recv()
        assert msg, 'Websocket closing'
        assert msg['type'] in types, '{} not in types: {}'.format(msg, types)
        return msg

    def connect(self):
        try:
            self.wins = 0
            self.losses = 0
            self.draws = 0

            self.ws = create_connection('ws://{}/game'.format(self.hostname))
            print('Bot connected - waiting to start game...')
            self.send({
                'type': 'StartGame',
                'room': self.room,
                'userAgent': self.user,
                'gameType': self.GAME_TYPE,
                'nGames': self.ngames,
            })
            self.index = self.recv_type('YouAre')['index']

            for i in range(self.ngames):
                self.recv_type('Started')
                print('Game {} started'.format(i + 1))
                winner = self.play_game((self.index + i) % 2 == 0)
                if winner == -2:
                    print('The game was a draw.')
                    self.draws += 1
                elif self.index == winner:
                    print('Your bot has won the game.')
                    self.wins += 1
                else:
                    print('Your bot has lost the game.')
                    self.losses +=1
                print('{} - {}{}'.format(
                    self.wins,
                    self.losses,
                    ' ({} draws)'.format(self.draws) if self.draws else ''
                ))
        finally:
            if hasattr(self, 'ws') and self.ws.connected:
                self.ws.close()

    def play_game(self, is_first_player, player_colour):
        raise NotImplementedError()


class GomokuBase(Client):
    SIZE = 15
    GAME_TYPE = 'Gomoku'

    def render_state(self, state, is_player_black):
        """
        Return a pretty string representation of the board.
        """
        MOVES_STR = {
            -1 if is_player_black else 1: '██',
            0: '  ',
            1 if is_player_black else -1: '▒▒',
        }

        numbers = '   ' + ''.join(
            str(i) + (' ' if i < 10 else '')
            for i in range(self.SIZE)
        )
        top = '  ╔' + ('══' * self.SIZE) + '╗'
        bottom = '  ╚' + ('══' * self.SIZE) + '╝'

        collated_string = '{}\n{}\n{}\n{}'.format(
            numbers,
            top,
            '\n'.join([
                '{}║{}║'.format(
                    (' ' if i < 10 else '') + str(i),
                    ''.join([
                        MOVES_STR[state[i, j]]
                        for j in range(self.SIZE)
                    ]),
                )
                for i in range(self.SIZE)
            ]),
            bottom,
        )
        return collated_string

    def play_game(self, is_first_player):
        """
        A simple memoryless implementation of a Gomoku game-playing bot.
        Modify this if you want to do something fancy.
        (The first player is -1, the second player is 1).
        """
        state = np.zeros((self.SIZE, self.SIZE), dtype=int)
        turn_number = 0
        player_number = -1 if is_first_player else 1

        print('Your bot is playing {} ({})'.format(
            'first' if is_first_player else 'second',
            'black' if self.index == 0 else 'white'
        ))
        try:
            for turn_number in range(self.SIZE * self.SIZE):
                is_my_turn = bool(turn_number % 2) != is_first_player

                if is_my_turn:
                    # From the perspective of the brain, the bot is always 1,
                    # and the opponent -1.
                    (i, j) = self.play_turn(state)
                    self.send({'type': 'Move', 'move': int(15 * i + j)})

                update = self.recv_type('PlayerMove')
                (i, j) = update['move'] // self.SIZE, update['move'] % self.SIZE
                state[i, j] = 1 if is_my_turn else -1
                if 'winner' in update:
                    return update.get('winner')
        finally:
            print(self.render_state(state, self.index == 0))
