import os
import csv
import socket
import ipaddress
from datetime import datetime

# Функция для чтения сети из файла
def read_network_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            network = file.readline().strip()
            return ipaddress.ip_network(network, strict=False)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return None

# Функция для проверки доступности IP-адреса
def is_ip_online(ip):
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    return response == 0

# Функция для получения имени хоста (если доступно)
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except socket.herror:
        return "Неизвестно"

# Функция для получения MAC-адреса с использованием утилиты nmap
def get_mac_address(ip):
    try:
        result = os.popen(f"nmap -sP {ip} | grep 'MAC Address'").read().strip()
        if result:
            return result.split(' ')[-1]
        return "MAC не найден"
    except:
        return "Ошибка при получении MAC"

# Сохранение результатов в CSV-файл
def save_to_csv(file_path, data, headers):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Основной код
network = read_network_from_file('network_config.txt')

if network is None:
    print("Не удалось прочитать IP-сеть из файла.")
    exit(1)

online_ips = []
offline_ips = []

# Получение общего количества IP-адресов
total_ips = network.num_addresses

# Обработка каждого IP-адреса в сети
for index, ip in enumerate(network.hosts(), start=1):
    print(f"Проверка IP {index}/{total_ips}: {ip}...")
    is_online = is_ip_online(ip)
    hostname = get_hostname(ip)
    mac_address = get_mac_address(ip)

    if is_online:
        online_ips.append([str(ip), hostname, mac_address, "Онлайн"])
    else:
        offline_ips.append([str(ip), hostname, mac_address, "Оффлайн"])

    # Обновление прогресса
    print(f"Прогресс: {index}/{total_ips} завершено")

# Сохранение онлайн и оффлайн IP-адресов в отдельные CSV-файлы
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
save_to_csv(f'online_ips_{current_time}.csv', online_ips, ["IP", "Hostname", "MAC-адрес", "Статус"])
save_to_csv(f'offline_ips_{current_time}.csv', offline_ips, ["IP", "Hostname", "MAC-адрес", "Статус"])

print(f"Результаты сохранены в файлы: online_ips_{current_time}.csv и offline_ips_{current_time}.csv")
