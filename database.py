import json
import firebase

from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from firebase import jsonutil

firebase = firebase.FirebaseApplication('https://team-foobar-maze-generator.firebaseio.com/', None)
key = 'abcdefghijklmnopqrstuvwxyz'

def encrypt(n, plaintext):

    result = ''

    for l in plaintext.lower():
        try:
            i = (key.index(l) + n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result.lower()

def decrypt(n, ciphertext):

    result = ''

    for l in ciphertext:
        try:
            i = (key.index(l) - n) % 26
            result += key[i]
        except ValueError:
            result += l

    return result

#firebase.put('/leaderboard/top10_moves', username, 58)

###############################
def start():
    success = False

    print "Welcome!"

    while success == False:

        test = raw_input("1 to login\n2 to signup\n")

        if test == "1":
            account_fetched = False

            while account_fetched == False:

                username = raw_input("Input username: ")
                result = firebase.get('/users', username)

                if result != None:
                    decrypted_password = decrypt(5, result['password'])
                    password_matched = False

                    while password_matched == False:
                        password = raw_input("Input password: ")

                        if password == decrypted_password:
                            print "password matches"

                            leaderboard_moves = firebase.get('/leaderboard/top10_moves', None)
                            print leaderboard_moves

                            leaderboard_times = firebase.get('/leaderboard/top10_times', None)
                            print leaderboard_times

                            password_matched = True
                            account_fetched = True
                            success = True
                        else:
                            print "Password incorrect, try again."
                else:
                    print "Incorrect username, try again."

        elif test == "2":
            account_created = False

            while account_created == False:

                username = raw_input("Input a unique username: ")

                if (firebase.get('/users', username)) == None:
                    # username does not exist
                    print "Username does not exist"
                    email = raw_input("Input email: ")
                    password = raw_input("Input password: ")
                    encrypted_password = encrypt(5, password)

                    if firebase.put('/users/', username, {'email': email, 'password': encrypted_password}):
                        account_created = True

                else:
                    print "Username exists, try again\n"

            success = True
        else:
            print "error"

start()
