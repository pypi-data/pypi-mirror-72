import requests
from bs4 import BeautifulSoup
from time import sleep

from trello.exceptions import MovedURL, HorriblyGoneWrongError


def get_soup(url):
    """Method to get the soup from the url"""
    counter = 5
    timeout_counter = 5
    headers = {
        'User-Agent': 'TrelloUpdater',
        'From': 'anubhav.yadav@gmx.com',
    }
    while True:
        try:
            r = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.ConnectionError:
            print("There is no network connectivity on this computer, will try again after {} seconds".format(counter))
            counter *= counter
            continue
        except requests.exceptions.Timeout:
            print("There is a problem at the target. Retry again in {} seconds".format(timeout_counter))
            continue
        except requests.exceptions.TooManyRedirects:
            print("There is something wrong with the URL, has the website moved?")
            raise MovedURL("Website has moved?")
        except requests.exceptions.RequestException as e:
            print("Something has horribly gone wrong, contact the developer")
            print(e)
            raise HorriblyGoneWrongError("Something has horribly gone wrong, contact the developer")
        break
        while r.status_code != 200:
            sleep(0.5)
            try:
                r = requests.get(url, headers=headers, timeout=10)
            except requests.exceptions.ConnectionError:
                print("Requests blocked! Lets wait for {} seconds".format(counter))
                counter *= counter
                continue
            except requests.exceptions.Timeout:
                print("There is a problem at the target. Retrying again in {} seconds".format(timeout_counter))
                continue
            except requests.exceptions.TooManyRedirects:
                print("There is somthing wrong with the URL, has the website moved?")
                raise MovedURL("Website has moved")
            except requests.exceptions.RequestException as e:
                print("Something horribly gone wrong, contact the developer")
                print(e)
                raise HorriblyGoneWrongError("Somethign has horribly gone wrong, contact the developer")
            break
        sleep(0.5)
    return BeautifulSoup(r.text, "html.parser")
