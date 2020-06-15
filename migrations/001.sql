CREATE TABLE users
(
  id SERIAL,
  username varchar(100),
  last_name varchar(100)
);

insert into users VALUES (DEFAULT, 'test', 'Roman');
insert into users VALUES (DEFAULT, 'test2', 'Ivan');
