# IRC settings
irc_address = 'localhost'                       # address of the irc server
irc_port = 6667                                 # port of the irc server
irc_nick = 'SRB2ChatBridge'                     # nick of the irc client
irc_username = 'srb2chatbridge'                 # username of the irc client
irc_con_channel = '#console'                    # name of the channel where the console output will be sent
irc_chat_channel = '#chat'                      # name of the channel where the chat output will be sent
irc_con_channel_password = 'changeme'           # password for accessing the console channel
irc_con_channel_topic = 'This is a server console.'
irc_chat_channel_topic = 'This is a live chat from the server.'
irc_chat_allowed = ['has completed the level.', 'Speeding off to level...', 'Map is now ']  # a list of filters that allow a message to be sent in the chat channel
# Runtime settings
screen_name = 'srb2'                            # name of the linux screen (make sure to run 'start.py' in the screen with the same name)
command = 'lsdl2srb2'                           # exec command
command_args = ['-dedicated', '-room', '33']    # exec arguments
