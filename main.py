import os
import ipaddress

# Задаём диапазон сети
network = ipaddress.ip_network("192.168.226.0/24", strict=False)

# Функция для проверки доступности IP-адреса
def is_ip_online(ip):
    print(f"Проверка {ip}...")  # Выводим проверяемый IP-адрес
    # Для Linux используем '-c 1' (1 пакет), '-W 1' (1 сек таймаут)
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    if response == 0:
        print(f"{ip} онлайн")
    else:
        print(f"{ip} оффлайн")
    return response == 0  # Если response == 0, IP онлайн

# Поиск свободных IP-адресов
free_ips = []

for ip in network:
    if not is_ip_online(ip):  # Если IP не онлайн, то добавляем его как свободный
        free_ips.append(ip)

# Вывод результатов
if free_ips:
    print("Свободные IP-адреса:")
    for free_ip in free_ips:
        print(free_ip)
else:
    print("Свободных IP-адресов не найдено.")
