import sqlite3
import pprint
conn = sqlite3.connect('messenger.sqlite')
c=conn.cursor()
pp = pprint.PrettyPrinter(indent=1, width=80, compact=False)
ppp = pprint.PrettyPrinter(indent=1, width=80, compact=True)
c.execute('''PRAGMA foreign_keys = 1''')

c.execute('''drop table if exists chat''')
c.execute('''drop table if exists message_sskp''')
c.execute('''drop table if exists chat_all_for_one''')
c.execute('''drop table if exists chat_all_all''')
c.execute('''drop table if exists contact''')
c.execute('''drop table if exists user''')
c.execute('''drop trigger if exists after_insert_chat_all_for_one''')
c.execute('''drop trigger if exists after_delete_chat_all_for_one''')
c.execute('''drop trigger if exists before_update_chat_all_all_name''')
c.execute('''drop trigger if exists after_insert_contact''')
c.execute('''drop trigger if exists before_delete_user''')

###

c.execute('''CREATE TABLE IF NOT EXISTS user(
    id_user integer not null,
    nickname varchar(30) not null,
    name varchar(40) not null,
    mail varchar(40) not null,
    password varchar(20) not null,
    CONSTRAINT PK_user_id_user primary key(id_user),
    CONSTRAINT UQ_user_nickname unique(nickname),
    CONSTRAINT UQ_user_mail unique(mail),
    CONSTRAINT CK_user_nickname check(length(nickname) > 0 and length(nickname) <= 30),
    CONSTRAINT CK_user_name check(length(name) > 0 and length(name) <= 40),
    CONSTRAINT CK_user_mail check(length(mail) > 0 and length(mail) <= 40 and (mail like '%@gmail.com' or mail like '%@mail.ru')),
    CONSTRAINT CK_user_password check(length(password) >= 8 and length(password) <= 20)
    )''')


c.execute('''CREATE TABLE IF NOT EXISTS contact(
    id_user integer not null,
    id_contact integer not null,
    CONSTRAINT PK_contact_id_user_id_contact primary key(id_user,id_contact),
    CONSTRAINT FK_contact_id_user foreign key(id_user) references user(id_user) on delete cascade on update cascade,
    CONSTRAINT FK_contact_id_contact foreign key(id_contact) references user(id_user) on delete cascade on update cascade,
    CONSTRAINT CK_contact_id_user_id_contact check(id_user != id_contact)
    )''')

c.execute('''CREATE TABLE IF NOT EXISTS chat_all_all(
    id_chat integer not null,
    creator integer,
    count_users int(6) not null CONSTRAINT DF_chat_all_all_count_users DEFAULT 1,
    name varchar(30) CONSTRAINT DF_chat_all_all_name DEFAULT NULL,
    change_name boolean not null CONSTRAINT DF_chat_all_all_change_name DEFAULT false,
    CONSTRAINT PK_chat_all_all_id_chat primary key(id_chat),
    CONSTRAINT FK_chat_all_all_creator foreign key(creator) references user(id_user) on delete set NULL on update cascade,
    CONSTRAINT CK_chat_all_all_name_count_users check(not(name != NULL and count_users = 2) and length(name) > 0 and length(name) <= 30)
    )''')

c.execute('''CREATE TABLE IF NOT EXISTS chat_all_for_one(
    id_ch_c integer not null,
    id_user_add integer not null,
    time_add text not null CONSTRAINT DF_chat_all_for_one_time_add DEFAULT current_date,
    CONSTRAINT PK_chat_all_for_one_id_ch_c_id_user_add primary key(id_ch_c, id_user_add),
    CONSTRAINT FK_chat_all_for_one_id_ch_c foreign key(id_ch_c) references chat_all_all(id_chat) on delete cascade on update cascade,
    CONSTRAINT FK_chat_all_for_one_id_user_add foreign key(id_user_add) references user(id_user) on delete cascade on update cascade
    )''')  

c.execute('''CREATE TABLE IF NOT EXISTS message_sskp(
    id_stroke integer not null,
    id_user integer,
    sms varchar(90) not null,
    type_sms varchar(10) not null,
    time text not null CONSTRAINT DF_message_sskp_time DEFAULT current_date,
    constraint PK_message_sskp_id_stroke primary key(id_stroke),
    constraint FK_message_sskp_id_user foreign key(id_user) references user(id_user) on delete set NULL on update cascade,
    CONSTRAINT UQ_message_sskp_id_user_time unique(id_user, time),
    CONSTRAINT CK_message_sskp_sms check(length(sms) > 0 and length(sms) < 90),
    CONSTRAINT CK_message_sskp_type_sms check(type_sms in ('text', 'img', 'video', 'audio', 'file', 'link', 'gif'))
    )''')

c.execute('''CREATE TABLE IF NOT EXISTS chat(
    id_person_chat integer not null,
    id_stroke integer not null,
    CONSTRAINT PK_chat_all_for_one_id_stroke primary key(id_stroke),
    CONSTRAINT FK_chat_all_all_id_stroke foreign key(id_stroke) references message_sskp(id_stroke) on delete cascade on update cascade,  
    CONSTRAINT FK_chat_all_all_id_person_chat foreign key(id_person_chat) references chat_all_all(id_chat) on delete cascade on update cascade   
    )''')

###

c.execute('''CREATE TRIGGER IF NOT EXISTS after_insert_chat_all_for_one
             after insert on chat_all_for_one
             for each row
             begin
                  update chat_all_all set count_users = count_users + 1 
                  where id_chat = NEW.id_ch_c;
                  update chat_all_all set name = substring(
                          (select (select name from user where id_user = creator) || ', ' ||
                              group_concat((select name from user where id_user = NEW.id_user_add), ', ')
                          from chat_all_for_one
                          where id_chat = NEW.id_ch_c),
                      1, 27) || '...'
                  where count_users > 2 and id_chat = NEW.id_ch_c and not change_name;
             end ''')

c.execute('''CREATE TRIGGER IF NOT EXISTS after_delete_chat_all_for_one
             after delete on chat_all_for_one
             for each row
             begin
                  update chat_all_all set count_users = count_users - 1 
                  where id_chat = OLD.id_ch_c;
                  update chat_all_all set name = substring(
                          (select (select name from user where id_user = creator) || ', ' ||
                              group_concat((select name from user where id_user = OLD.id_user_add), ', ')
                          from chat_all_for_one
                          where id_chat = OLD.id_ch_c),
                      1, 27) || '...'
                  where count_users > 2 and id_chat = OLD.id_ch_c and not change_name;
                  update chat_all_all set name = NULL
                  where count_users = 2;
             end ''')

"""
c.execute('''CREATE TRIGGER IF NOT EXISTS before_update_chat_all_all_name
             before update of name on chat_all_all
             begin
                  update chat_all_all set change_name = true
                  where name != OLD.name;
             end ''')
"""

c.execute('''CREATE TRIGGER IF NOT EXISTS after_insert_contact
             after insert on contact
             for each row
             begin
                  delete from contact
                  where (select true from contact as con
                         where contact.id_contact = con.id_user and
                               con.id_contact = contact.id_user and
                               contact.id_contact < contact.id_user);
             end ''')

c.execute('''CREATE TRIGGER IF NOT EXISTS before_delete_user
             after delete on user
             when OLD.id_user in (select creator from chat_all_all)
             begin
                  update chat_all_all set creator = (
                      select id_user_add from chat_all_for_one as cafo1
                      where time_add = (select min(time_add) from chat_all_for_one as cafo2
                                        where cafo1.id_ch_c = cafo2.id_ch_c))
                  where creator = NULL;
             end ''')

###

users=[ ('vikysia', 'Агарелышева Виктория', 'vikysia@gmail.com', 'qwertyuiop'),
        ('vlad', 'Агеев Владислав', 'vlad@gmail.com', 'asdfghjklz'),
        ('dinussiik', 'Ахметзянова Диана', 'dinussiik@gmail.com', 'xvbnmerqwt'),
        ('lia', 'Ахметова Лия', 'lia@gmail.com', 'yujiopasdf'),
        ('andrei', 'Бегашев Андрей', 'andrei@gmail.com', 'ghjklzxcvb'),
        ('sanek', 'Бекетов Александр', 'sanek@gmail.com', 'nmqwertyui'),
        ('timofei', 'Бирюков Тимофей', 'timofei@gmail.com', 'opasdfghjk'),
        ('maria', 'Ефремова Мария', 'maria@gmail.com', 'lzxcvbnmqw'),
        ('sergei', 'Зайцев Сергей', 'sergei@gmail.com', 'ertyuiopas'),
        ('michael', 'Инин Михаил', 'hellword@gmail.com', 'whyulookatthis'),
        ('anutka', 'Караваева Анна', 'anutka@gmail.com', 'vbnmqwerty'),
        ('yaroslav', 'Кораблев Ярослав', 'yaroslav@gmail.com', 'uiopasdfgh'),
        ('anatolik', 'Липин Анатолий', 'anatolik@gmail.com', 'jklzxvbnmz'),
        ('maxxx', 'Морев Максим', 'maxxx@gmail.com', 'fujrnwoksm'),
        ('annekra', 'Некрасова Анастасия', 'annekra@gmail.com', 'zuahekwbtp'),
        ('anna', 'Петрова Анна', 'anna@gmail.com', 'bjyexintzq'),
        ('semga', 'Сараев Семён', 'semga@gmail.com', 'anehdrbsek'),
        ('evgeni', 'Сенкевич Евгений', 'evgeni@gmail.com', 'iwbehsnxkf'),
        ('julia', 'Смекалова Юлия', 'julia@gmail.com', 'plebdhjtmw'),
        ('kris', 'Соколова Кристина', 'kris@gmail.com', 'zishebfomt'),
        ('sara', 'Сточинский Роман', 'sara@gmail.com', 'osbehtbzog'),
        ('svetlana', 'Халтурина Светлана', 'svetlana@gmail.com', 'wofbttosvb'),
        ('dana', 'Хасанова Дана', 'dana@gmail.com', 'boldnjxlds') ]

c.executemany("INSERT INTO user (nickname, name, mail, password) VALUES (?,?,?,?)", users)
conn.commit()


con = [ (1,2), (1,3), (1,5), (1,6), (1,8), (1,10), (1,12), (1,15), (1,18), (1,20), (1,21), (1,22),
        (2,1), (2,3), (2,4), (2,5), (2,7), (2,9), (2,13), (2,17), (2,18),
        (3,1), (3,2), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (3,13), (3,14), (3,15), (3,16), (3,17), (3,18), (3,19), (3,20), (3,21), (3,22), (3,23),
        (4,2), (4,3), (4,7), (4,8), (4,10), (4,15), (4,16), (4,17), (4,18), (4,19), (4,20), (4,21), (4,22), (4,23),
        (5,1), (5,2), (5,3), (5,6), (5,9), (5,10), (5,13), (5,14), (5,15), (5,17), (5,19), (5,20), (5,23),
        (6,1), (6,3), (6,5), (6,7), (6,9), (6,11), (6,12), (6,14), (6,17), (6,18), (6,21), (6,22), (6,23),
        (7,2), (7,3), (7,4), (7,6), (7,8), (7,11), (7,15), (7,16), (7,18), (7,19), (7,20),
        (8,1), (8,3), (8,4), (8,7), (8,9), (8,10), (8,12), (8,13), (8,14), (8,15), (8,16), (8,17), (8,18), (8,21), (8,22),
        (9,2), (9,3), (9,5), (9,6), (9,8), (9,11), (9,12), (9,13), (9,14), (9,16), (9,17), (9,18), (9,19), (9,20), (9,21), (9,22), (9,23),
        (10,1), (10,3), (10,4), (10,5), (10,8), (10,11), (10,12), (10,13), (10,15), (10,16), (10,17), (10,20), (10,22), (10,23),
        (11,3), (11,6), (11,7), (11,9), (11,10), (11,12), (11,14), (11,16), (11,17), (11,18), (11,21), (11,23),
        (12,1), (12,3), (12,6), (12,8), (12,9), (12,10), (12,13), (12,14), (12,15), (12,19), (12,20), (12,21), 
        (13,2), (13,3), (13,5), (13,8), (13,9), (13,10), (13,12), (13,22), (13,23), 
        (14,3), (14,5), (14,6), (14,8), (14,9), (14,11), (14,12), (14,15), (14,16), (14,17), (14,19), (14,20), (14,21), (14,22), (14,23),
        (15,1), (15,3), (15,4), (15,5), (15,7), (15,8), (15,10), (15,12), (15,14), (15,16), (15,18), (15,20), (15,22), (15,23),
        (16,3), (16,4), (16,7), (16,8), (16,9), (16,10), (16,11), (16,14), (16,15), (16,18), (16,20), (16,21), (16,23), 
        (17,2), (17,3), (17,4), (17,5), (17,6), (17,8), (17,9), (17,10), (17,11), (17,14), (17,23), 
        (18,1), (18,2), (18,3), (18,4), (18,6), (18,7), (18,8), (18,9), (18,11), (18,15), (18,16), (18,19), (18,20), (18,22), (18,23), 
        (19,3), (19,4), (19,5), (19,7), (19,9), (19,12), (19,14), (19,18), (19,20), (19,21), 
        (20,1), (20,3), (20,4), (20,5), (20,7), (20,9), (20,10), (20,12), (20,14), (20,15), (20,16), (20,18), (20,19), (20,22), 
        (21,1), (21,3), (21,4), (21,6), (21,8), (21,9), (21,11), (21,12), (21,14), (21,16), (21,19), (21,23), 
        (22,1), (22,3), (22,4), (22,6), (22,8), (22,9), (22,10), (22,13), (22,14), (22,15), (22,18), (22,20), (22,23), 
        (23,3), (23,4), (23,5), (23,6), (23,9), (23,10), (23,11), (23,13), (23,14), (23,15), (23,16), (23,17), (23,18), (23,21), (23,22)]

c.executemany("INSERT INTO contact(id_user, id_contact) VALUES (?,?)", con)
conn.commit()


c.execute("INSERT INTO chat_all_all(creator) VALUES (1), (3), (3), (3), (10), (13), (15), (15), (18), (20), (22), (23)")
conn.commit()


chat_for_one = [ ( 1, 5, '2024-04-21 16:45:21'), ( 2, 10, '2024-04-22 07:38:09'), ( 2, 15, '2024-04-22 14:13:12'),
                 ( 2, 20, '2024-04-23 15:55:25'), ( 2, 7, '2024-04-23 11:41:20'), ( 3, 8, '2024-04-23 12:35:00'),
                 ( 4, 1, '2024-04-25 09:21:41'), ( 4, 2, '2024-04-25 16:42:56'), ( 5, 19, '2024-04-26 09:09:09'),
                 ( 6, 22, '2024-04-27 19:46:21'), ( 7, 20, '2024-04-27 17:47:27'), ( 8, 6, '2024-04-28 23:23:23'),
                 ( 8, 7, '2024-04-29 20:40:20'), ( 8, 8, '2024-04-30 10:30:07'), ( 9, 19, '2024-05-02 18:53:53'),
                 ( 10, 4, '2024-05-03 00:03:32'), ( 11, 13, '2024-05-03 03:05:07'), ( 12, 14, '2024-05-03 17:38:04') ]

c.executemany("INSERT INTO chat_all_for_one(id_ch_c, id_user_add, time_add) VALUES (?,?,?)", chat_for_one)
conn.commit()


m_s = [ (1,'Стоит ли идти на пары в субботу?', 'text', '2024-05-04 15:45:20'),
        (14,'конечно нет', 'text', '2024-05-05 16:00:02'),
        (10,'vsephotoru1715979334.jpeg', 'img', '2024-05-16 19:15:10'),
        (11,'ахаахах', 'text', '2024-05-17 19:20:05'),
        (15,'c://users/downloads/photo.png', 'img', '2024-05-18 05:03:01') ]

c.executemany("INSERT INTO message_sskp(id_user, sms, type_sms, time) values (?,?,?,?)", m_s)
conn.commit()


chat_ps = [ (1,1), (1,2), (2,3), (2,4), (3,5) ]

c.executemany("INSERT INTO chat(id_person_chat, id_stroke) values (?,?)", chat_ps)
conn.commit()

#c.execute('''Select tbl_name, sql from sqlite_master  ''')
#pp.pprint(c.fetchall())

conn.close()
