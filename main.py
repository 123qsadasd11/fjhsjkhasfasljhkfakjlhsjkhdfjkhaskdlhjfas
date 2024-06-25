TOKEN = 'vk1.a.pChjpXd_lXWJWiWbgXcaTvX2RgpbPY_KFMeyD9Rz7LdEcUJwRKi1kIO2DvenRtXNH0sG93F3kx5fylCUQoVqigENEw5g1bcOS8sK25uawlG5wmCX4XdSH-HwqQn16pFrjm8LVcBsHosFtf-U2Nh7OTJo0JiwO9jW8MdK1aiHku2rXDwmfOCWlaP8u7yMF_tXcenrM5wjyGZNSp3TpsYVxw'
GROUP_ID = 226337453


import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor, VkKeyboardButton

from config import Config


vk = vk_api.VkApi(token=TOKEN)
long_poll = VkBotLongPoll(vk=vk, group_id=GROUP_ID)
api = vk.get_api()


config = Config(file='users.json', mode='json')
users = Config(file='users_in_bot.json', mode='json')


def search(nick: str):
    if config.isset(nick):
        return config.get(nick)
    else:
        return 'not'


def get_info(user_id):
    return users.get(str(user_id))


def keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button(label='Профиль', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='Информация', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='Команды', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


for event in long_poll.listen():

    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object['message']['text'].lower()
        args = text.split()
        command = args[0]
        del args[0]

        peer_id = event.object['message']['peer_id']

        if not users.isset(str(peer_id)):
            users.set(str(peer_id), {
                'subscribe': False,
                'role': 'user'
            })
            users.save()
            api.messages.send(peer_id=peer_id,
                              keyboard=keyboard(),
                              random_id=0,
                              message='Добро пожаловать!')

        match command:
            case '/search':
                if not get_info(str(peer_id))['subscribe']:
                    api.messages.send(peer_id=peer_id,
                                      message='[!] У вас нет подписки!',
                                      random_id=0)
                    continue
                if len(args) >= 1:
                    nick = args[0]
                    search1 = search(str(nick))
                    if search1 == 'not':
                        api.messages.send(peer_id=peer_id,
                                          message='[!] Данный аккаунт не найден!',
                                          random_id=0)
                    else:
                        text = f'Информация об аккаунте {str(nick)}:\n'
                        for k, v in search1.items():
                            text += f'{k}: {", ".join(v)}\n'
                        api.messages.send(peer_id=peer_id,
                                          message=text,
                                          random_id=0)
                else:
                    api.messages.send(peer_id=peer_id,
                                      message='[!] Укажите ник',
                                      random_id=0)
            case '/give':
                if get_info(peer_id)['role'] == 'admin':
                    all_ = users.getAll()
                    all_[str(args[0])]['subscribe'] = True
                    users.setAll(all_)
                    users.save()
                    api.messages.send(peer_id=peer_id,
                                      message=f'[+] Вы успешно выдали подписку @id{str(args[0])}',
                                      random_id=0)
                    api.messages.send(peer_id=args[0],
                                      message='[+] Вам выдана подписка!',
                                      random_id=0)
                else:
                    api.messages.send(peer_id=peer_id,
                                      message=f'[!] Да пошел ты нахуй',
                                      random_id=0)
        match text:
            case 'профиль':
                text = f"""[+] Ваш id: {str(peer_id)}\n
[+] Подписка: {"активна" if get_info(str(peer_id)) == True else "нет"}\n
[+] Роль: {get_info(str(peer_id))["role"]}"""
                api.messages.send(peer_id=peer_id,
                                  message=text,
                                  random_id=0)
            case 'информация':
                text = f"""[!] StealPass - бот, который позволяет узнать пароль от аккаунта!\n
[+] На данный момент в базе - {str(len(config.getAll()))} аккаунтов!
[+] Актуальная цена подписки - 100rub/lifetime(навсегда)
[+] За покупкой - @desolatr1x"""
                api.messages.send(peer_id=peer_id,
                                  message=text,
                                  random_id=0)
            case 'команды':
                text = """[?] Помощь по командам:\n
[-] /search | /поиск <ник> - поиск аккаунта и данные к нему в базе данных."""
                api.messages.send(peer_id=peer_id,
                                  message=text,
                                  random_id=0)
