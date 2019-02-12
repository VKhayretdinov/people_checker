import getpass
import video
import vk_api
import photo
import sys


def main(module):
    vk = authorization()
    target_id = int(input("ID пользователя, которому отправлять фото-> "))
    if module == 1:
        sending_frequency = int(input("Как часто присылать фото(в минутах)? -> "))
        photo.start_send_photos(vk, target_id, sending_frequency)
    else:
        video.face_detection_dnn(vk, target_id)


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


def choose_module():
    ans = int(input("""
    Какой модуль запустить? 
    1 -- отправка фото через определеннный промежуток времени
    2 -- отправка фото при обнаружении хотя бы одного человека в кадре
    -> """))

    true_list = [1, 2]

    if ans not in true_list:
        sys.exit("Ошибка при вводе типа модуля")
    else:
        return ans


if __name__ == "__main__":
    print("------------------------------------------------------------------------------------------------------"
          "-----------------")
    print("ВК может заблокировать аккаунт из-за подозрительной активности, лучше используйте ненужный профиль для "
          "работы программы")
    print("------------------------------------------------------------------------------------------------------"
          "-----------------")
    module_type = choose_module()
    main(module_type)

