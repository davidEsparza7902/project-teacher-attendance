DROP DATABASE IF EXISTS BD_ASISTENCIA_ADMINISTRATIVA_UNT;
CREATE DATABASE BD_ASISTENCIA_ADMINISTRATIVA_UNT;
USE BD_ASISTENCIA_ADMINISTRATIVA_UNT;
CREATE TABLE ADMINISTRATIVO(
	DNI		CHAR(8) PRIMARY KEY NOT NULL,
	NOMBRE	VARCHAR(60) NOT NULL,
    APELLIDO_PATERNO VARCHAR(60) NOT NULL,
    APELLIDO_MATERNO VARCHAR(60) NOT NULL,
	AREA VARCHAR(120) NOT NULL,
	CONTRASENIA	VARCHAR(30) NOT NULL,
	CORREO  VARCHAR(50) NOT NULL,
    FOTO LONGBLOB
);

CREATE TABLE ASISTENCIA (
    ID INTEGER PRIMARY KEY auto_increment,
    DNI_ADMINISTRATIVO CHAR(8) NOT NULL,
    FECHA DATE NOT NULL,
    HORA_ENTRADA TIME,
    HORA_SALIDA TIME,
    TIPO_ASISTENCIA VARCHAR(20),
    FOREIGN KEY (DNI_ADMINISTRATIVO) REFERENCES ADMINISTRATIVO(DNI)
);