-- Tabla estados

create table estados(
id_estado int not null primary key identity(1,1),
estado_nombre varchar(255)
)

insert into estados values ('Jalisco')
insert into estados values ('Colima')
insert into estados values ('Nayarit')

select * from estados

drop table estados