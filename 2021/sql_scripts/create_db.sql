Create database production;
use production;

CREATE TABLE Заказ
(
	номер_заказа         INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	описание_заказа      VARCHAR(200) NULL,
	id_организации_заказчика INTEGER NULL
);



CREATE TABLE Заказ_Конечный_продукт
(
	номер_заказа         INTEGER NOT NULL,
	id_продукта          INTEGER NOT NULL,
	количество           INTEGER NULL,
	CHECK (количество>=0)
);



ALTER TABLE Заказ_Конечный_продукт
ADD PRIMARY KEY (номер_заказа,id_продукта);



CREATE TABLE Заказ_Материал
(
	номер_заказа         INTEGER NOT NULL,
	id_материала         INTEGER NOT NULL,
	количество           INTEGER NULL,
	CHECK (количество>=0)
);



ALTER TABLE Заказ_Материал
ADD PRIMARY KEY (номер_заказа,id_материала);



CREATE TABLE Конечный_продукт
(
	id_продукта          INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	наименование_продукта VARCHAR(120) NOT NULL
);



CREATE TABLE Материал
(
	id_материала         INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	наименование_материала VARCHAR(120) NOT NULL,
	количество           INTEGER NULL,
	CHECK (количество>=0)
);



CREATE TABLE Оборудование
(
	id_оборудования      INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	название             VARCHAR(120) NOT NULL,
	id_типа              INTEGER NULL
);



CREATE TABLE Организация_заказчик
(
	id_организации_заказчика INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	наименование_организации_заказчика VARCHAR(200) NULL,
	контактная_информация VARCHAR(200) NULL
);



CREATE TABLE Организация_продавец
(
	id_организации_продавца INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	наименование_организации_продавца VARCHAR(200) NULL,
	контактная_информация VARCHAR(200) NULL
);



CREATE TABLE Производство
(
	id_производства          INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_продукта      INTEGER NOT NULL,
	название_производства VARCHAR(120) NULL
);



CREATE TABLE Производство_Оборудование
(
	id_производства      INTEGER NOT NULL,
	id_оборудования      INTEGER NOT NULL,
	количество           INTEGER NULL,
	CHECK (количество>=0)
);



ALTER TABLE Производство_Оборудование
ADD PRIMARY KEY (id_производства,id_оборудования);



CREATE TABLE Рецептура
(
	id_материала         INTEGER NOT NULL,
	id_производства      INTEGER NOT NULL,
	количество           INTEGER NULL,
	CHECK (количество>=0)
);



ALTER TABLE Рецептура
ADD PRIMARY KEY (id_материала,id_производства);



CREATE TABLE Тип_оборудования
(
	id_типа              INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY,
	наименование_типа    VARCHAR(200) NULL
);



CREATE TABLE Цена_материала
(
	id_материала         INTEGER NOT NULL,
	цена                 INTEGER NULL,
	id_организации_продавца INTEGER NOT NULL,
	CHECK (цена>0)
);



ALTER TABLE Цена_материала
ADD PRIMARY KEY (id_материала,id_организации_продавца);



ALTER TABLE Заказ
ADD FOREIGN KEY R_15 (id_организации_заказчика) REFERENCES Организация_заказчик (id_организации_заказчика);



ALTER TABLE Заказ_Конечный_продукт
ADD FOREIGN KEY R_6 (номер_заказа) REFERENCES Заказ (номер_заказа);



ALTER TABLE Заказ_Конечный_продукт
ADD FOREIGN KEY R_26 (id_продукта) REFERENCES Конечный_продукт (id_продукта);



ALTER TABLE Заказ_Материал
ADD FOREIGN KEY R_7 (номер_заказа) REFERENCES Заказ (номер_заказа);



ALTER TABLE Заказ_Материал
ADD FOREIGN KEY R_28 (id_материала) REFERENCES Материал (id_материала);



ALTER TABLE Оборудование
ADD FOREIGN KEY R_29 (id_типа) REFERENCES Тип_оборудования (id_типа);



ALTER TABLE Производство
ADD FOREIGN KEY R_13 (id_продукта) REFERENCES Конечный_продукт (id_продукта);



ALTER TABLE Производство_Оборудование
ADD FOREIGN KEY R_22 (id_производства) REFERENCES Производство (id_производства);



ALTER TABLE Производство_Оборудование
ADD FOREIGN KEY R_24 (id_оборудования) REFERENCES Оборудование (id_оборудования);



ALTER TABLE Рецептура
ADD FOREIGN KEY R_16 (id_материала) REFERENCES Материал (id_материала);



ALTER TABLE Рецептура
ADD FOREIGN KEY R_20 (id_производства) REFERENCES Производство (id_производства);



ALTER TABLE Цена_материала
ADD FOREIGN KEY R_18 (id_материала) REFERENCES Материал (id_материала);



ALTER TABLE Цена_материала
ADD FOREIGN KEY R_3 (id_организации_продавца) REFERENCES Организация_продавец (id_организации_продавца);


