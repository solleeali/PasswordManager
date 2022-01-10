import random, pickle, time


def fn_masterpass(n, d, m):
    name_wsp = n
    date_of_birth = d
    month_of_birth = m
    
    
    # Processing name for encryption
    name = ""
    name_lower = name_wsp.lower()
    name_strip = name_lower.strip()
    name_split = name_strip.split()
    for ch in name_split:
        name = name + ch
        
    name_for_pass = name[0:3]  # Final part of name prepared for the password
    
    # Processing date of birth for encryption
    if int(date_of_birth) % 2 == 0: # Special set : [!, @, #, $, &, *]
        sp_for_pass = "!@#"         # Deciding special character set on the basis of even or odd date
    else:
        sp_for_pass = "$&*"
    
    if len(date_of_birth) == 1:  # 3 numeric characters for password when number of digits is 1
        if int(date_of_birth) == 9:
            a, b, c = 9, 8, 7
        else:
            a = int(date_of_birth)
            b = (a + 1)
            c = (b + 1)
    elif len(date_of_birth) == 2:  # 4 numeric characters for password when number of digits is 2
        a = int(date_of_birth)
        b = a + 1
        c = ""
        
    A, B, C = str(a), str(b), str(c)
    
    num_for_pass = A + B + C
    
    # Processing month for encryption
    
    month_for_pass = month_of_birth.lower()
    
    password = name_for_pass + num_for_pass + month_for_pass + sp_for_pass
    
    return password




def fn_nextpass(lastpass):
    
    list_of_alpha = list("abcdefghijklmnopqrstuvwxyz")
    list_of_sp = ["!", "@", "#", "$", "&", "*"]
    
    nextpassword = ""
    
    for ch in lastpass:
    
        if ch.isalpha():
            
            ind_of_ch = list_of_alpha.index(ch.lower())
            
            ind_of_newch = ind_of_ch + 1
            
            if ind_of_newch >= 26:
                ind_of_newch = ind_of_newch - 26
            
            newch = list_of_alpha[ind_of_newch]
            
            dec_num = random.randint(0, 1)
            if dec_num == 0:
                x = newch.upper()
            else:
                x = newch.lower()
            
            nextpassword = nextpassword + x
            
        elif ch.isnumeric():
            a = int(ch)
            if a == 9:
                a = -1
                
            b = a + 1
            
            nextpassword = nextpassword + str(b)
        
        else:
            ind_of_spch = list_of_sp.index(ch)
            ind_of_newspch = ind_of_spch + 1
            
            if ind_of_newspch >= 6:
                ind_of_newspch = ind_of_newspch - 6
            
            newspch = list_of_sp[ind_of_newspch]
            
            nextpassword = nextpassword + newspch
        
    return nextpassword



def fn_make_user_data(n, d, m, p):
    
    mpass = fn_masterpass(n, d, m)
    userdata = {"username": n.lower(),
                "pin": pin,
                "passwords": {"masterpass": mpass,
                              
                              }
                }
    return userdata


def fn_dump_user_data(user_data, saved_data_list): # Add the new user data to the binary file
    
    
    file_obj = open("usersdata.bin", "wb")
    
    saved_data_list.append(user_data)
    
    pickle.dump(saved_data_list, file_obj)
    
    file_obj.close()
    print()
    print("User Data Saved Successfully!")



def fn_get_users_data(): # Get all the users data from binary and make it into a list
    
    saved_data_list = []
    file_obj = open("usersdata.bin", "rb")
    try:
        while True:
            bin_data = pickle.load(file_obj)
            saved_data_list = bin_data
    except:
        pass
    file_obj.close()
    
    return saved_data_list



def fn_display_users(list_of_data):  # Display all the users saved in the list of users data
    list_of_acc = []
    users = []
    
    for data in list_of_data:
        name_of_user = data["username"]
        
        list_of_acc = list(data["passwords"].keys())

        pass_count = len(list_of_acc) - 1
        
        if pass_count == 0:
            pass_count = "No"
        
        users.append((name_of_user, pass_count))
    
    print("All saved users:")
    index = 1
    for user, pass_count in users:
        print()
        print("\t" + " " + str(index) + " -> " + user + " : " + str(pass_count) + " password(s) saved.")
        index = index + 1
    
    if users == []:
        print("\t -> There's a little lonely here :( ")
        print("\t -> Seems like you're new here...")



def fn_selected_user_data(user_index, list_of_data):  # Use in case of existing users 
    
    selected_index = user_index - 1
    
    try:
        selected_user_data = list_of_data[selected_index]
    except:
        selected_user_data = None
    
    return selected_user_data



def fn_dump_generated_pass(account_name, selected_user_data, list_of_data):
    
    updated_list_of_data = []
    list_of_passw = []
    
    for passw in (selected_user_data["passwords"]).values():
        
        list_of_passw.append(passw)
    
    lastpass = list_of_passw[-1]
    
    nextpassword = fn_nextpass(lastpass)
    
    selected_user_data["passwords"][account_name] = nextpassword
    
    new_user_data = selected_user_data
    
    for data in list_of_data:
        if data["passwords"]["masterpass"] == new_user_data["passwords"]["masterpass"]:
            data = new_user_data
        
        updated_list_of_data.append(data)
    
    file_obj = open("usersdata.bin", "wb")
    
    pickle.dump(updated_list_of_data, file_obj)
    
    file_obj.close()
    
    return nextpassword, updated_list_of_data



def fn_display_user_passwords(selected_user_data):
    user_name = (selected_user_data["username"])
    list_of_passw = []
    index = 1
    print("\n" * 80)
    print("Logged in user :" + "\t" + user_name)
    print()
    print("Saved passwords of " + user_name + ": ")
    for old_account, passw in (selected_user_data["passwords"]).items():
        
        if old_account == "masterpass":
            continue
        print()
        print("\t" + str(index) + " -> " + old_account + " : " + passw)
        index = index + 1
        list_of_passw.append(passw)
        
    if list_of_passw == []:
        print("\t -> You don't have any passwords yet...")
        


def fn_new_user(list_of_data):
    
    userExists = False
    while not userExists:
        print()
        print()
        name = input("@ Please Enter Your Name (no spaces): " + "\t")
        print()
        
        userExists = fn_user_exists(name, listOfData)
        
        if name == "logout":
            return "logout", None, None, None
        
        if userExists:
            print()
            print("A user with name " + name + " already exists.")
            print()
            print("@ Try with another name :")
            print()
            print("@ Or type 'logout' to log yourself out:")
            userExists = False
            continue
        
        dob = input("@ Please Enter the Date You were Born in (in numbers only): " + "\t")
        print()
        mob = input("@ Please Enter the Month You were Born in (first 3 characters only): " + "\t")
        print()
        pin = input("@ Now Set Up A PIN for Authorization: "+"\t")
        print()
        userExists = True
        
    return name, dob, mob, pin


def fn_existing_user(selected_user_data):
    
    correct_pin = False
    existing_name = selected_user_data["username"]
    print("\n" * 80)
    print("Welcome " + existing_name + ",")
    while True:
        print()
        print("@ Type your pin : ")
        print()
        print()
        your_pin = input(": ")
        if your_pin == selected_user_data["pin"]:
            correct_pin = True
            break
        if your_pin.lower() == "logout":
            return "logout"
        print()
        print("\n" * 80)
        print("@ Incorrect Pin : " + "\t" + "Try Again")
        print()
        print("@ Or type 'logout' to log yourself out:")
        print()
        
    return correct_pin
    

def fn_create_new_pass(account_name, selected_user_data, list_of_data):
    
    newPass, updated_list_of_data = fn_dump_generated_pass(account_name, selected_user_data, list_of_data)
    
    return updated_list_of_data



def fn_user_exists(name, list_of_data):
    
    user_exists = False
    for userdata in list_of_data:
        
        if userdata["username"] == name:
            user_exists = True
    
    return user_exists
        

def fn_password_exists(account_name, selected_user_data):
    
    pass_exists = False
    list_of_accounts = []
    for old_account in (selected_user_data["passwords"]).keys():
        
        if old_account == "masterpass":
            continue
        list_of_accounts.append(old_account)
    
    for old_acc_name in list_of_accounts:
        if old_acc_name == account_name:
            pass_exists = True
            print("\n" * 80)
            print("A password with " + account_name + " already exists.")
            print()
            print("@ Try with another account name:")
    
    return pass_exists
        
    
def fn_update_pass(account_name, selected_user_data, list_of_data):
    
    updated_list_of_data = []
    
    old_passw = selected_user_data["passwords"][account_name]
    
    new_pass = fn_nextpass(old_passw)
    
    selected_user_data["passwords"][account_name] = new_pass
    
    
    for data in list_of_data:
        
        if selected_user_data["passwords"]["masterpass"] == data["passwords"]["masterpass"]:
            data = selected_user_data
        
        updated_list_of_data.append(data)
    
    
    file_obj = open("usersdata.bin", "wb")
    
    pickle.dump(updated_list_of_data, file_obj)
    
    return updated_list_of_data
    
    


def fn_delete_pass(account_name, selected_user_data, list_of_data):
    
    updated_list_of_data = []
    
    del selected_user_data["passwords"][account_name]
    
    for data in list_of_data:
        
        if selected_user_data["passwords"]["masterpass"] == data["passwords"]["masterpass"]:
            data = selected_user_data
        
        updated_list_of_data.append(data)
    
    file_obj = open("usersdata.bin", "wb")
    
    pickle.dump(updated_list_of_data, file_obj)
    
    return updated_list_of_data


def fn_animation(message):
    
    evenlength = False
    limit = len(message)
    if limit % 2 == 0:
        evenlength = True
    hlimit = limit//2
    
    for i in range(0, hlimit):
        messg1 = (" " * i) + "*" + (" " * (hlimit - (i + 1)))
        if evenlength:
            messg2 = ""
        else:
            messg2 = " "
        messg3 = (" " * (hlimit - (i + 1))) + "*" + (" " * i)
        messg = messg1 + messg2 + messg3
        print(messg)
        time.sleep(0.5)
    print(message)
    time.sleep(0.5)
    
    for i in range(0, hlimit):
        messg1 = (" " * (hlimit - (i + 1))) + "*" + (" " * i)
        if evenlength:
            messg2 = ""
        else:
            messg2 = " "
        messg3 = (" " * i) + "*" + (" " * (hlimit - (i + 1)))
        messg = messg1 + messg2 + messg3
        print(messg)
        time.sleep(0.5)


file_obj = open("usersdata.bin", "ab")
file_obj.close()

heading = '''

                                                          __
    ____   ____ _ _____ _____ _      __ ____   _____ ____/ /
   / __ \ / __ `// ___// ___/| | /| / // __ \ / ___// __  / 
  / /_/ // /_/ /(__  )(__  ) | |/ |/ // /_/ // /   / /_/ /  
 / .___/ \__,_//____//____/  |__/|__/ \____//_/    \__,_/   
/_/____ ___   ____ _ ____   ____ _ ____ _ ___   _____       
  / __ `__ \ / __ `// __ \ / __ `// __ `// _ \ / ___/       
 / / / / / // /_/ // / / // /_/ // /_/ //  __// /           
/_/ /_/ /_/ \__,_//_/ /_/ \__,_/ \__, / \___//_/            
                                /____/
            
                                Created By Julie / Muhriz

'''



while True:
    
    print(heading)
    
    listOfData = fn_get_users_data()
    fn_display_users(listOfData)
    
    newUser = False
    LoggedIn = False
    
    print()
    print("@ Select from above existing users to login (Enter only the 'index number'):")
    print()
    print("@ Are you a new user?")
    print()
    print("@ Type 'newuser' if yes :")
    print()
    print()
    resp = input(": ")
        
    if resp.lower() == "newuser":
        newUser = True
    
    if newUser:
        print("\n" * 80)
        
        name, dob, mob, pin = fn_new_user(listOfData)
        
        if name == "logout":
            continue
        
        if name == None:
            continue
        
        userDictData = fn_make_user_data(name, dob, mob, pin)
        
        selectedUserData = userDictData
        
        fn_dump_user_data(selectedUserData, listOfData)
        
        LoggedIn = True
    
    if resp.isnumeric():
        
        userIndex = int(resp)
        
        selectedUserData = fn_selected_user_data(userIndex, listOfData)
        
        if selectedUserData == None:
            fn_animation("User does not exist.")
            continue
            
        LoggedIn = fn_existing_user(selectedUserData)
        
        
    if resp.lower() == "clear":
        file_obj = open("usersdata.bin", "wb")
        file_obj.close()
        continue
    
    if LoggedIn == "logout":
        continue
    
    while LoggedIn:
        
        fn_display_user_passwords(selectedUserData)
        print()
        print()
        print("@ Type 'newpass' to create a new password:")
        print()
        print("@ Type 'logout' to log yourself out:")
        print()
        print("@ Type 'update <account_name>' to update the password:")
        print()
        print("@ Type 'delete <account_name>' to delete the password:")
        print()
        print()
        
        sec_resp = input(": ").lower()
        
        while sec_resp == "newpass":
                            
            print()
            print()
            print("@ Type the account name for the password:")
            print()
            print("(for eg. google, facebook, instagram etc.)")
            print()
            accountName = input(": ")
            
            passwordExists = fn_password_exists(accountName, selectedUserData)
            
            if not passwordExists:
                listOfData = fn_create_new_pass(accountName, selectedUserData, listOfData)
                sec_resp = "notnewpass"
        
        
        if "update" in sec_resp:
            
            update_options = sec_resp.split()
            
            updateAccountName = update_options[1]
            
            accountList = list(selectedUserData["passwords"].keys())
            
            if updateAccountName not in accountList:
                
                fn_animation(updateAccountName + " does not exist.")
                continue
            listOfData = fn_update_pass(updateAccountName, selectedUserData, listOfData)
            
        
        if "delete" in sec_resp:
            
            delete_options = sec_resp.split()
            
            deleteAccountName = delete_options[1]
            
            accountList = list(selectedUserData["passwords"].keys())
            
            if deleteAccountName not in accountList:
                
                fn_animation(deleteAccountName + " does not exist.")
                continue
            listOfData = fn_delete_pass(deleteAccountName, selectedUserData, listOfData)


        if sec_resp == "logout":
            LoggedIn = False
    