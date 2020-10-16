-- Author: Emanuel Camarena
-- Modified on: 16/10/20

-- CREATE TABLES
-- CREATE TABLE ESTADOS - COMPLETED (16/10/20)
create table estados(
id_estado int not null primary key identity(1,1),
estado_id varchar(5) not null,
estado_nombre varchar(255) not null
)

-- CREATE TABLE MUNICIPIOS - COMPLETED (16/10/20)
create table municipios(
id_municipios int not null primary key identity(1,1),
municipios_id varchar(1) not null,
id_estado int not null foreign key references estados(id_estado),
municipio_nombre varchar(255) not null
)

-- CREATE TABLE PELICULAS - COMPLETED (16/10/20)
create table peliculas (
id_peliculas int not null primary key identity(1,1),
peliculas_nombre varchar(255) not null,
peliculas_minutos int not null
)

--INSERT INFORMATION
-- INSERT ESTADOS - COMPLETED (16/10/20)
insert into estados values ('J11','Jalisco')
insert into estados values ('N11','Nuevo León')
insert into estados values ('E11','Estado de México')
insert into estados values ('C11','Chihuahua')
insert into estados values ('S11','Sinaloa')


-- INSERT MUNICIPIOS - COMPLETED (16/10/20) 
-- JALISCO - COMPLETED
insert into municipios values ('A','1','Guadalajara')
insert into municipios values ('B','1','Zapopan')
insert into municipios values ('C','1','Tlaquepaque')
insert into municipios values ('D','1','Tonalá')
insert into municipios values ('E','1','Zapotlanejo')
insert into municipios values ('F','1','Tlajomulco')
insert into municipios values ('G','1','Ayotlán')
insert into municipios values ('H','1','Tequila')
insert into municipios values ('I','1','Ocotlán')
insert into municipios values ('J','1','Puerto Vallarta')

-- NUEVO LEÓN - COMPLETED
insert into municipios values ('A','2','Guadalupe')
insert into municipios values ('B','2','Abasolo')
insert into municipios values ('C','2','Apodaca')
insert into municipios values ('D','2','Ciénega de Flores')
insert into municipios values ('E','2','General Zaragoza')
insert into municipios values ('F','2','Iturbide')
insert into municipios values ('G','2','Juárez')
insert into municipios values ('H','2','Monterrey')
insert into municipios values ('I','2','Salinas Victoria')
insert into municipios values ('J','2','General Zuazua')

-- ESTADO DE MÉXICO - COMPLETED
insert into municipios values ('A','3','Cuautitlán Izcalli')
insert into municipios values ('B','3','Chalco')
insert into municipios values ('C','3','Aculco')
insert into municipios values ('D','3','Atizapán')
insert into municipios values ('E','3','Chapultepec')
insert into municipios values ('F','3','Ecatepec de Morelos')
insert into municipios values ('G','3','Naucalpan de Juárez')
insert into municipios values ('H','3','Morelos')
insert into municipios values ('I','3','Texcoco')
insert into municipios values ('J','3','Toluca')

-- CHIHUAHUA - COMPLETED
insert into municipios values ('A','4','Ignacio Zaragoza')
insert into municipios values ('B','4','Allende')
insert into municipios values ('C','4','Valle de Zaragoza')
insert into municipios values ('D','4','Rosario')
insert into municipios values ('E','4','Nonoava')
insert into municipios values ('F','4','Matamoros')
insert into municipios values ('G','4','Guadalupe y Calco')
insert into municipios values ('H','4','Coronado')
insert into municipios values ('I','4','Delicias')
insert into municipios values ('J','4','Galeana')

-- SINALOA - COMPLETED
insert into municipios values ('A','5','Guasave')
insert into municipios values ('B','5','Navolato')
insert into municipios values ('C','5','Cosalá')
insert into municipios values ('D','5','Angostura')
insert into municipios values ('E','5','Mocorito')


-- INSERT PELICULAS
insert into peliculas values ('Mulan',120)
insert into peliculas values ('The pick of Destiny',140)
insert into peliculas values ('The Lion King',130)
insert into peliculas values ('Toy Story 4',120)
insert into peliculas values ('Cars 3',100)

-- SELECT - FOR TESTING
select * from estados
select * from municipios

-- DROP TABLES  -- DROP ONLY IF NEEDED
drop table estados
drop table municipios