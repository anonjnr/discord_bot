#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
# bot_bcad_3.6.py

import utilities, os, fnmatch, re

async def membersDump(ctx):
    serverName = (f"*{ctx.message.guild.name.replace(' ', '-')}*")
    membersList = []
    for file in os.listdir('./logs'):
        if fnmatch.fnmatch(file, 'members-server*'):
            if fnmatch.fnmatch(file, serverName):
                filePath = './logs/' + file
                with open(filePath) as fp:
                    lines = fp.readlines()
                    for line in lines:
                        line = line.split("Number: " + line[re.search(r"\d", line).start()])[1].strip(" ").replace("_", "\_")
                        if line not in membersList:
                            membersList.append(line)
    membersList = '\n'.join(membersList)
    return membersList
    # with open('./logs/members.log', 'r', newline='\n', encoding='utf-8') as members_list_raw:
    #     members_list = members_list_raw.read()
    #     return members_list

async def membersLog(ctx):
    log_path = ("./logs/members" + "-server-" + ctx.message.guild.name.replace(' ', '-') + "-" + (utilities.epoch_to_custom_date(utilities.FMT_TIME_FILE)) + ".log")
    for i, member in enumerate(ctx.message.guild.members):
        list_mem_num = (f'{i}')
        list_mem_id = (f'{member.id}')
        list_mem = (f'{member}')
        list_mem_name = (f'{member.name}')
        list_all = (f'Number: {list_mem_num} ID: {list_mem_id} Name: {list_mem} ({list_mem_name})\n')
        with open(log_path, 'a') as file:
            file.write(list_all)
    return log_path