alter table document ADD
keywords varchar(10000),
case_type varchar(200),
case_num varchar(200),
public_prosecution varchar(200);

/*
  mysql dump
 */
mysqldump -u root -p --routines --default-character-set=utf8 --databases judgment > judgment_with_abstract.sql