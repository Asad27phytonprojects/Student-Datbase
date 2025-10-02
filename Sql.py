# create database studens_record

# use studens_record


# create table Users_Table(
#  user_id int primary key auto_increment,
#  username varchar(100) not null unique,
#  Passwor varchar(255) not null ,
#  rol Enum('admin','student') not null ,
#  is_active boolean default true
#  );
 
#  create table students_Table(
#   students_id int primary key auto_increment,
#   user_id int not null,
#   foreign key(user_id) references Users_Table(user_id),
#   Namee varchar(150) not null ,
#   email varchar(160) unique,
#   enrolled boolean default false,
#   created_at timestamp default current_timestamp);
  
#   create table Payments_Table(
#    payments_id int primary key auto_increment,
#    students_id int ,
#    foreign key (students_id) references  students_Table(students_id),
#    amount decimal(10.2) not null ,
#    payment_date date not null ,
#    order_status enum('paid','unpaid') not null )  