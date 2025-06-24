import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="sunnybunny.123",
        database="gamingzone"
    )

-- games table
create table if not exists games (
    id int auto_increment primary key,
    name varchar(100),
    charge_per_hour decimal(5,2)
);

-- members table
create table if not exists members (
    id int auto_increment primary key,
    name varchar(100),
    membership_type enum('daily', 'monthly', 'yearly'),
    hours_spent int default 0,
    hours_left int
);

-- game_play table
create table if not exists game_play (
    id int auto_increment primary key,
    member_id int,
    game_id int,
    hours_played int,
    foreign key (member_id) references members(id),
    foreign key (game_id) references games(id)
);
