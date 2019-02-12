from faker import Faker
from requests import put
import json
fake = Faker()


def register_test(count):
    successful_account = []
    for i in range(count):
        account = fake.email()
        password = fake.street_name()
        name = fake.name()
        data = {'account': account, 'password': password, 'name': name}
        res = json.loads(
            put("http://localhost:5000/register", data).content
        )
        if res.get('msg') == "register successful":
            successful_account.append(data)
    return successful_account


def login_test(login_account_list):
    successful_count = 0
    for user in login_account_list:
        res = put("http://localhost:5000/login", data={'account': user['account'], 'password': user['password']})
        if res.status_code == 200:
            successful_count += 1
            print("Account:"+user['account']+"login_successful")
    return successful_count


if __name__ == "__main__":
    successful_data = register_test(10)
    print(successful_data)
    successful_login = login_test(successful_data)
    print("successful_login:", successful_login)

