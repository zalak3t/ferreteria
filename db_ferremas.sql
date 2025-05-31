DROP TABLE usuarios;
DROP TABLE productos;

CREATE TABLE usuarios(
    rut NUMBER(8) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    pass VARCHAR2(50) NOT NULL,
    tipo VARCHAR2(50) NOT NULL
);

CREATE TABLE productos(
    codigo_producto VARCHAR2(9) PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    codigo VARCHAR(9) NOT NULL,
    nombre VARCHAR(100) NOT NULL, 
    imagen varchar(200) NOT NULL ,
    precio VARCHAR2(50) NOT NULL,
    tipo VARCHAR2(100) NOT NULL
);

INSERT INTO usuarios VALUES(11111111,'Luis','lu@gmail.com','Luis231','normal');
INSERT INTO usuarios VALUES(22222222,'Ana','an@gmail.com','Ana231','vendedor');
INSERT INTO usuarios VALUES(33333333,'Alan','al@gmail.com','Alan231','bodeguero');
INSERT INTO usuarios VALUES(44444444,'Benja','be@gmail.com','Benja231','contador');
INSERT INTO usuarios VALUES(55555555,'Juan','ju@gmail.com','Juan231','administrador');

INSERT INTO productos VALUES('fer-12345','Bosch','BOS-67890','taladro percutor bosch','a','$2000','manual');
commit;




select * from usuarios;
select * from productos;
