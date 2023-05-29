CREATE TABLE authuser (
        id SERIAL NOT NULL,
        username VARCHAR NOT NULL,
        fullname VARCHAR,
        email VARCHAR,
        hashed_password VARCHAR NOT NULL,
        is_active BOOLEAN,
        is_superuser BOOLEAN,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        PRIMARY KEY (id),
        UNIQUE (username)
);
-- username: dummy, password: 123456
INSERT INTO authuser (username, hashed_password, is_active, is_superuser, created_at) VALUES ('dummy', '$2b$12$8FjGxyMgE6JlmEA8pf4AmuurQMm.BW.P1kRBnH.ExUtmY.WSOSqU2', TRUE, TRUE, NULL) RETURNING authuser.id;