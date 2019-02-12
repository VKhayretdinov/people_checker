import json
import time
import os
import random
import requests
import cv2


PHOTO_PATH = "images/ph0"


def take_photo():
    """
    Take photo and save this in 'image' folder

    """

    cap = cv2.VideoCapture(0)  # Open the default camera

    if not cap.isOpened():
        cap.open()

    ret, img = cap.read()

    if ret and img is not None:
        cv2.imwrite(PHOTO_PATH + ".jpg", img)


def send_photo(vk, target_id):
    """
        Send a photo to target

        :param vk: the VkApiMethod(self) for using methods of API VK
        :param target_id: user's id to send a photo
    """
    data = vk.photos.getMessagesUploadServer()
    upload_url = data["upload_url"]
    files = {'photo': open(PHOTO_PATH + ".jpg", 'rb')}

    response = requests.post(upload_url, files=files)
    result = json.loads(response.text)

    upload_result = vk.photos.saveMessagesPhoto(server=result["server"],
                                                photo=result["photo"],
                                                hash=result["hash"])

    vk.messages.send(user_id=target_id,
                     attachment="photo" + str(vk.users.get()[0]["id"]) + "_" + str(upload_result[0]["id"]),
                     random_id=int(random.randint(1, 999999999)))

    os.remove(PHOTO_PATH + ".jpg")

    print("Фото отправлено")


def start_send_photos(vk, target_id, frequency_min):
    """
    send photo in the infinite loop

    :param vk: the VkApiMethod(self) for using methods of API VK
    :param target_id: user's id to send a photo
    :param frequency_min: frequency of sending photos (indicated in minutes)
    """
    while True:
        take_photo()
        send_photo(vk, target_id)
        time.sleep(60*int(frequency_min))

