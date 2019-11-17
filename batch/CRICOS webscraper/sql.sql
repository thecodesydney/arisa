CREATE TABLE INSTITUTES (
	id INT NOT NULL AUTO_INCREMENT,
	cricos_prov_code VARCHAR(10) NOT NULL,
	trading_name VARCHAR(50),
	inst_name VARCHAR(50),
	inst_type VARCHAR(20),
	total_capacity INT,
	website VARCHAR(50),
	inst_post_address VARCHAR(200),
	page INT,
	update_date DATE NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE CONTACTS_PRINCIPAL (
	id INT NOT NULL AUTO_INCREMENT,
	inst_id INT NOT NULL,
	name VARCHAR(20),
	title VARCHAR(20),
	phone VARCHAR(20),
	fax VARCHAR(20),
	page INT,
	update_date DATE NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (inst_id) REFERENCES INSTITUTES(id)
);

CREATE TABLE CONTACTS_INT_STUDENT (
	id INT NOT NULL AUTO_INCREMENT,
	inst_id INT NOT NULL,
	name VARCHAR(20),
	title VARCHAR(20),
	phone VARCHAR(20),
	fax VARCHAR(20),
	email VARCHAR(30),
	page INT,
	update_date DATE NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (inst_id) REFERENCES INSTITUTES(id)
);

ALTER TABLE contact_int_student
    ADD CONSTRAINT inst_id_frgn
        FOREIGN KEY (inst_id)
        REFERENCES institute (id)
        ON DELETE CASCADE;

1.
show create table contact_int_student;

2.
Alter table contact_principal drop foreign key contact_principal_ibfk_1;
Alter table contact_int_student drop foreign key contact_int_student_ibfk_1;

3.
Alter table contact_int_student add foreign key (`inst_id`) REFERENCES `institute` (`id`) on DELETE CASCADE;
Alter table contact_principal add foreign key (`inst_id`) REFERENCES `institute` (`id`) on DELETE CASCADE;

INSERT INTO STATE (name)
VALUES ('Australian Capital Territory'),('New South Wales'),('Northern Territory'),('Queensland'),('South Australia'),('Tasmania'),('Victoria'),('Western Australia');
