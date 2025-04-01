DROP TABLE Movie CASCADE CONSTRAINTS;
DROP TABLE Director CASCADE CONSTRAINTS;
DROP TABLE Movie_Review CASCADE CONSTRAINTS;
DROP TABLE Directs_Movie CASCADE CONSTRAINTS;
DROP TABLE Directs_TV_Show CASCADE CONSTRAINTS;
DROP TABLE Movie_Genre CASCADE CONSTRAINTS;
DROP TABLE Movie_Awards CASCADE CONSTRAINTS;
DROP TABLE Movie_SServices CASCADE CONSTRAINTS;

DROP TABLE Writes_Movie CASCADE CONSTRAINTS;
DROP TABLE Writes_Show CASCADE CONSTRAINTS;
DROP TABLE Writer_Media CASCADE CONSTRAINTS;
DROP TABLE Writer CASCADE CONSTRAINTS;
DROP TABLE Acts_Movie CASCADE CONSTRAINTS;
DROP TABLE Acts_Show CASCADE CONSTRAINTS;
DROP TABLE Actor_Media CASCADE CONSTRAINTS;
DROP TABLE Actor CASCADE CONSTRAINTS;
DROP TABLE Show_Streaming_Services CASCADE CONSTRAINTS;
DROP TABLE Show_Media CASCADE CONSTRAINTS;
DROP TABLE Show_Genre CASCADE CONSTRAINTS;
DROP TABLE Show_Review CASCADE CONSTRAINTS;
DROP TABLE Show_Award CASCADE CONSTRAINTS;
DROP TABLE Tv_Show CASCADE CONSTRAINTS;


CREATE TABLE Movie(
MID			CHAR(15) 	CONSTRAINT Movie_MID_PK PRIMARY KEY,
Title			VARCHAR2(50),
Runtime			NUMBER(3),
Year_of_Release		NUMBER(4),
User_Rating		NUMBER(3,1));

CREATE TABLE Director(
DID			CHAR(15)	CONSTRAINT Director_MID_PK PRIMARY KEY,
FName			VARCHAR2(20),
MInit			CHAR(1),
LName			VARCHAR2(20),
Date_of_Birth		DATE,
Age			NUMBER(2),
Biography		VARCHAR2(3000));

CREATE TABLE Movie_Review(
MID			CHAR(15),
Reviewer		VARCHAR2(40),
Title			VARCHAR2(50),
Star			NUMBER(1),
Description		VARCHAR2(3000),
MRDate			DATE,
CONSTRAINT Movie_Review_pk PRIMARY KEY(Mid, Reviewer));


CREATE TABLE Directs_Movie(
MID			CHAR(15),
DID			CHAR(15),
CONSTRAINT Directs_Movie_mid_did_PK PRIMARY KEY(Mid, Did));

CREATE TABLE Directs_TV_Show(
TID			CHAR(15),
DID			CHAR(15),
CONSTRAINT Directs_TV_Show_tid_did_PK PRIMARY KEY(Tid, Did));

CREATE TABLE Movie_Genre(
MID			CHAR(15),
MGenre			VARCHAR2(50),
CONSTRAINT Movie_Genre_Mid_Mgenre_PK PRIMARY KEY(Mid, Mgenre));

CREATE TABLE Movie_Awards(
MID			CHAR(15),
MAwards			VARCHAR2(200),
CONSTRAINT Movie_Awards_Mid_Mawards_PK PRIMARY KEY(Mid, Mawards));

CREATE TABLE Movie_SServices(
MID			CHAR(15),
MSS			VARCHAR2(100),
CONSTRAINT Movie_SServices_Mid_Mss_PK PRIMARY KEY(Mid, Mss));

ALTER TABLE Movie_Review
ADD CONSTRAINT Movie_Review_mid_fk FOREIGN KEY(mid)
REFERENCES Movie(mid);

ALTER TABLE Movie_Genre
ADD CONSTRAINT movie_genre_mid_fk FOREIGN KEY(Mid)
REFERENCES Movie(Mid);

ALTER TABLE Movie_Awards
ADD CONSTRAINT movie_awards_mid_fk FOREIGN KEY(Mid)
REFERENCES Movie(Mid);

ALTER TABLE Movie_SServices
ADD CONSTRAINT movie_sservices_mid_fk FOREIGN KEY(Mid)
REFERENCES Movie(Mid);


CREATE TABLE Tv_Show
(
id CHAR(9) CONSTRAINT tv_show_id_pk PRIMARY KEY,
title VARCHAR2(30),
tv_show_rating NUMBER(2,1),
year_of_release CHAR(4)
);


CREATE TABLE Show_Award
(
tv_show_id CHAR(9),
Saward VARCHAR2(20),
CONSTRAINT show_award_tvid_saward_pk PRIMARY KEY(tv_show_id, Saward)
);

CREATE TABLE Show_Review
(
tv_show_id CHAR(9),
reviewing_user_id CHAR(9),
description VARCHAR2(500),
star_rating CHAR(1),
date_of_review DATE,
CONSTRAINT show_review_tvid_reviwer_id_pk PRIMARY KEY(tv_show_id,reviewing_user_id)
);

CREATE TABLE Show_Genre
(
tv_show_id CHAR(9),
genre VARCHAR2(20),
CONSTRAINT show_genre_tvid_genre_pk PRIMARY KEY(tv_show_id, genre)
);

CREATE TABLE Show_Media
(
tv_show_id CHAR(9),
media VARCHAR2(20),
CONSTRAINT show_media_tvid_media_pk PRIMARY KEY(media, tv_show_id)
);

CREATE TABLE Show_Streaming_Services
(
tv_show_id CHAR(9),
streaming_service VARCHAR2(20),
CONSTRAINT showSS_media_tvid_pk PRIMARY KEY(streaming_service, tv_show_id)
);

CREATE TABLE Actor
(
actor_id CHAR(9) CONSTRAINT actor_actor_id_pk PRIMARY KEY,
f_name VARCHAR2(25),
m_initial CHAR(1),
l_name VARCHAR2(25),
biography VARCHAR2(500),
dob DATE,
age NUMBER(3)
);

CREATE TABLE Actor_Media
(
actor_id CHAR(9),
media VARCHAR2(20),
CONSTRAINT actor_media_tvid_media_pk PRIMARY KEY(media, actor_id)
);

CREATE TABLE Acts_Show
(
actor_id CHAR(9),
tv_show_id CHAR(9),
CONSTRAINT acts_show_actorid_tvid_pk PRIMARY KEY(actor_id, tv_show_id)
);

CREATE TABLE Acts_Movie
(
actor_id CHAR(9),
movie_id CHAR(9),
CONSTRAINT acts_movie_actorid_movieid_pk PRIMARY KEY(actor_id, movie_id)
);

CREATE TABLE Writer
(
writer_id CHAR(9) CONSTRAINT writer_writer_id PRIMARY KEY,
f_name VARCHAR2(25),
m_initial CHAR(1),
l_name VARCHAR2(25),
biography VARCHAR2(500),
dob DATE,
age NUMBER(3)
);

CREATE TABLE Writer_Media
(
writer_id CHAR(9),
media VARCHAR2(20),
CONSTRAINT writer_media_tvid_media_pk PRIMARY KEY(media, writer_id)
);




CREATE TABLE Writes_Show
(
writer_id CHAR(9),
tv_show_id CHAR(9),
CONSTRAINT writes_show_writerid_tvid_pk PRIMARY KEY(writer_id, tv_show_id)
);

CREATE TABLE Writes_Movie
(
writer_id CHAR(9),
movie_id CHAR(9),
CONSTRAINT writes_movie_wid_mid_pk PRIMARY KEY(writer_id, movie_id)
);


ALTER TABLE Show_Award
ADD CONSTRAINT ShowA_tv_showid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_Show(id);
ALTER TABLE Show_Review
ADD CONSTRAINT ShowR_tv_showid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_Show(id);
ALTER TABLE Show_Genre
ADD CONSTRAINT ShowG_tv_showid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_Show(id);
ALTER TABLE Show_Media
ADD CONSTRAINT ShowM_tv_showid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_Show(id);
ALTER TABLE Show_Streaming_Services
ADD CONSTRAINT ShowSS_tv_showid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_Show(id);

ALTER TABLE Actor_media 
ADD CONSTRAINT actorMedia_actorid_fk FOREIGN KEY(actor_id)
REFERENCES Actor(actor_id);
ALTER TABLE Acts_show
ADD CONSTRAINT actorShow_tvid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_Show(id);
ALTER TABLE Acts_show
ADD CONSTRAINT actorShow_actorid_fk FOREIGN KEY(actor_id)
REFERENCES Actor(actor_id);
ALTER TABLE Acts_movie
ADD CONSTRAINT actorMovie_actorid_fk FOREIGN KEY(actor_id)
REFERENCES Actor(actor_id);
ALTER TABLE Acts_movie
ADD CONSTRAINT actorMovie_movieid_fk FOREIGN KEY(movie_id)
REFERENCES movie(MID);

ALTER TABLE Writer_Media
ADD CONSTRAINT Writer_media_writerid_fk FOREIGN KEY(writer_id)
REFERENCES Writer(writer_id);
ALTER TABLE Writes_Show
ADD CONSTRAINT Writes_show_writerid_fk FOREIGN KEY(writer_id)
REFERENCES Writer(writer_id);
ALTER TABLE Writes_Show
ADD CONSTRAINT Writes_show_tvid_fk FOREIGN KEY(tv_show_id)
REFERENCES Tv_show(id);
ALTER TABLE Writes_Movie
ADD CONSTRAINT Writes_movie_writerid_fk FOREIGN KEY(writer_id)
REFERENCES Writer(writer_id);
ALTER TABLE Writes_Movie
ADD CONSTRAINT Writes_movie_movieid_fk FOREIGN KEY(movie_id)
REFERENCES movie(MID);




DESC Movie;
DESC Director;
DESC Movie_Review;
DESC Directs_Movie;
DESC Directs_TV_Show;
DESC Movie_Genre;
DESC Movie_Awards;
DESC Movie_SServices;












DESC Writes_Movie;
DESC Writes_Show;
DESC Writer_Media;
DESC Writer;
DESC Acts_Movie;
DESC Acts_Show;
DESC Actor_Media;
DESC Actor;
DESC Show_Streaming_Services;
DESC Show_Media;
DESC Show_Genre;
DESC Show_Review;
DESC Show_Award;
DESC Tv_Show;
















































