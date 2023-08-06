#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql.cursors
import os

# Возвращает строку типа DATE для SQL
def get_date_type(date):
    return str(date['byear']) + '-' + str(date['bmonth']) + '-' + str(date['bday'])


# Информация из config
def get_con_info():
    p = os.path.abspath('')
    info = []
    p = p[:p.rfind('/')] + '/config.env'
    file = open(p)
    for line in file:
        if line.find('username=') != -1 or line.find('password=') != -1 or line.find('base_name=') != -1 or line.find('temporary_table=') != -1 or line.find('permanent_table=') != -1:
            info.append(line[line.find('"')+1:line.rfind('"')])
    return info


# Сохранение + миграция + комит
def mySQL_save(people):
    info = get_con_info()
    con = pymysql.connect(
        host='localhost',
        user=info[0],
        password=info[1],
        db=info[2],
    )
    with con:
        cursor = con.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS `{info[3]}`;")
        cursor.execute(f"CREATE TABLE `{info[3]}` (`last_name` varchar(50) NOT NULL, `first_name` varchar(50) NOT NULL, `middle_name` varchar(50) NOT NULL, `birth_date` date NOT NULL, `position_id` int unsigned NOT NULL, `image_url` varchar(255) DEFAULT NULL, `url` varchar(255) NOT NULL, PRIMARY KEY (`last_name`,`first_name`,`middle_name`,`birth_date`,`position_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;")
        for person in people:
            sql = f"INSERT IGNORE INTO `{info[3]}` (`last_name`, `first_name`, `middle_name`, `birth_date`, `position_id`, `image_url`, `url`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (person['last_name'][0].upper() + person['last_name'][1:],
                                 person['first_name'][0].upper() + person['first_name'][1:],
                                 person['middle_name'][0].upper() + person['middle_name'][1:],
                                 get_date_type({'bday': person['bday'], 'bmonth': person['bmonth'], 'byear': person['byear']}),
                                 person['position_id'],
                                 person['image_link'],
                                 person['link']
                                 )
                           )
        cursor.execute(f"DELETE LOW_PRIORITY FROM `{info[4]}`;")
        cursor.execute(f"INSERT INTO {info[2]}.{info[4]} SELECT * FROM {info[2]}.{info[3]};")
        cursor.execute(f"DROP TABLE IF EXISTS `{info[3]}`;")
    con.commit()
