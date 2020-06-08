from selenium import webdriver
from time import sleep
from pw import pw


class InstagramBot:

    def __init__(self, username, password):
        """
        Initializes bot. Gets You to main Instagram page (feed)
        :param username: Your username
        :param password: Your password

        """
        self.username = username
        self.followers = []
        self.followings = []

        self.driver = webdriver.Chrome()

        self.driver.get("https://www.instagram.com")
        sleep(2)  # Wait 2 seconds to load
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").\
            send_keys(username)  # Find username box and put in given username

        self.driver.find_element_by_xpath("//input[@name=\"password\"]"). \
            send_keys(password)  # Find password box and put in given password

        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        # Click login and go to feed

        sleep(5)

    def find_my_followers(self, number_of_followers) -> None:

        """
        Gets all the followers you currently have and puts their username into
        a list.

        :param number_of_followers: The number of followers you currently have
        """

        self.driver.get("https://www.instagram.com/" + self.username + "/")
        #  Go to user page
        sleep(2)

        self.driver.find_element_by_xpath(
            "//a[contains(@href,'/followers')]").click()  # Go to followers list
        sleep(2)

        popup = self.driver.find_element_by_class_name('isgrP')
        followers_list = []
        actual = number_of_followers - 6  # has to be -6 due to the height of
        # the box, otherwise it does not get all the users

        while len(followers_list) <= actual:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight', popup)
            sleep(0.3)
            followers = self.driver.find_elements_by_class_name('FPmhX')

            for follower in followers:
                if follower.text not in followers_list:
                    followers_list.append(follower.text)

        self.followers = followers_list

    def find_my_following(self, number_of_following) -> None:

        """
        Gets all the usernames of people that ypu currently follow

        :param number_of_following: The number of people you currently follow.
        """

        self.driver.get("https://www.instagram.com/" + self.username + "/")
        sleep(2)

        self.driver.find_element_by_xpath(
            "//a[contains(@href,'/following')]").click()
        sleep(2)

        popup = self.driver.find_element_by_class_name('isgrP')
        following_list = []
        actual = number_of_following - 6

        while len(following_list) <= actual:
            self.driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight', popup)
            sleep(0.3)
            followings = self.driver.find_elements_by_class_name('FPmhX')

            for following in followings:
                if following.text not in following_list:
                    following_list.append(following.text)

        self.followings = following_list

    def get_users(self) -> [str]:

        """
        Compares followers and following. Puts the people that you follow who
        dont follow you back into a list.

        :return: list of usernames
        """

        lst = []

        for following in self.followings:
            if following not in self.followers:
                lst.append(following)

        return lst


def put_unfaithful_in_txt_file(lst: [str]) -> None:

    """
    Puts the people that you follow who dont follow you back into txt file.

    :param lst: list of usernames of people that you follow but dont follow you
    back.

    """

    with open('users.txt', mode='w') as file:
        header = 'Users that do not follow you back:\n'
        file.write(header)

        for person in lst:
            file.write(person + '\n')

    file.close()


if __name__ == "__main__":

    numb_of_followers = 438
    numb_of_following = 869
    un = ""  # Username

    bot = InstagramBot(un, pw)
    bot.find_my_followers(numb_of_followers)
    bot.find_my_following(numb_of_following)

    users = bot.get_users()
    put_unfaithful_in_txt_file(users)
