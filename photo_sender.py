import getpass
import json
import time
import os
import random
import requests
import vk_api
import cv2


def main():
    vk = authorization()
    sending_frequency = int(input("Как часто присылать фото(в минутах)? -> "))
    start_send_photos(vk, sending_frequency)


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


def take_photo(img_name):
    """
    Take photo and save this in 'image' folder

    :param img_name: the image name for saving picture
    :return: result of saving photo (True or False)
    """
    cap = cv2.VideoCapture(0)  # Open the default camera

    if not cap.isOpened():
        cap.open()

    ret, img = cap.read()

    if ret and img is not None:
        cv2.imwrite("images/" + str(img_name) + ".jpg", img)
        return True
    else:
        return False


def send_photo(vk, photo_path):
    """
    Send photo to VK user

    :param vk: the VkApiMethod(self) for using methods of API VK
    :param photo_path: path to the photo for sending
    """
    photo_name = 0
    target_id = int(input("id пользователя-> "))

    if take_photo(photo_name):
        data = vk.photos.getMessagesUploadServer()

        upload_url = data["upload_url"]
        files = {'photo': open(photo_path + str(photo_name) + ".jpg", 'rb')}

        response = requests.post(upload_url, files=files)
        result = json.loads(response.text)

        upload_result = vk.photos.saveMessagesPhoto(server=result["server"],
                                                    photo=result["photo"],
                                                    hash=result["hash"])

        vk.messages.send(user_id=target_id,
                         attachment="photo" + str(vk.users.get()[0]["id"]) + "_" + str(upload_result[0]["id"]),
                         random_id=int(random.randint(1, 999999999)))

        os.remove(photo_path + str(photo_name) + ".jpg")
    else:
        vk.messages.send(user_id=target_id,
                         message="Problems getting photos from the camera. Check the device please.",
                         random_id=int(random.randint(11111111, 999999999)))


def start_send_photos(vk, frequency_min):
    """
    send photo in the infinite loop

    :param vk: the VkApiMethod(self) for using methods of API VK
    :param frequency_min: frequency of sending photos (indicated in minutes)
    """
    while True:
        send_photo(vk, "images/")
        print("Фото отправлено")
        time.sleep(60*int(frequency_min))


if __name__ == "__main__":
    main()
