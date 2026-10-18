import argparse
import json
import os
import re
from collections import defaultdict

pattern = re.compile(
    r'^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s+\S+\s+\S+\s+\[(?P<date>[^\]]+)\]\s+"(?P<method>GET|POST|PUT|DELETE|OPTIONS|HEAD)\s+(?P<url>(?:[^"\s\\]|\\.)+)\s+[^"]+"\s+(?P<status>\d{3})\s+(?P<bytes>\d+|-)\s+"(?P<referer>(?:[^"\\]|\\.)*)"\s+"(?P<user_agent>(?:[^"\\]|\\.)*)"\s+(?P<duration>\d+)$')


def get_ip_requests(item):
    ip, methods = item
    return sum(methods.values())


def get_request_duration(request):
    return request["duration"]


def parse_log_file(file):
    dict_ip = defaultdict(lambda: {"GET": 0, "POST": 0, "PUT": 0, "DELETE": 0, "OPTIONS": 0, "HEAD": 0})

    total_requests = 0
    requests = []

    with open(file, encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match is None:
                print(f"Строка не распознана: {line.strip()}")
                continue

            ip = match.group("ip")
            date = match.group("date")
            method = match.group("method")
            url = match.group("url")
            duration = int(match.group("duration"))

            dict_ip[ip][method] += 1
            total_requests += 1

            requests.append({"ip": ip, "date": f"[{date}]", "method": method, "url": url, "duration": duration})

    top_ips = dict(sorted(dict_ip.items(), key=get_ip_requests, reverse=True)[:3])

    top_longest = sorted(requests, key=get_request_duration, reverse=True)[:3]

    total_stat = {method: sum(ip_stat[method] for ip_stat in dict_ip.values()) for method in
                  ("GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD")
                  }

    return {
        "top_ips": top_ips,
        "top_longest": top_longest,
        "total_stat": total_stat,
        "total_requests": total_requests
    }


def print_statistic(file, statistic):
    print(f"\nФайл: {file}")
    print(f"Общее количество запросов: {statistic['total_requests']}")

    print("Количество запросов по HTTP-методам:")
    for method, count in statistic["total_stat"].items():
        print(f"{method} - {count}")

    print("Топ 3 IP адресов:")
    for ip, methods in statistic["top_ips"].items():
        print(f"{ip} - {sum(methods.values())}")

    print("Топ 3 самых долгих запросов:")
    for request in statistic["top_longest"]:
        print(
            f"{request['method']} {request['url']} "
            f"IP: {request['ip']} "
            f"длительность: {request['duration']} мс "
            f"дата: {request['date']}"
        )


def save_statistic(file, statistic):
    file_name = os.path.splitext(os.path.basename(file))[0]
    result_file = os.path.join(os.path.dirname(file), f"{file_name}_result.json")

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(statistic, f, ensure_ascii=False, indent=4)

    return result_file


def get_log_files(path):
    if os.path.isfile(path):
        return [path]

    if os.path.isdir(path):
        log_files = []

        for file_name in os.listdir(path):
            file_path = os.path.join(path, file_name)

            if os.path.isfile(file_path) and file_name.endswith(".log"):
                log_files.append(file_path)

        return sorted(log_files)

    raise FileNotFoundError(f"Путь не найден: {path}")


def log_parser(path):
    log_files = get_log_files(path)

    if not log_files:
        print("Лог-файлы не найдены.")
        return

    for log_file in log_files:
        statistic = parse_log_file(log_file)
        result_file = save_statistic(log_file, statistic)

        print_statistic(log_file, statistic)
        print(f"Статистика сохранена в файл: {result_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='path', action='store', required=True)
    args = parser.parse_args()

    log_parser(args.path)
