#!/usr/bin/python3

import threading, asyncio
import re, json
import requests
import time
import traceback

from config import *
from collections import deque

from hakcbot_utilities import load_from_file

from hakcbot_init import Hakcbot
from hakcbot_threads import Threads
from hakcbot_execute import Execute
from hakcbot_spam import Spam
from hakcbot_commands import Commands

class Run:
    def __init__(self):
        self.Hakcbot = Hakcbot()

        self.Threads = Threads(self)
        self.Automate = Automate(self)
        self.Execute = Execute(self)
        self.Spam = Spam(self)
        self.Commands = Commands(self)

        self.linecount = 0

        self.online = False
        self.uptime_message = 'DOWRIGHT is OFFLINE.'

        roles = load_from_file('roles.json')
        self.mod_list = roles['user_roles']['mods']

    def start(self):
        self.Threads.start()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.main())

    async def main(self):
        await self.Hakcbot.connect()

        await self.Spam.create_tld_set()
        await self.Spam.adjust_blacklist()
        await self.Spam.adjust_whitelist()

        await asyncio.gather(self.Hakc(), self.Hakc2())

    async def Hakc(self):
        loop = asyncio.get_running_loop()
        recv_buffer =  ''
        try:
            while True:
                recv_buffer = await loop.sock_recv(self.Hakcbot.sock, 1024)
                recv_buffer = recv_buffer.decode('utf-8', 'ignore')
                chat = recv_buffer.split('\n')
                recv_buffer = chat.pop()

                for line in chat:
                    if ('PING :tmi.twitch.tv\r' == line):
                        print(line)
                        self.linecount = 0
                        await loop.sock_sendall(self.Hakcbot.sock, 'PONG :tmi.twitch.tv\r\n'.encode('utf-8'))

                    elif ('PRIVMSG' in line):
                        blocked_message, user, message = await self.Spam.main(line)
                        if (not blocked_message):
                            print(f'{user.name}: {message}')

                            await self.Execute.parse_message(user, message)
                            self.linecount += 1

                    elif ('JOIN' in line):
                        pass
                        # placeholder for when i want to track joins/ see if a user joins
        except Exception as E:
            traceback.print_exc()
            print(f'Main Process Error: {E}')

    async def Hakc2(self):
        cmds = []
        timers = []

        for t_count, cmd in enumerate(self.Commands.automated, 1):
            cmds.append(cmd)
            timers.append(self.Commands.automated[cmd]['timer'])

        try:
            await asyncio.gather(*[self.Automate.timers(cmds[t], timers[t]) for t in range(t_count)])
        except Exception as E:
            print(f'AsyncIO General Error | {E}')

    async def send_message(self, message, response=None):
        loop = asyncio.get_running_loop()
        print(f'hakcbot: {message}')
        message = f'PRIVMSG #{CHANNEL} :{message}'

        await loop.sock_sendall(self.Hakcbot.sock, f'{message}\r\n'.encode('utf-8'))
        if (response):
            response = f'PRIVMSG #{CHANNEL} :{response}'
            await loop.sock_sendall(self.Hakcbot.sock, f'{response}\r\n'.encode("utf-8"))

class Automate:
    def __init__(self, Hakcbot):
        self.Hakcbot = Hakcbot

        self.flag_for_timeout = deque()

    async def timers(self, cmd, timer):
        try:
            message = self.Hakcbot.Commands.standard_commands[cmd]['message']
            while True:
                await asyncio.sleep(60 * timer)
                print(f'Line Count: {self.Hakcbot.linecount}')
                cooldown = getattr(self.Hakcbot.Commands, f'hakc{cmd}')
                if (not cooldown and self.Hakcbot.linecount >= 3):
                    await self.Hakcbot.send_message(message)
                elif (cooldown):
                    print(f'hakcbot: {cmd} command on cooldown')
        except Exception as E:
            print(f'AsyncIO Timer Error: {E}')

    async def timeout(self):
        while True:
            if (not self.flag_for_timeout):
                await asyncio.sleep(1)
                continue

            while self.flag_for_timeout:
                user = self.flag_for_timeout.popleft()
                message = f'/timeout {user} 3600 account age less than one day.'
#            response = f'sorry {user}, accounts must be older than 1 day to talk in chat.'

                await self.Hakcbot.send_message(message)

def Main():
    Hakcbot = Run()
    Hakcbot.start()

if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
        print('Exiting Hakcbot :(')
