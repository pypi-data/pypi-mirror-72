import os, sys, time, imaplib, email

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rstdepassuredtchnq.core.base.config import email_conf as conf_file


class Email_Util:

    def connect(self, imap_host):
        self.mail = imaplib.IMAP4_SSL(imap_host)
        return self.mail

    def login(self, username, password):
        result_flag = False
        try:
            self.mail.login(username, password)
        except Exception as e:
            print('\nException in Email_Util.login')
            print('PYTHON SAYS:')
            print(e)
            print('\n')
        else:
            result_flag = True

        return result_flag

    def get_folders(self):
        return self.mail.list()

    def select_folder(self, folder):
        result_flag = False
        response = self.mail.select(folder)
        if response[0] == 'OK':
            result_flag = True

        return result_flag

    def get_latest_email_uid(self, subject=None, sender=None, time_delta=10, wait_time=300):
        global item_list
        uid = None
        time_elapsed = 0
        search_string = ''
        if subject is None and sender is None:
            search_string = 'ALL'

        if subject is None and sender is not None:
            search_string = '(FROM "{sender}")'.format(sender=sender)

        if subject is not None and sender is None:
            search_string = '(HEADER Subject "{subject}")'.format(subject=subject)

        if subject is not None and sender is not None:
            search_string = '(FROM "{sender}" HEADER Subject "{subject}")'.format(sender=sender, subject=subject)

        print("  - Automation will be in search/wait mode for max %s seconds" % wait_time)

        item_list = self.all_get_uid(time_elapsed, wait_time, time_delta, search_string, uid)
        print('Items Listed %s' % item_list)

        return item_list[-1]

    def all_get_uid(self, time_elapsed, wait_time, time_delta, search_string, uid):
        global item_list
        while (time_elapsed < wait_time and uid is None):
            time.sleep(time_delta)
            result, data = self.mail.uid('search', None, str(search_string))
            item_list = data[0].split()
            print('\n ------------- Latest Email UID %s' % item_list)
            print('\n ------------- Latest Email UID %s' % item_list[-1])
            print('\n ------------- Oldest Email UID %s' % item_list[0])

            if data[0].strip() != '':  # Check for an empty set
                uid = data[0].split()[-1]

            time_elapsed += time_delta

        return item_list

    def fetch_email_body(self, uid):
        "Fetch the email body for a given uid"
        email_body = []
        if uid is not None:
            result2, email_data = self.mail.uid('fetch', uid, '(RFC822)')
            raw_email = email_data[0][1]
            print('Raw Email Message \n %s' % raw_email)
            email_msg = email.message_from_string(raw_email.decode('utf-8'))
            print('Email Message \n %s' % email_msg)
            email_body = self.get_email_body(email_msg)
            print('Email Body \n %s' % email_body)

        return email_body

    def get_email_body(self, email_msg):
        "Parse out the text of the email message. Handle multipart messages"
        email_body = []
        maintype = email_msg.get_content_maintype()
        if maintype == 'multipart':
            for part in email_msg.get_payload():
                if part.get_content_maintype() == 'text':
                    email_body.append(part.get_payload())
        elif maintype == 'text':
            email_body.append(email_msg.get_payload())

        print('get_email_body Value is %s' % email_body)

        return email_body

    def logout(self):
        "Logout"
        result_flag = False
        response = self.mail.logout()
        if response == 'BYE':
            result_flag = True

        return result_flag


# ---EXAMPLE USAGE---
if __name__ == '__main__':
    # Fetching conf details from the conf file
    imap_host = conf_file.imaphost
    username = conf_file.username
    password = conf_file.app_password

    # Initialize the email object
    email_obj = Email_Util()

    # Connect to the IMAP host
    email_obj.connect(imap_host)

    # Login
    if email_obj.login(username, password):
        print("PASS: Successfully logged in.\n")
    else:
        print("FAIL: Failed to login")

    # Get a list of folder
    folders = email_obj.get_folders()
    print(folders)
    if folders != None or []:
        print("\n PASS: Email folders: \n", email_obj.get_folders())

    else:
        print("FAIL: Didn't get folder details")

    # Select a folder
    if email_obj.select_folder('Inbox'):
        print("PASS: Successfully selected the folder: Inbox")
    else:
        print("FAIL: Failed to select the folder: Inbox")

    # ----------------------------------------------------------------------------------------------------------------
    # ------------------------------       Fetch Email with Subject & Sender      ------------------------------------
    # ----------------------------------------------------------------------------------------------------------------
    #
    unique_sender_subject_latest_email_uid = email_obj.get_latest_email_uid(
        subject='Fwd: Action Needed: Update your PayPal info', sender='deepirms2619@gmail.com',
        wait_time=2)
    print('Latest Email UID is %s ' % unique_sender_subject_latest_email_uid)
    unique_sender_subject_email_body = email_obj.fetch_email_body(unique_sender_subject_latest_email_uid)
    print('Latest Email Body of Unique Sender is %s ' % unique_sender_subject_email_body)

    data_sender_subject_flag = False
    for line in unique_sender_subject_email_body:
        line = line.replace('=', '')
        line = line.replace('<', '')
        line = line.replace('>', '')

        if "Connect your Paypal Now:" and "We are writing today because we need you to update your Upwork payment" in line:
            data_sender_subject_flag = True
            break
    if data_sender_subject_flag == True:
        print("PASS: Automation provided correct Email details. Email contents matched with provided data.")
    else:
        print(
            "FAIL: Provided data not matched with Email contents. Looks like automation provided incorrect Email details")

    # ----------------------------------------------------------------------------------------------------------------
    # ------------------------------------  Fetch Email with only Sender    ------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------
    #
    unique_sender_latest_email_uid = email_obj.get_latest_email_uid(sender='deepirms2619@gmail.com',
                                                                    wait_time=2)
    print('Latest Email UID is %s ' % unique_sender_latest_email_uid)
    unique_sender_email_body = email_obj.fetch_email_body(unique_sender_latest_email_uid)
    print('Latest Email Body of Unique Sender is %s ' % unique_sender_email_body)

    data_flag = False
    for line in unique_sender_email_body:
        line = line.replace('=', '')
        line = line.replace('<', '')
        line = line.replace('>', '')

        if "Spaces for you" and "Follow some interesting Spaces below to get started." in line:
            data_flag = True
            break
    if data_flag == True:
        print("PASS: Automation provided correct Email details. Email contents matched with provided data.")
    else:
        print(
            "FAIL: Provided data not matched with Email contents. Looks like automation provided incorrect Email details")

    # ----------------------------------------------------------------------------------------------------------------
    # -----------------------------------   Fetch Email with only Subject  ------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------
    #
    unique_latest_email_uid = email_obj.get_latest_email_uid(subject='Pulse - Account creation request', wait_time=2)
    print('Latest Email UID is %s ' % unique_latest_email_uid)
    unique_email_body = email_obj.fetch_email_body(unique_latest_email_uid)
    print('Latest Email Body is %s ' % unique_email_body)

    # Get the latest email's unique id
    latest_email_uid = email_obj.get_latest_email_uid(wait_time=2)
    print('Latest Email UID is %s ' % latest_email_uid)
    if latest_email_uid != None:
        print("PASS: Unique id of the latest email with given sender is: ", latest_email_uid)

        # Check the text of the latest email id
        email_body = email_obj.fetch_email_body(latest_email_uid)
        data_flag = False
        print("\n  - Automation checking mail contents")
        for line in email_body:
            line = line.replace('=', '')
            line = line.replace('<', '')
            line = line.replace('>', '')

            if "Critical security alert" and "Access for less secure apps has been turned on" in line:
                data_flag = True
                break
        if data_flag == True:
            print("PASS: Automation provided correct Email details. Email contents matched with provided data.")
        else:
            print(
                "FAIL: Provided data not matched with Email contents. Looks like automation provided incorrect Email details")

    else:
        print("FAIL: After wait of 5 mins, looks like there is no email present with given sender")
