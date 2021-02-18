import sys
import requests

base_url = "https://api.trello.com/1/{}"
auth_params = {
    'key': "82d0a920ee5747c53c845a352ae4d964",
    'token': "b9dd880f608b855a5240dac8357e80f6d70b9e717c237d00d16590b71b6dbeda", }
board_id = "60255c5510396663defb3dbc"
response = requests.get(base_url.format('boards/' + board_id), params=auth_params).json()


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    # Получим данные всех задач в колонке и перечислим все назван
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        print(column["name"] + " - {}".format(len(task_data)))

        if not task_data:
            print('\t' + 'Нет задач!')
            continue

        for task in task_data:
            print('\t' + task['name'] + "\t" + task["id"])

def create(name, column_name):
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)["id"]
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})


def move(name, column_name):
    dublicate_tasks = get_task_dublicates(name)
    if len(dublicate_tasks) > 1:
        print("Задач с таким названием несколько штук:")
        for index,task in enumerate(dublicate_tasks):
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()[
                'name']
            print("Задача №{}\tid: {}\tНаходится в колонке: {}\t ".format(index, task['id'], task_column_name))
        task_id = input("Пожалуйста, введите ID задачи, которую нужно переместить: ")
    else:
        task_id = dublicate_tasks[0]['id']
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})

def column_check(column_name):
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for  column in column_data:
        if column["name"] == column_name:
            return column["id"]
    return

def create_column(column_name):
    return requests.post(base_url.format('lists'),
                         data={'name': column_name, 'idBoard': board_id, **auth_params}).json()

def get_task_dublicates(task_name):
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Заведём список колонок с дублирующимися именами
    duplicate_tasks = []
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == task_name:
                duplicate_tasks.append(task)
    return duplicate_tasks



if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])