from faker import Faker
from requests import put, post, get
import json
fake = Faker()


def register_test(count):
    successful_account = []
    for i in range(count):
        account = fake.email()
        password = fake.street_name()
        name = fake.name()
        data = {'account': account, 'password': password, 'name': name}
        print(data)
        res = json.loads(
            post("http://localhost:80/user/register", data).content
        )
        print(res)
        if res.get('msg') == "register successful":
            successful_account.append(data)
    return successful_account


def login_test(login_account_list):
    successful_count = 0
    login_user_list = []
    for user in login_account_list:
        res = post("http://localhost:80/user/login", data={'account': user['account'], 'password': user['password']})
        if res.status_code == 200:
            successful_count += 1
            login_user = {'Account': user['account'], 'user_id': json.loads(res.content).get('user_id')}
            login_user_list.append(login_user)
    return login_user_list


def get_user_info_test(login_user_list):
    successful_count = 0
    user_info_list = []
    for user in login_user_list:
        res = get('http://localhost:80/user/getUserInfo/{}'.format(user['user_id']))
        if res.status_code == 200:
            user_info_list.append(res.content)
            successful_count += 1
            print('{} get info successful'.format(user['user_id']))
    return successful_count, user_info_list


def logout_test(login_user_list):
    succesful_logout = 0
    for login_user in login_user_list:
        res = post('http://localhost:80/user/logout', data={'user_id':login_user['user_id']})
        if res.status_code == 200:
            succesful_logout += 1
    return succesful_logout


if __name__ == "__main__":
    successful_data = register_test(10)
    print(successful_data)
    successful_login_list = login_test(successful_data)
    print("successful_login:", len(successful_login_list))
    info_count, info_list = get_user_info_test(successful_login_list)
    print(info_count)
    print(info_list)
    successful_logout = logout_test(successful_login_list)
    print('successful_logout: ', successful_logout)

