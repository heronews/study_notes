CREATE TABLE user(
    id INTEGER PRIMARY KEY NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    enable INTEGER NOT NULL
);

CREATE TABLE user_role(
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL
);

CREATE TABLE role(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE role_permission(
    id INTEGER PRIMARY KEY NOT NULL,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL
);

CREATE TABLE permission(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE user_session(
    id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    expire_time TEXT NOT NULL
);

INSERT INTO permission (id, name) VALUES(1, 'user:insert');
INSERT INTO permission (id, name) VALUES(2, 'user:delete');
INSERT INTO permission (id, name) VALUES(3, 'user:update');
INSERT INTO permission (id, name) VALUES(4, 'user:select');

INSERT INTO role (id, name) VALUES(1, '管理员');

INSERT INTO role_permission (role_id, permission_id) VALUES(1, 1);
INSERT INTO role_permission (role_id, permission_id) VALUES(1, 2);
INSERT INTO role_permission (role_id, permission_id) VALUES(1, 3);
INSERT INTO role_permission (role_id, permission_id) VALUES(1, 4);

INSERT INTO user (id, username, password, enable)
VALUES(1, 'admin', '$argon2id$v=19$m=65536,t=3,p=4$qfWekzKGcI6x9h4jRKhV6g$s9073NrcUgyxwf/Kz+0iu98FDTq6D+Vlk2L6uxUMHF0', 1);

INSERT INTO user_role (user_id, role_id) VALUES(1, 1);