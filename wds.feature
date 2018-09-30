Feature: Тестирование WDS

Scenario Outline: Проверка стабильности поднятия WDS при смене каналов

When Подключиться по telnet к устройству с IP "192.168.1.2" с prompt "root@WB([0-9]+)"
When Сменить частотный канал на "<channel>"
When Подключиться по telnet к устройству с IP "192.168.1.1" с prompt "root@WB([0-9]+)"
When Сменить частотный канал на "<channel>"
When Подождать "30" секунд
When Проверить пингом доступность хоста "192.168.1.20"

Examples: Channels
| channel |
| 100     |