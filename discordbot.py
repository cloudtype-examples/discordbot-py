#버전 1.0.0

from datetime import datetime
from time import time
import discord
import pytz

KST = pytz.timezone('Asia/Seoul')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

server_list = []
text_channel_list = []
master_text_channel = []

#test_server_list = []
#test_text_channel_list = []

@client.event
async def on_ready():
    print('{0.user} 봇 가동시작'.format(client)) #봇이 실행되면 콘솔창에 표시
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == "로그":
                server_list.append(channel.guild.id)
                text_channel_list.append(channel.id)
                #test_server_list.append(channel.guild.name)  #test
                #test_text_channel_list.append(channel.name)  #test
            if channel.name == "마스터-로그":
                master_text_channel.append(channel.id)

"""
    for i in server_list:
        print(i)
    for i in text_channel_list:
        print(i)
    for i in test_server_list:
        print(i)
    for i in test_text_channel_list:
        print(i)
"""



#봇이 새로운 채널에 추가되었을 때 리스트에 추가
@client.event
async def on_guild_join(guilds):
    for channel in guilds.text_channels:
        if channel.name == "로그":
            server_list.append(channel.guild.id)
            text_channel_list.append(channel.id)
            #test_server_list.append(channel.guild.name)  #test
            #test_text_channel_list.append(channel.name)  #test
"""
    for i in server_list:
        print(i)
    for i in text_channel_list:
        print(i)
    for i in test_server_list:
        print(i)
    for i in test_text_channel_list:
        print(i)
"""
#봇이 채널에서 추방되었을 때 리스트 정리
@client.event
async def on_guild_remove(guilds):
    ind = server_list.index(guilds.id)
    del text_channel_list[ind]
    del server_list[ind]
    #del test_server_list[ind]  #test
    #del test_text_channel_list[ind]  #test
"""
    for i in server_list:
        print(i)
    for i in text_channel_list:
        print(i)
    for i in test_server_list:
        print(i)
    for i in test_text_channel_list:
        print(i)
"""

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="학생")
    await member.add_roles(role)


@client.event
async def on_message(message):
    if message.author == client.user: # 봇 자신이 보내는 메세지는 무시
        return

    if message.content.startswith('?안녕'): # 만약 $hello로 시작하는 채팅이 올라오면
        await message.channel.send("안녕") # Hello!라고 보내기
    
    if message.content.startswith('?서버리스트확인'): # 만약 $hello로 시작하는 채팅이 올라오면
        if message.channel.id == master_text_channel[0]:
            await message.channel.send("등록된 서버의 개수 : {}".format(len(server_list)))
            await message.channel.send("등록된 텍스트채널의 개수 : {}".format(len(text_channel_list)))
            for i in range(len(server_list)):
                await message.channel.send("서버{} : {}".format(i+1, client.get_guild(server_list[i])))
    
    if message.content.startswith('?서버리스트초기화'): # 만약 $hello로 시작하는 채팅이 올라오면
        if message.channel.id == master_text_channel[0]:
            server_list.clear()
            text_channel_list.clear()
            for guild in client.guilds:
                for channel in guild.text_channels:
                    if channel.name == "로그":
                        server_list.append(channel.guild.id)
                        text_channel_list.append(channel.id)
            await message.channel.send("리스트 초기화완료")

    if message.content.startswith('?종주만세'):
        master_text_channel[0] = message.channel.id
        await message.channel.send("이제부터 이곳에 마스터로그를 출력합니다")

    if message.content.startswith('?help'): # 만약 $hello로 시작하는 채팅이 올라오면
        await message.channel.send("?안녕 = 봇 상태 확인용 인사")
        await message.channel.send("?서버리스트확인 = 현재 봇이 관리하고 있는 서버리스트 확인")
        await message.channel.send("?서버리스트초기화 = 서버리스트 리셋")
        await message.channel.send("?종주만세 = 명령용 마스터로그채널로 설정")

@client.event
async def on_voice_state_update(member, before, after):
    print(before)
    print(after)
    print("------정보 끝------")
    if before.channel == None and after.channel != None:
        now = datetime.now(KST)

        ch = client.get_channel(text_channel_list[server_list.index(member.guild.id)])
        master_ch = client.get_channel(master_text_channel[0])


        await ch.send("log.{} {}[{}] {} 입장".format(now.strftime('%Y/%m/%d %H:%M:%S'),member.display_name, member, after.channel, ))
        await master_ch.send("log.{} ({}) {}[{}] {} 입장".format(now.strftime('%Y/%m/%d %H:%M:%S'), member.guild, member.display_name, member, after.channel, ))

    if after.channel == None and before.channel != None:
        now = datetime.now(KST)

        ch = client.get_channel(text_channel_list[server_list.index(member.guild.id)])
        master_ch = client.get_channel(master_text_channel[0])


        await ch.send("log.{} {}[{}] {} 퇴장".format(now.strftime('%Y/%m/%d %H:%M:%S'),member.display_name, member, before.channel, ))
        await master_ch.send("log.{} ({}) {}[{}] {} 퇴장".format(now.strftime('%Y/%m/%d %H:%M:%S'), member.guild, member.display_name, member, before.channel, ))



client.run('OTY4NzQxMTMzMzk4MTc5ODUw.YmjQfA.yecgc4G5LBOQcSujrJb5B4sw3_w') #토큰

#OTY4NzQxMTMzMzk4MTc5ODUw.YmjQfA.yecgc4G5LBOQcSujrJb5B4sw3_w

