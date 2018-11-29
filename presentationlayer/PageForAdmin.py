__author__ = "likthiis"

import pymysql.cursors
import getpass
import subprocess


class PageForAdmin:
    cursor = "init for use"
    database_list = []
    now_database = "(NO A NAME)you have not chose"
    status_in_database = False
    myconnection = "init for use"
    username = ""
    password = ""
    current_table = "(NO A NAME)you have not chose"
    tables_list = []
    temp_rows_detail = {}
    temp_rows_name = []

    # Hello, if you are a visitor, read this function clearly for understanding what this system goes.
    def show_the_main_menu_to_admin(self):
        print("")
        print("--------Welcome to this management system--------\n")

        while True:
            print("------------Please choose our services-----------\n"
                  "-        'help' for detail                      -\n"
                  "-        [gate] database connect                -\n"
                  "-        [help] help                            -\n"
                  "-        [quit] quit                            -\n"
                  "-                                               -\n"
                  "--------Now, use your keyboard and choose--------")

            choose = input(">>").strip()

            # UnitTest
            # Empty Code

            # Format Work
            if choose[0:4] == "gate":
                # Command will be:gate -u username -p password
                self.connect_in_database(choose)
            elif choose[0:4] == "help":
                print("help")
                self.instructions()
            elif choose[0:4] == "quit":
                # Quit the system
                print("Quit the system, thanks for your using")
                break

    def command_check(self, command):
        # Command will be:gate -u username -p password
        # Skin the pea!
        # Find the index of '-u'
        s = command.find("-u")
        if s == -1:
            print("Format Error, check your arguments")
            return

        # Strip Work
        if command[s + 2] != " ":
            print("Format Error, check your arguments")
            return

        while command[s + 2] == " ":
            s += 1

        command = command[s + 2:]
        # Get your username
        s = command.find("-p")
        if s == -1:
            print("Format Error, check your arguments")
            return

        while command[s - 1] == " ":
            # Strip Work
            s -= 1
        username = command[0:s]
        # print(username.strip())

        # Get your password
        s = command.find("-p")
        # Strip Work
        if command[s + 2] != " ":
            print("Format Error, check your arguments")
            return

        while command[s + 2] == " ":
            s += 1
        password = command[s + 2:]
        return username, password

    def connect_in_database(self, command):
        try:
            username, password = self.command_check(command)
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
        show_the_menu = "need"
        while True:

            if show_the_menu == "need":
                print("------------Please choose our services-----------\n"
                      "-                                               -\n"
                      "-            [show 'dbs'/'tables']              -\n"
                      "-                 [tds/tas]                     -\n"
                      "-               [use database]                  -\n"
                      "-             [create db database]              -\n"
                      "-          [CD] create one database             -\n"
                      "-          [CT] create one table                -\n"
                      "-           [I] insert one info                 -\n"
                      "-           [S] show one info                   -\n"
                      "-           [U] update one info                 -\n"
                      "-           [D] delete one info                 -\n"
                      "-                   [help]                      -\n"
                      "-                   [hide]                      -\n"
                      "-                   [quit]                      -\n"
                      "-                                               -\n"
                      "--------Now, use your keyboard and choose--------")

                current_status = "Status:\n" \
                                 "Current Database:%s\n" \
                                 "Current Table:%s\n" \
                                 "Current User:%s\n" % (self.now_database, self.current_table, self.username)
                print(current_status)
            show_the_menu = "need"
            choose = input(">>").strip()

            if choose[0:4] == "show":
                show_the_menu = "needn't"
                if choose[4] != " ":
                    print("Format Error, check your command")
                    continue
                choose = choose[4:].strip()
                if choose == "dbs":
                    self.show_all_database()
                if choose == "tables" and self.status_in_database:
                    self.show_all_table()

            if choose == "tds":
                show_the_menu = "needn't"
                self.show_all_database()
            elif choose == "tas" and self.status_in_database:
                self.show_all_table()

            if choose == "tas":
                show_the_menu = "needn't"

            if choose[0:3] == "use":
                # use database or use table
                if choose[3] != " ":
                    print("Format Error, check your command")
                    continue
                choose = choose[3:].strip()
                # choose must be a name of database or table
                # use self.status_in_database to judge
                a = False
                for row in self.database_list:
                    if choose == row:
                        a = True
                        show_the_menu = "needn't"
                        self.select_one_database(choose)

                if a is False or self.status_in_database is False:
                    show_the_menu = "needn't"
                    print("This name cannot be found in databases, please check clearly")

            if choose[0:6] == "create":
                if choose[6] != " ":
                    print("Format Error, check your command")
                    continue
                choose = choose[6:].strip()
                if choose[0:3] != "db ":
                    print("Format Error, check your command")
                    continue

                if choose[0:2] == "db":
                    show_the_menu = "needn't"
                    choose = choose[2:].strip()
                    print(choose)
                    self.create_one_database(choose)


            if choose == "CD":
                print("CD was input")
                self.create_one_database()
            elif choose == "CT" and self.status_in_database:
                print("CT was input")
                self.create_one_table()
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
            elif choose == "help":
                print("help")
                self.instructions()
            # elif self.status_in_database is False:
            #     print("You are out of any database, choose one first")
            elif choose == "quit":
                # Quit this subsystem
                print("Quit Database Operation System")
                break

    def instructions(self):
        print("HELP:")
        print("   COMMAND   AUG_NUM   AUG_LIST\n"
              "   gate      2         [-u username must, -p password must]\n"
              "   use for connecting your database\n"
              "   help      0         []\n"
              "   use for getting the detail of commands\n"
              "   quit      0         []\n"
              "   use for quitting the system\n"
              "   show      1         ['dbs'/'tables' must]\n"
              "   show all databases or tables, you can only get tables while in exact database\n"
              "   tds       0         []\n"
              "   show databases quickly\n"
              "   tas       0         []\n"
              "   show tables quickly\n"
              )

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

    def create_one_database(self, new_one):
        # print("Input a name for creation:")
        # new_one = input(">>")
        for row in self.database_list:
            if new_one == row:
                print("Database Exist")
                return

        result = self.cursor.execute('create database if not exists ' + new_one)
        if result == 1:
            print("Database Created Success")
        else:
            print("Database Failed")

    def select_one_database(self, database_name):
        try:
            # print("Input a name for choosing:")
            # Close current connection, and open another one
            # base_name = input(">>")
            self.cursor.close()
            self.myconnection.close()
            self.myconnection = pymysql.connect("localhost", self.username, self.password, database_name)
            self.cursor = self.myconnection.cursor()
            self.now_database = database_name
            self.status_in_database = True
            print("Connection Success, now use " + database_name)

        except pymysql.err.OperationalError as e:
            print("Error occur:" + str(e))
            print("Connection Failed")

    def table_create_detail_input(self):
        execute_sen = ""
        base_name = input("Input a name for creating a table:")
        execute_sen = "create table %s(" % (base_name.strip())
        row_input = True
        rows_name = []
        rows = {}
        is_it_has_key = False
        while row_input:
            name = input("Input a name for a row:")
            style = input("Input a style for a row:")

            if is_it_has_key == False:
                quit_ask = input("Want to make it primary key?(Y/N)")
                if quit_ask == "Y":
                    style += " auto_increment primary key"
                    is_it_has_key = True
                if quit_ask == "N":
                    style += ""

            rows[name] = style
            rows_name.append(name)

            quit_ask = input("Want to continue input?(Y/N)")
            if quit_ask == "Y":
                row_input = True
            if quit_ask == "N":
                row_input = False

        for name in rows_name:
            execute_sen += "%s %s," % (name, rows[name])

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
        try:
            # Show all rows' name for checking
            self.describe_the_info()
            fields = ""
            for name in self.temp_rows_name:
                fields += name + ","
            fields = fields[:-1]
            row_name = input("Input the row's name which you will use to query(%s):" % fields)

            i = 1

            for name in self.temp_rows_name:
                if name == row_name:
                    i = 0
                    break

            if i == 1:
                print("Row's name wrong, back to menu")

            row_info = input("Input the info of this row(style:%s):" % self.temp_rows_detail[row_name])
            row_want = input("Input the raw you want to know, '*' means all, row divided by dot:")

            self.cursor.execute("select %s from %s where %s = '%s'" % (row_want, self.current_table, row_name, row_info))
            get_info = self.cursor.fetchall()
            print("Result Show")
            for row in get_info:
                print(str(row))

        except pymysql.err.ProgrammingError as pe:
            print("Error occur:" + str(pe))
        except TypeError as te:
            print("Error occur " + str(te))

    def insert_one_info(self):
        try:
            self.describe_the_info()
            # Insert the info
            i = len(self.temp_rows_detail) - 1
            ii = 0

            row_datas = {}
            fields = ""
            datas = ""

            print("Please input your data, input NULLPY for ignore this column")
            while ii <= i:
                # 将数据表暂存表分拆表示，用以用户输入数据
                row_name = self.temp_rows_name[ii]
                row_style = self.temp_rows_detail[row_name]
                row_data = input("%s[style limit:%s]>>" % (row_name, row_style))
                if row_data.strip() != "NULLPY":
                    row_datas[row_name] = row_data
                    fields += row_name + ","
                    datas += "'" + row_data + "'" + ","
                ii += 1

            if fields == "" or datas == "":
                print("Empty data, stop insert")
                return

            fields = fields[:-1]
            datas = datas[:-1]
            row_insert_execute_sen = "insert into %s(%s) values(%s)" % (self.current_table, fields, datas)
            print(row_insert_execute_sen)
            result = self.cursor.execute(row_insert_execute_sen)
            self.myconnection.commit()
            if result == 1:
                print("Insert Success")
            else:
                print("Insert Fail")
        except pymysql.err.ProgrammingError as pe:
            print("Error occur:" + str(pe))


    def describe_the_info(self):
        try:
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
            row_info = self.cursor.fetchall()
            self.temp_rows_detail.clear()
            self.temp_rows_name.clear()
            self.current_table = table_name
            for row in row_info:
                tmp = "%2s" % str(row)
                # print(tmp)
                # Handle the info of row
                start_end_dict = {"('": "',", ", '": "',"}
                dict_index = ["('", ", '"]
                # One row once
                row_name, row_style = self.analysis_row(start_end_dict, dict_index, tmp)
                self.temp_rows_detail[row_name] = row_style
                self.temp_rows_name.append(row_name)
            print(self.temp_rows_detail)
        except pymysql.err.ProgrammingError as pe:
            print("Error occur " + pe)

    def analysis_row(self, start_end_dict, dict_index, base_string):
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
                row_name = sub_str
            if index_num == 1:
                row_style = sub_str

            # Now get the style
            index_num += 1
            if index_num == 2:
                # Will work after getting the name and style
                return row_name, row_style
            # Find the next start index
            start1 = dict_index[index_num]
            end1 = start_end_dict[start1]
            s = base_string.find(start1, e)


singular_point = PageForAdmin()
singular_point.show_the_main_menu_to_admin()
