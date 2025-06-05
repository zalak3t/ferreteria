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
    imagen varchar(200) NOT NULL,
    precio VARCHAR2(50) NOT NULL,
    tipo VARCHAR2(100) NOT NULL
);


INSERT INTO usuarios VALUES(11111111,'Luis','lu@gmail.com','Luis231','cliente');
INSERT INTO usuarios VALUES(22222222,'Ana','an@gmail.com','Ana231','vendedor');
INSERT INTO usuarios VALUES(33333333,'Alan','al@gmail.com','Alan231','bodeguero');
INSERT INTO usuarios VALUES(44444444,'Benja','be@gmail.com','Benja231','contador');
INSERT INTO usuarios VALUES(55555555,'Juan','ju@gmail.com','Juan231','administrador');

INSERT INTO productos VALUES('ele-54321','Makita','MAK-98765','Amoladora Angular 7"','makita_amoladora','4500','eléctrica');
INSERT INTO productos VALUES('ele-66778','Makita','MAK-22334','Sierra Circular 1200W','makita_sierra.jpg','5200','eléctrica');

INSERT INTO productos VALUES('mat-11223','Sika','SIK-33445','Mortero de Reparación 25kg','sika_mortero.jpg','1500','material');
INSERT INTO productos VALUES('mat-22334','Sika','SIK-44556','Adhesivo para Cerámica 5kg','sika_adhesivo.jpg','1800','material');

INSERT INTO productos VALUES('aca-55667','Stanley','STA-77889','Lija al Agua #120','stanley_lija.jpg','800','acabado');
INSERT INTO productos VALUES('aca-66778','Stanley','STA-88990','Masilla para Madera','stanley_masilla.jpg','950','acabado');

INSERT INTO productos VALUES('seg-99001','Bosch','BOS-11223','Casco de Seguridad','bosch_casco.jpg','1200','seguridad');
INSERT INTO productos VALUES('seg-00112','Bosch','BOS-22334','Guantes de Seguridad','bosch_guantes.jpg','750','seguridad');

INSERT INTO productos VALUES('med-22334','Stanley','STA-44556','Cinta Métrica 8m','stanley_cinta.jpg','600','medición');
INSERT INTO productos VALUES('med-33445','Stanley','STA-55667','Nivel Laser','stanley_nivel.jpg','3200','medición');

INSERT INTO productos VALUES('man-55667','Stanley','STA-11223','Martillo Carpintero 16oz','stanley_martillo.jpg','1500','manual');
INSERT INTO productos VALUES('man-66778','Stanley','STA-22334','Destornillador Phillips #2','stanley_destornillador.jpg','800','manual');

COMMIT;

SELECT * FROM usuarios;
SELECT * FROM productos;