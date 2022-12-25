#!/bin/python3

import os
import sys
import socket
import config
from subprocess import Popen, PIPE
from threading import Thread


def console_in(sock):
    while True:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            commands = data.decode('utf-8').split('\r\n')
            for command in commands:
                if command != '':
                    print(command)
                    if 'PING' in command:
                        print('Sending PONG')
                        sock.send(b'PONG\r\n')

                    if 'PRIVMSG' in command:
                        cmd = command.split()
                        nick = cmd[0].split('!')[0][1:]
                        # user = cmd[0].split('!')[1].split('@')[0]
                        cmd[3] = cmd[3][1:]
                        contents = ' '.join(cmd[3:])
                        if cmd[2] == config.irc_con_channel:
                            os.system('screen -S {} -p 0 -X stuff "{}^M"'.format(config.screen_name, contents))
                        if cmd[2] == config.irc_chat_channel:
                            print("received chat message")
                            os.system('screen -S {} -p 0 -X stuff "{}^M"'.format(config.screen_name,
                                                                                 'say [IRC]<{}>: {}'.format(nick,
                                                                                                            contents)))


def console_out(stderr, sock):
    while True:
        for line in stderr:
            line_decoded = line.decode('utf-8').strip('\n')
            print(line_decoded)
            if line_decoded != '':
                if line_decoded[0] != '$':
                    sock.send(bytes('PRIVMSG {} :'.format(config.irc_con_channel), 'utf-8') + bytes(line_decoded,
                                                                                                    'utf-8') + b'\r\n')
                if line_decoded[0] == '*' or line_decoded[0] == '<':
                    sock.send(bytes('PRIVMSG {} :'.format(config.irc_chat_channel), 'utf-8') + bytes(line_decoded,
                                                                                                     'utf-8') + b'\r\n')
                for allowed in config.irc_chat_allowed:
                    if allowed in line_decoded:
                        sock.send(
                            bytes('PRIVMSG {} :'.format(config.irc_chat_channel), 'utf-8') +
                            bytes(line_decoded, 'utf-8') + b'\r\n')


def main():
    # Connect to the IRC server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((config.irc_address, config.irc_port))
    except socket.error:
        print("Could not connect to the IRC server, quitting...")
        return -1

    sock.send(b'CAP LS 302\r\n')
    sock.send(
        bytes('NICK {}\r\nUSER {} 0 * {}\r\n'.format(config.irc_nick, config.irc_username, config.irc_nick), 'utf-8'))
    sock.send(bytes('JOIN {} {}\r\n'.format(config.irc_con_channel, config.irc_con_channel_password), 'utf-8'))
    sock.send(bytes('TOPIC {} :{}\r\n'.format(config.irc_con_channel, config.irc_con_channel_topic), 'utf-8'))
    # sock.send(bytes('MODE {} +p\r\n'.format(config.irc_con_channel), 'utf-8'))
    # sock.send(bytes('MODE {} +s\r\n'.format(config.irc_con_channel), 'utf-8'))
    # sock.send(bytes('MODE {} +t\r\n'.format(config.irc_con_channel), 'utf-8'))
    sock.send(bytes('MODE {} +k {}\r\n'.format(config.irc_con_channel, config.irc_con_channel_password), 'utf-8'))
    sock.send(bytes('JOIN {}\r\n'.format(config.irc_chat_channel), 'utf-8'))
    sock.send(bytes('TOPIC {} :{}\r\n'.format(config.irc_chat_channel, config.irc_chat_channel_topic), 'utf-8'))

    # Start the subprocess

    proc = Popen([config.command] + config.command_args, stdin=sys.stdin, stdout=PIPE, stderr=PIPE)

    # Start read/write threads

    thread_in = Thread(target=console_in, args=[sock])
    thread_in.daemon = True
    thread_in.start()
    thread_out = Thread(target=console_out, args=[proc.stderr, sock])
    thread_out.daemon = True
    thread_out.start()

    proc.wait()

    thread_in.join(timeout=1)
    thread_out.join(timeout=1)
    return 0


if __name__ == '__main__':
    main()
