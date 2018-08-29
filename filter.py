# DTC 2 Section 14, Team 4
# Written by: Jack Wiig
# Purpose: This file filters MAC Addresses that have been scanned from the network and stored in MACList.txt alongside
# the users registered through the website.
# Output: This file outputs to here.csv and notHere.csv, two "Comma Separated Value" files that are formatted to be
# tables on the website.


# Device class, which simply groups together the name of a person's device and its MAC address.
class Device:
    def __init__(self, name, mac):
        self.n = name
        self.m = mac


# This is a Person class, which ties a person's name to a list of devices
class Person:
    def __init__(self, name):
        self.n = name
        self.d = []

    def add_device(self, device):
        self.d.append(device)


# A Node, containing a letter, in a Trie
class TrieNode:
    def __init__(self, data, last_letter, first_child, next_sibling):
        self.data = data
        self.last = last_letter
        self.first_child = first_child
        self.next_sibling = next_sibling


# Type of Tree that stores one letter in a word per generation, called a Trie.
class Trie:
    def __init__(self):
        self.root = TrieNode("\0", False, None, None)

    def add(self, word): 
        current_node = self.root  
        last_node = self.root 
        last_sibling = self.root 

        found = True

        for letter in word:
            if found:
                last_node = current_node
                current_node = current_node.first_child
                found = False

                if current_node is not None:
                    if current_node.data == letter:
                        found = True

                    else:
                        sibling_node = current_node.next_sibling
                        last_sibling = current_node

                        while sibling_node is not None:
                            if sibling_node.data == letter:
                                current_node = sibling_node
                                found = True
                                break

                            last_sibling = sibling_node
                            sibling_node = sibling_node.next_sibling

            if not found:
                if current_node is None:
                    current_node = TrieNode(letter, False, None, None)
                    last_node.first_child = current_node

                else:
                    last_sibling.next_sibling = TrieNode(letter, False, None, None)
                    current_node = last_sibling.next_sibling

                last_node = current_node
                current_node = current_node.first_child

        last_node.last = True

    def contains(self, word):
        current_node = self.root

        for letter in word:
            current_node = current_node.first_child
            found = False

            if current_node is None:
                return False

            if current_node.data == letter:
                found = True

            else:
                while current_node is not None:
                    if current_node.data == letter:
                        found = True
                        break

                    current_node = current_node.next_sibling

            if not found:
                return False

        if current_node.last:
            return True

        return False


# Reads MAC addresses from a file and returns them in an array
def get_mac_list(mac_file):

    imported_mac = open(mac_file, "r")

    mac_list = Trie()

    for mac in imported_mac:
        mac = mac.rstrip("\n").lower()
        mac_list.add(mac)

    imported_mac.close()

    return mac_list


# Reads user data from file and returns it in an array
def get_users(user_file):

    user_lines = []
    user_list = []

    user_base = open(user_file, "r")

    for read_lines in user_base:
        user_lines.append(read_lines)

    user_base.close()

    for i in range(0, len(user_lines), 3):
        name_in_parts = user_lines[i].split("@@@")
        user_name = ""

        for part in name_in_parts:
            user_name += " " + part

        user_name = user_name.lstrip(" ")
        user_name = user_name.rstrip("\n")

        device_name = user_lines[i + 1].rstrip("\n")
        device_mac = user_lines[i + 2].rstrip("\n")

        new_device = Device(device_name, device_mac)

        exists = False

        for user in user_list:
            if user_name == user.n:
                user.d.append(new_device)
                exists = True

        if not exists:
            new_person = Person(user_name)
            new_person.add_device(new_device)
            user_list.append(new_person)

    return user_list


# Runs the program
def main():
    here = open("/home/pi/CatConnect/here.csv", "w+")
    here.write("Name,Device(s)\n")

    not_here = open("/home/pi/CatConnect/notHere.csv", "w+")
    not_here.write("Name\n")

    address_list = get_mac_list("/home/pi/CatConnect/MACList.txt")
    user_list = get_users("/var/lib/mysql/wordpress/users.txt")

    for user in user_list:

        connected = []

        for device in user.d:
            if address_list.contains(device.m.lower()):
                connected.append(device.n)

        if connected:
            here.write(user.n + ",")

            device_list = "\""

            for device_name in connected:
                device_list += device_name + ", "

            device_list = device_list.rstrip(", ")
            device_list += "\"\n"
            here.write(device_list)

        else:
            not_here.write(user.n + "\n")

    here.close()
    not_here.close()


main()