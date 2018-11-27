__author__ = "likthiis"

import pymysql.cursors
import getpass
import subprocess


class PageForAdmin:
    cursor = "init for use"
    database_list = []
    now_database = "(NO A NAME)you havent choosed"
    status_in_database = False
    myconnection = "init for use"
    username = ""
    password = ""
    current_table = ""
    tables_list = []

    def show_the_main_menu_to_admin(self):
        print("")
        print("--------Welcome to this management system--------\n")

        while True:
            print("------------Please choose our services-----------\n"
                  "-                                               -\n"
                  "-           [C] connect to database             -\n"
                  "-          [GG] help                            -\n"
                  "-           [Q] quit                            -\n"
                  "-                                               -\n"
                  "--------Now, use your keyboard and choose--------")

            choose = input(">>").strip()

            if choose == "C":
                print("C was input")
                self.connect_in_database()
            elif choose == "GG":
                print("help")
                self.instructions()
            elif choose == "Q":
                # Quit the system
                print("Quit the system, thanks for your using")
                break

    def connect_in_database(self):
        try:
            # connect mysql by name and pw(unittest)
            # self.cursor = pymysql.connect("localhost", "qinne", "111111")

            # connect mysql by name and pw(formal)
            print("Please input your name and your password")

            # invaild in pycharm
            # password = getpass.getpass("Password:")
            username = input("Name:")
            password = input("Password:")
            self.myconnection = pymysql.connect("localhost", username, password)
            self.cursor = self.myconnection.cursor()

            print("Result is " + str(self.cursor))
            print("Connection Success")
            self.preload(username=username, password=password)
            self.database_use_panel()
        except pymysql.err.OperationalError as e:
            print("Error occur:" + str(e))
            print("Connection Failed")

    def database_use_panel(self):
        print("------------Database Operation System------------\n")
        while True:
            print("------------Please choose our services-----------\n"
                  "-                                               -\n"
                  "-           [S] show all database               -\n"
                  "-         [TAS] show all table                  -\n"
                  "-          [CD] create one database             -\n"
                  "-          [SD] select one database             -\n"
                  "-          [ST] select one table                -\n"
                  "-          [CT] create one table                -\n"
                  "-           [I] insert one info                 -\n"
                  "-           [S] show one info                   -\n"
                  "-           [U] update one info                 -\n"
                  "-           [D] delete one info                 -\n"
                  "-          [GG] help                            -\n"
                  "-           [Q] quit                            -\n"
                  "-                                               -\n"
                  "--------Now, use your keyboard and choose--------")

            current_status = "Status:\nCurrent Database:%s\nCurrent User:%s" % (self.now_database, self.username)
            print(current_status)
            choose = input(">>").strip()

            if choose == "S":
                print("S was input")
                self.show_all_database()
            elif choose == "CD":
                print("CD was input")
                self.create_one_database()
            elif choose == "TAS" and self.status_in_database:
                print("TAS was input")
                self.show_all_table()
            elif choose == "CT" and self.status_in_database:
                print("CT was input")
                self.create_one_table()
            elif choose == "SD":
                print("SD was input")
                self.select_one_database()
            elif choose == "I" and self.status_in_database:
                print("I was input")
                self.insert_one_info()
            elif choose == "S" and self.status_in_database:
                print("S was input")
                self.show_one_info()
            elif choose == "U" and self.status_in_database:
                print("U was input")
                self.update_one_info()
            elif choose == "D" and self.status_in_database:
                print("D was input")
                self.delete_one_info()
            elif choose == "GG":
                print("help")
                self.instructions()
            elif self.status_in_database == False:
                print("You are out of any database, choose one first")
            elif choose == "Q":
                # Quit this subsystem
                print("Quit Database Operation System")
                break

    def instructions(self):
        pass

    def preload(self, username, password):
        self.cursor.execute('show databases')
        mylist = self.cursor.fetchall()
        self.username = username
        self.password = password
        for row in mylist:
            tmp = "%2s" % row
            self.database_list.append(tmp)

    def show_all_table(self):
        print("Now show all tables from " + self.now_database)
        # clean the list all
        self.tables_list.clear()

        self.cursor.execute("show tables from " + self.now_database)
        mylist = self.cursor.fetchall()
        for row in mylist:
            tmp = "%2s" % row
            tmp = tmp.strip()
            print(tmp)
            self.tables_list.append(tmp)

    def show_all_database(self):
        print("Now show all databases")
        for row in self.database_list:
            tmp = "%2s" % row
            print(tmp)

    def create_one_database(self):
        print("Input a name for creation:")
        new_one = input(">>")
        for row in self.database_list:
            if new_one == row:
                print("Database Exist")
                return

        result = self.cursor.execute('create database if not exists ' + new_one)
        if result == 1:
            print("Database Created Success")
        else:
            print("Database Failed")

    def select_one_database(self):
        try:
            print("Input a name for choosing:")
            # Close current connection, and open another one
            base_name = input(">>")
            self.cursor.close()
            self.myconnection.close()
            self.myconnection = pymysql.connect("localhost", self.username, self.password, base_name)
            self.cursor = self.myconnection.cursor()
            self.now_database = base_name
            self.status_in_database = True
            print("Connection Success, now use " + base_name)

        except pymysql.err.OperationalError as e:
            print("Error occur:" + str(e))
            print("Connection Failed")

    def table_create_detail_input(self):
        execute_sen = ""
        base_name = input("Input a name for creating a table:")
        execute_sen = "create table %s(" % (base_name.strip())
        column_input = True
        columns_name = []
        columns = {}
        is_it_has_key = False
        while column_input:
            name = input("Input a name for a column:")
            style = input("Input a style for a column:")

            if is_it_has_key == False:
                quit_ask = input("Want to make it primary key?(Y/N)")
                if quit_ask == "Y":
                    style += " auto_increment primary key"
                    is_it_has_key = True
                if quit_ask == "N":
                    style += ""

            columns[name] = style
            columns_name.append(name)

            quit_ask = input("Want to continue input?(Y/N)")
            if quit_ask == "Y":
                column_input = True
            if quit_ask == "N":
                column_input = False

        for name in columns_name:
            execute_sen += "%s %s," % (name, columns[name])

        execute_sen = list(execute_sen)
        execute_sen[len(execute_sen) - 1] = ")"
        execute_sen = ''.join(execute_sen)
        return execute_sen

    def create_one_table(self):
        try:
            execute_sen = self.table_create_detail_input()
            print(execute_sen)
            self.cursor.execute(execute_sen)
        except Exception as e:
            print("Error occur:" + str(e))

    def delete_one_info(self):
        pass

    def update_one_info(self):
        pass

    def show_one_info(self):
        pass

    def insert_one_info(self):
        self.describe_the_info()
        # Insert the info
        # 识别列的格式，自动帮助填补格式

        pass


    def describe_the_info(self):
        if len(self.tables_list) == 0:
            self.show_all_table()
        else:
            print("Here is the list of tables:")
            for row in self.tables_list:
                print(row)

        # Choose the table to insert
        # Describe the table
        table_name = input("Input the name of the table:")
        self.cursor.execute("desc " + table_name)
        column_info = self.cursor.fetchall()
        columns_detail = {}
        for row in column_info:
            tmp = "%2s" % str(row)
            print(tmp)
            # Handle the info of row
            start_end_dict = {"('": "',", ", '": "',"}
            dict_index = ["('", ", '"]
            # One column once
            column_name, column_style = self.analysis_column(start_end_dict, dict_index, tmp)
            columns_detail[column_name] = column_style
        print(columns_detail)

    def analysis_column(self, start_end_dict, dict_index, base_string):
        index_num = 0
        # Find the start index
        start1 = dict_index[index_num]
        end1 = start_end_dict[start1]
        s = base_string.find(start1)
        # -1 means we get the index for starting
        while s != -1:
            # Find the end index
            e = base_string.find(end1, s)
            # Cut the string
            sub_str = base_string[s+len(start1):e]

            if index_num == 0:
                column_name = sub_str
            if index_num == 1:
                column_style = sub_str

            # Now get the style
            index_num += 1
            if index_num == 2:
                # Will work after getting the name and style
                return column_name, column_style
            # Find the next start index
            start1 = dict_index[index_num]
            end1 = start_end_dict[start1]
            s = base_string.find(start1, e)


singular_point = PageForAdmin()
singular_point.show_the_main_menu_to_admin()
