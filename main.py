import getpass
import video
import vk_api


def main():
    # vk = authorization()
    # sending_frequency = int(input("Как часто присылать фото(в минутах)? -> "))
    # start_send_photos(vk, sending_frequency)

    video.show_video()


def authorization():
    """
    Authorizes user

    :return: VkApiMethod(self) for using methods of API VK
    """
    login = "+7" + input("Логин-> +7")
    password = getpass.getpass("Пароль-> ")  # Set "Emulate terminal in output console" for PyCharm

    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.exceptions.BadPassword:
        print("Неверный логин/пароль")
        authorization()

    return vk_session.get_api()


if __name__ == "__main__":
    main()
