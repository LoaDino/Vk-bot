#импортируем вк-апи прослушку сообщений, цвета кнопок, отправку сообщений и клавиатуру из вк-апи, а также рандом для красоты
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from random import choice


token='2186ae0b66dcd6cf13f556008329e92e30f0fbe2d2cba42b02c5ecd5c2d179b4c82958b8609aab76d3473' # вставить токен апи сюда

session=vk_api.VkApi(token=token)

def write_message(user_id,message,keyboard=None):  # функция для отправки сообщения
    param={
        'user_id':user_id,
        'message':message,
        'random_id':0
    }

    if keyboard!=None:
        param['keyboard']=keyboard.get_keyboard()
    else:
        param=param
    
    session.method('messages.send',param) #метод отправки сообщения

longpoll = VkLongPoll(session)
keyboard1 = VkKeyboard() #создадим клавиатуру для игры

keyboard1.add_button('Камень✊',color=VkKeyboardColor.POSITIVE)
keyboard1.add_button('Ножницы✌️',color=VkKeyboardColor.POSITIVE)
keyboard1.add_button('Бумага✋',color=VkKeyboardColor.POSITIVE)
keyboard1.add_line()
keyboard1.add_button('Ящерица🤏',color=VkKeyboardColor.PRIMARY)
keyboard1.add_button('Спок🖖',color=VkKeyboardColor.PRIMARY)
keyboard1.add_line()
keyboard1.add_button('Вернуться в начало↩',color=VkKeyboardColor.NEGATIVE) # добавим нужные кнопки

keyboard2=VkKeyboard() # создадим клавиатуру для меню
keyboard2.add_button('Играть с ботом🤖',color=VkKeyboardColor.NEGATIVE)
keyboard2.add_button('Играть онлайн😎',color=VkKeyboardColor.POSITIVE)
keyboard2.add_line()
keyboard2.add_button('Покажи правила📃',color=VkKeyboardColor.SECONDARY)
keyboard2.add_button('Покажи мои медали🎖',color=VkKeyboardColor.SECONDARY)

clients = {} #тут будут хранится данные об игроках (ниже по коду)
medals = {} #отдельно хранятся медальки, так как это единственное, что не сбрасывается


#сделаем иерархию для игры ( то есть дадим понять, что кого бьет )
ierarh = { 'Камень✊':['Ножницы✌️',"Ящерица🤏"], 'Ножницы✌️':['Бумага✋',"Ящерица🤏"], 'Бумага✋':['Камень✊','Спок🖖'], "Ящерица🤏":['Бумага✋','Спок🖖'], 'Спок🖖':['Ножницы✌️','Камень✊'] } 
bots_choice = ['Камень✊','Ножницы✌️','Бумага✋',"Ящерица🤏",'Спок🖖'] # для бота, чтобы он выбирал из этого, а также для филтрации сообщений

bots = ['Бот-Антон','Бот-Андрей','Бот-Виталя','Бот-Артем','Игорь','Бот-Эдуард'] #ники ботов


#различные сообщения после победы, поражения, ничьи
win_quote = ['✨Победа, победа вместо обеда!✨','Да ты чародей-читатель мыслей!🧙‍♂️','Ты случайно не ведешь курсы по игре RPS? Я бы записалась на них😺']
lose_quote = ['К сожалению, повелительница фортуны повернулась не в твою сторону😔',"Не растраивайся, пирожок!🤗",'Ему(ей) просто повезло!☝️']
draw_quote = ['Вы сговорились?🤨','Вот это я понимаю схожесть мыслей👤👤','Вы как будто близнецы из фильма "Мачо и ботан 2"😲']

#цикл прослушки сообщений сообщества
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me: #если к нам пришло сообщения
        message=event.text # полчуим текст сообщения 
        if str(event.user_id) not in clients:
            clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore'] #так выглядит паспорт игрока 
#(первое- это где он сейчас, второе - это выбор игрока в игре, третье- это айди соперника, 4-ое - это его счет, 5-ое - это счет Бота(если он играет против бота))


        if str(event.user_id) not in medals:
            medals[str(event.user_id)] = [0,0] #медальки с ботом и онлайн игры
        #выше были проверки на то, впервые ли нам пишут, чтобы добавить его(её) в клиенты и дать возможность получать медали


        #ответы на сообщения с определенным текстом
        if message=='Начать':
            user = session.method( "users.get", {"user_ids": event.user_id} )[0]['first_name'] #при помощи метода получим данные пользователя ро айди и возьмем из данный его имя
            write_message(event.user_id, 'Привет, '+user+', я - бот RPS(Rock Paper Scirrors)\nВыбери тип игры👇🏻', keyboard2)
        
        elif message== 'Вернуться в начало↩':
            write_message(event.user_id,'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
            clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore'] 
        elif message == 'Покажи правила📃':
            write_message(event.user_id,'Кто кого побеждает:\n✊ -> ✌️ 🤏\n✌️ -> ✋ 🤏\n ✋ -> ✊ 🖖\n 🤏 -> ✋ 🖖\n 🖖 -> ✊ ✌️')
        
        elif message == 'Покажи мои медали🎖':
            write_message(event.user_id,f'Медалек-побед против бота🏅: {medals[str(event.user_id)][0]}\nМедалек-побед в онлайне🥇: {medals[str(event.user_id)][1]}')



        elif message=='Играть онлайн😎':
            write_message(event.user_id,'Подбор противника...🔄')
            for i in clients: #проверка всех клиентов
                if clients.get(i)[0] == 'waiting...' and i != str( event.user_id ): #если кто-то ожидает игру и это не ты сам
                    user1 = session.method( "users.get", {"user_ids": event.user_id} )[0]['first_name']
                    user2 = session.method( "users.get", {"user_ids": int(i)} )[0]['first_name']
                    write_message( event.user_id,f'Готово!✅ Твой соперник: {user2} с {medals[i][1]} медалями! \n🏆Играем до 10 побед!🏆\nВыбери действие👇🏻',keyboard1 )
                    write_message( int(i),f'Готово!✅ Твой соперник: {user1} с {medals[str(event.user_id)][1]} медалями! \n🏆Играем до 10 побед!🏆\nВыбери действие👇🏻',keyboard1 )
                    clients[str(event.user_id)][2] = i #дадим айди соперника
                    clients[i][2]=str(event.user_id) # дадим айди свой сопернику
                    clients[str(event.user_id)][3] = 0 #начнем счет
                    clients[i][3] = 0
                    clients[str(event.user_id)][1] = 'Choosing...' #из режима NoGame перейдем в режим выбора
                    clients[i][1] = 'Choosing...'
                    clients[str(event.user_id)][0] = 'gameonline' # запускаем игру им
                    clients[i][0] = 'gameonline'

            if clients[str(event.user_id)][0] != 'gameonline': #если соперник не найден, то в ожидание
                clients[str(event.user_id)][0] = 'waiting...' #дадим понять, что ты ожидаешь игру



        
        elif message=='Играть с ботом🤖':
            write_message(event.user_id, f'Готово!✅ Твой соперник: {choice(bots)}\n🏆Играем до 10 побед!🏆\nВыбери действие👇🏻',keyboard1)
            clients[str(event.user_id)][0] = 'gamebot'
            clients[str(event.user_id)][3] = 0
            clients[str(event.user_id)][4] = 0



        
        elif message in bots_choice: #если пришло игровое сообщение
            if clients[str(event.user_id)][0] == 'gameonline':  #если челик в онлайн игре

                id_opponent = clients[str(event.user_id)][2] #получим айди противника 

                if clients[id_opponent][1] == 'Choosing...': #если оппонент выбирает
                    clients[str(event.user_id)][1] = message #дадим понять,что мы выбрали

                    write_message(event.user_id,'Ждём соперника...🔁')
                    write_message(int(id_opponent),'❗️Твой соперник уже выбрал, что поставить, выбирай скорее!❗️')
                
                elif clients[id_opponent][1] == 'NoGame': #если соперник вышел
                    write_message(event.user_id,'Твой соперник ушел...')
                    
                    write_message(event.user_id,'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore']
                    
                
                elif clients[id_opponent][1] in ierarh[message]: #если его выбор находитсяв списке тех, кого побеждает мой выбор
                    clients[str(event.user_id)][3] += 1 #+1 Score
                    score = [clients[str(event.user_id)][3],clients[id_opponent][3]] #получаем счета

                    write_message(event.user_id,f'Противник выбрал {clients[id_opponent][1]} \n{choice(win_quote)}\nСчет: ⭐️ (ты){score[0]}:{score[1]} ⭐️')
                    write_message(int(id_opponent),f'Противник выбрал {message} \n{choice(lose_quote)}\nСчет: ⭐️ (ты){score[1]}:{score[0]} ⭐️')
                    clients[id_opponent][1] = 'Choosing...' #сбросить выбор
                    clients[str(event.user_id)][1] = 'Choosing...'

                elif clients[id_opponent][1] == message: #если один и тот же выбор
                    score = [clients[str(event.user_id)][3],clients[id_opponent][3]]

                    write_message(event.user_id,f'Противник тоже выбрал {clients[id_opponent][1]} \n{choice(draw_quote)}\nСчет: ⭐️ (ты){score[0]}:{score[1]} ⭐️')
                    write_message(int(id_opponent),f'Противник тоже выбрал {message} \n{choice(draw_quote)}\nСчет: ⭐️ (ты){score[1]}:{score[0]} ⭐️')
                    clients[id_opponent][1] = 'Choosing...'
                    clients[str(event.user_id)][1] = 'Choosing...'

                else: 
                    clients[id_opponent][3] += 1
                    score = [clients[str(event.user_id)][3],clients[id_opponent][3]]

                    write_message(event.user_id,f'Противник выбрал {clients[id_opponent][1]} \n{choice(lose_quote)}\nСчет: ⭐️ (ты){score[0]}:{score[1]} ⭐️')
                    write_message(int(id_opponent),f'Противник выбрал {message} \n{choice(win_quote)}\nСчет: ⭐️ (ты){score[1]}:{score[0]} ⭐️')
                    clients[id_opponent][1] = 'Choosing...'
                    clients[str(event.user_id)][1] = 'Choosing...'

                
                if clients[str(event.user_id)][3] == 10: #если мы набрали 10 очков
                    write_message(event.user_id, f'🏆Поздравляю!🏆\nТы победил по счёту, получи медальку!🥇')
                    medals[str(event.user_id)][1] += 1

                    write_message(int(id_opponent), f'Противник набрал 10 очков, ты проиграл...😢')

                    write_message(int(id_opponent),'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    write_message(event.user_id,'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore']
                    clients[id_opponent]=['menu', 'NoGame', 'id', 'Score','BotScore']


                elif clients[id_opponent][3] == 10: #если противник набрал 10 очков
                    write_message(int(id_opponent), f'🏆Поздравляю!🏆\nТы победил по счёту, получи медальку!🥇')
                    medals[id_opponent][1] += 1

                    write_message(event.user_id, f'Противник набрал 10 очков, ты проиграл...😢')

                    write_message(event.user_id,'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    write_message(int(id_opponent),'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore']
                    clients[id_opponent]=['menu', 'NoGame', 'id', 'Score','BotScore']




            elif clients[str(event.user_id)][0] == 'gamebot': #если мы играем с ботом
                bot_choose = choice(bots_choice)

                if bot_choose in ierarh[message]:
                    clients[str(event.user_id)][3] += 1
                    score = [clients[str(event.user_id)][3],clients[str(event.user_id)][4]]
                    write_message(event.user_id, f'Бот выбрал {bot_choose} \n{choice(win_quote)}\nСчет: ⭐️ (ты){score[0]}:{score[1]} ⭐️')
                
                elif bot_choose == message:
                    score = [clients[str(event.user_id)][3],clients[str(event.user_id)][4]]
                    write_message(event.user_id, f'Бот тоже выбрал {bot_choose} \n{choice(draw_quote)}\nСчет: ⭐️ (ты){score[0]}:{score[1]} ⭐️')
                else:
                    clients[str(event.user_id)][4] += 1
                    score = [clients[str(event.user_id)][3],clients[str(event.user_id)][4]]
                    write_message(event.user_id, f'Бот выбрал {bot_choose} \n{choice(lose_quote)}\nСчет: ⭐️ (ты){score[0]}:{score[1]} ⭐️') 

                if clients[str(event.user_id)][3] == 10:
                    write_message(event.user_id, f'🏆Поздравляю!🏆\nТы победил по счёту, получи медальку!🏅')
                    medals[str(event.user_id)][0] += 1

                    write_message(event.user_id,'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore']


                elif clients[str(event.user_id)][4] == 10:
                    write_message(event.user_id, f'Противник набрал 10 очков, ты проиграл...😢')

                    write_message(event.user_id,'Ты в главном меню :)\n\n\nВыбери тип игры👇🏻',keyboard2)
                    clients[str(event.user_id)]=['menu', 'NoGame', 'id', 'Score','BotScore']
