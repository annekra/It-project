import sqlite3
import pprint
conn = sqlite3.connect('messenger.sqlite')
c=conn.cursor()
pp = pprint.PrettyPrinter(indent=1, width=80, compact=False)
ppp = pprint.PrettyPrinter(indent=1, width=80, compact=True)
c.execute('''PRAGMA foreign_keys = 1''')

# Пример корректного ввода данных в каждую таблицу
c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('turnoff', 'Виктор Тернов', 'turnoff@gmail.com', 'idktexttext')")
conn.commit()

c.execute("INSERT INTO contact(id_user, id_contact) VALUES (1,4), (4,1)")
conn.commit()

c.execute("INSERT INTO chat_all_all(creator) VALUES (4)")
conn.commit()

c.execute("INSERT INTO chat_all_for_one(id_ch_c, id_user_add, time_add) VALUES (11, 10, '2024-05-18 11:17:32')")
conn.commit()

c.execute("INSERT INTO message_sskp(id_user, sms, type_sms, time) values (10, 'Сессия близко...', 'text', '2024-05-18 11:18:30')")
conn.commit()

c.execute("INSERT INTO chat(id_person_chat, id_stroke) values (2,6)")
conn.commit()


# Пример корректного удаления данных из каждой таблицы
c.execute("DELETE from chat where id_person_chat = 2 and id_stroke = 6")
conn.commit()

c.execute("DELETE from message_sskp where id_stroke = 6")
conn.commit()

c.execute("DELETE from chat_all_for_one where id_ch_c = 11 and id_user_add = 10")
conn.commit()

c.execute("DELETE from chat_all_all where id_chat = 13")
conn.commit()

c.execute("DELETE from contact where id_user = 1 and id_contact = 4")
conn.commit()

c.execute("DELETE from user where id_user = 24")
conn.commit()


# Пример корректного изменения данных в таблице
c.execute("UPDATE chat_all_all set (name, change_name) = ('GG', 1) where id_chat = 2")
conn.commit()


# Пример корректного изменения таблиц после удаления пользователя
c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('turnoff', 'Виктор Тернов', 'turnoff@gmail.com', 'idktexttext')")
conn.commit()

c.execute("INSERT INTO chat_all_for_one(id_ch_c, id_user_add, time_add) VALUES (11, 24, '2024-05-18 11:17:32')")
conn.commit()

c.execute("INSERT INTO message_sskp(id_user, sms, type_sms, time) values (24, 'Сессия близко...', 'text', '2024-05-18 11:18:30')")
conn.commit()

c.execute("INSERT INTO chat(id_person_chat, id_stroke) values (11,6)")
conn.commit()

c.execute("DELETE from user where id_user = 24")
conn.commit()

"""
User with error (надо же показать ей что все check unique получается работают как и триггеры)
c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('vikysia', 'Аргентум Виктория', 'kryt@mail.ru','dfghbuk564hbj')")
conn.commit()
UNIQUE constraint failed: user.nickname

c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('vikysi', 'Аргентум Виктор', 'kryt@mail.ru','dfghbuk564hbj')")
conn.commit()
UNIQUE constraint failed: user.mail

c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('', 'Аргентум Урия', 'kry1t@mail.ru','dfghbuk564hbj')")
conn.commit()
CHECK constraint failed: CK_user_nickname

c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('asdfghjkl;lkjhgfdsdfffghijkkojiuytrghjkl;gdrtfytfutfkjhftghjk', 'Аргентум Урия', 'kry1t@mail.ru','dfghbuk564hbj')")
conn.commit()
CHECK constraint failed: CK_user_nickname

c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('a', '', 'kry1t@mail.ru','dfghbuk564hbj')")
conn.commit()
CHECK constraint failed: CK_user_name

c.execute("INSERT INTO user (nickname, name, mail, password) VALUES ('a', 'dhffkhghsrxffkhyhsxfthkfyfyhkyfkhfykfkyufkfkyhfykhyfkhyyfh', 'kry1t@mail.ru','dfghbuk564hbj')")
conn.commit()
CHECK constraint failed: CK_user_name
"""

print('\nUser')
c.execute('''Select * from user ''')
pp.pprint(c.fetchall())

print('\nContact')
c.execute('''Select * from contact ''')
ppp.pprint(c.fetchall())

print('\nChat_all_all')
c.execute('''Select * from chat_all_all ''')
pp.pprint(c.fetchall())

print('\nChat_all_for_one')
c.execute('''Select * from chat_all_for_one ''')
ppp.pprint(c.fetchall())

print('\nMessage_sskp')
c.execute('''Select * from message_sskp ''')
pp.pprint(c.fetchall())

print('\nChat')
c.execute('''Select * from chat ''')
ppp.pprint(c.fetchall())

#ch_all=[('kris sara julia', 19,3,0),('utopia', 5,6,1),('para',9,7,0 ),('povorot ne  tyda',14,9,0),('blog c++', 11, 8,1), ('lia anna', 4,2,0)] запросы на изменение имени 

#c.execute('''Select * from sqlite_master''')
#pp.pprint(c.fetchall())

conn.close()
