import json
import os
from datetime import datetime
from time import sleep

import lxml
import oracledb
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from random_user_agent.params import OperatingSystem, SoftwareName
from random_user_agent.user_agent import UserAgent

load_dotenv()

software_names = [SoftwareName.CHROME.value]
operating_systems = [
    OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value
]

user_agent_rotator = UserAgent(software_names=software_names,
                               operating_systems=operating_systems,
                               limit=100)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()

# Get Random User Agent String.

api_key = os.getenv("API_KEY")
main_api_url = f"https://www.omdbapi.com/?apikey={api_key}"
imdb_url = "https://imdb.com"
reviews_url = "/title/{}/reviews/?ref_=tt_ov_ururv"
media_data_url = "&i={}"
api_parameters = "&s={}&type={}"


def get_movie_review(movie_id):
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {"User-Agent": user_agent}
    review_response = requests.get(imdb_url + reviews_url.format(movie_id),
                                   headers=headers)
    if review_response.status_code == 200:
        soup = BeautifulSoup(review_response.text, "lxml")
        first_review_container = soup.find(
            "div",
            class_=
            "ipc-list-card--border-speech ipc-list-card--hasActions ipc-list-card--base ipc-list-card sc-3e6f8aa9-0 lbshKr",
        )
        review_title = first_review_container.find(
            "div",
            class_=
            "ipc-title ipc-title--base ipc-title--title ipc-title--on-textPrimary sc-3e6f8aa9-7 kyozWI",
        ).text
        review_content = soup.find("div",
                                   class_="ipc-html-content-inner-div").text
        # print(review_title.text)
        # print(imdb_url + reviews_url.format(movie_id))
        # print(review_content.text)
        bottom_info = soup.find(
            "ul",
            class_=
            "ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline base",
        )
        lis = bottom_info.find_all("li")

        user = lis[0].text
        review_date = datetime.strptime(lis[1].text, "%b %d, %Y")
        user_rating = int(
            soup.find("span", class_="ipc-rating-star--rating").text)
        return user, review_title, user_rating, review_content[:
                                                               2999], review_date
    else:
        print("Error getting review:", review_response.status_code)
        return None, None, None, None, None


def calculate_age(date_object):
    today = datetime.today()
    age = today.year - date_object.year

    # adjust if birthday hasn't occurred yet this year
    if (today.month, today.day) < (date_object.month, date_object.day):
        age -= 1

    return age


def get_movie_ids():
    movie_titles = [
        "The Shawshank Redemption",
        "The Godfather",
        "The Dark Knight",
        "The Godfather: Part II",
        "The Lord of the Rings: The Return of the King",
        "Pulp Fiction",
        "Forrest Gump",
        "The Empire Strikes Back",
        "The Matrix",
        "Fight Club",
        "Inception",
        "Goodfellas",
        "The Lord of the Rings: The Fellowship of the Ring",
        "Star Wars: A New Hope",
        "The Silence of the Lambs",
        "Se7en",
        "The Usual Suspects",
        "The Lion King",
        "Schindler's List",
        "Interstellar",
        "City of God",
        "Back to the Future",
        "Gladiator",
        "The Dark Knight Rises",
        "The Departed",
        "Whiplash",
        "The Prestige",
        "The Green Mile",
        "12 Angry Men",
        "Casablanca",
        "The Intouchables",
        "The Pianist",
        "The Terminator",
        "One Flew Over the Cuckoo's Nest",
        "The Good, the Bad and the Ugly",
        "The Shining",
        "Citizen Kane",
        "The Social Network",
        "The Revenant",
        "A Clockwork Orange",
        "Django Unchained",
        "The Great Dictator",
        "American History X",
        "Saving Private Ryan",
        "Braveheart",
        "The Hunt",
        "Requiem for a Dream",
        "The Big Lebowski",
        "The Wizard of Oz",
        "It's a Wonderful Life",
    ]
    movie_titles_ids = []
    for movie in movie_titles:
        response = requests.get(main_api_url +
                                api_parameters.format(movie, "movie"))
        try:
            to_dict = json.loads(response.text)
            movie_id = to_dict.get("Search")[0].get("imdbID")
            movie_titles_ids.append(movie_id)
        except Exception as e:
            print("Something went wrong: ", str(e))

    if len(movie_titles_ids) == len(movie_titles):
        final_dict = dict(zip(movie_titles_ids, movie_titles))
        return final_dict
    else:
        return None


def is_already_created(cursor, object_id, object_type):
    if object_type == "director":
        cursor.execute(
            """
            SELECT 1 FROM Director WHERE DID = :director_id
            """,
            {"director_id": object_id},
        )
        return cursor.fetchone() is not None
    elif object_type == "actor":
        cursor.execute(
            """
            SELECT 1 FROM Actor WHERE actor_id = :actor_id
            """,
            {"actor_id": object_id},
        )
        return cursor.fetchone() is not None
    elif object_type == "writer":
        cursor.execute(
            """
            SELECT 1 FROM Writer WHERE writer_id = :writer_id
            """,
            {"writer_id": object_id},
        )
        return cursor.fetchone() is not None


def get_tv_ids():
    tv_show_titles = [
        "Breaking Bad",
        "Game of Thrones",
        "The Wire",
        "Stranger Things",
        "The Sopranos",
        "Friends",
        "The Office",
        "Sherlock",
        "The Crown",
        "Black Mirror",
        "Westworld",
        "The Mandalorian",
        "Chernobyl",
        "The Boys",
        "Fargo",
        "True Detective",
        "The Witcher",
        "Money Heist",
        "Narcos",
        "Better Call Saul",
        "The Simpsons",
        "The Walking Dead",
        "Rick and Morty",
        "Vikings",
        "House of Cards",
        "Peaky Blinders",
        "The Queen's Gambit",
        "Dexter",
        "Big Bang Theory",
        "BoJack Horseman",
        "Dark",
        "Insatiable",
        "How I Met Your Mother",
        "Prison Break",
        "Brooklyn Nine-Nine",
        "Friends",
        "Supernatural",
        "The X-Files",
        "Arrow",
        "The Flash",
        "Lucifer",
        "Doctor Who",
        "Fleabag",
        "Hannibal",
        "Grey's Anatomy",
        "The Haunting of Hill House",
        "Narcos: Mexico",
        "The Marvelous Mrs. Maisel",
        "The Umbrella Academy",
        "Ozark",
        "Mindhunter",
    ]
    tv_show_titles_ids = []
    for tv_show in tv_show_titles:
        response = requests.get(main_api_url +
                                api_parameters.format(tv_show, "series"))
        try:
            to_dict = json.loads(response.text)
            tv_id = to_dict.get("Search")[0].get("imdbID")
            tv_show_titles_ids.append(tv_id)
        except Exception as e:
            print("Something went wrong: ", str(e))

    if len(tv_show_titles_ids) == len(tv_show_titles):
        final_dict = dict(zip(tv_show_titles_ids, tv_show_titles))
        return final_dict
    else:
        return None


movie_ids_json = {
    "tt0111161": "The Shawshank Redemption",
    "tt0068646": "The Godfather",
    "tt0468569": "The Dark Knight",
    "tt0071562": "The Godfather: Part II",
    "tt0167260": "The Lord of the Rings: The Returnof the King",
    "tt0110912": "Pulp Fiction",
    "tt0109830": "Forrest Gump",
    "tt0080684": "The Empire Strikes Back",
    "tt0133093": "The Matrix",
    "tt0137523": "Fight Club",
    "tt1375666": "Inception",
    "tt0099685": "Goodfellas",
    "tt0120737": "The Lord of the Rings: The Fellowship of the Ring",
    "tt0076759": "Star Wars: A New Hope",
    "tt0102926": "The Silence of the Lambs",
    "tt0114369": "Se7en",
    "tt0114814": "The Usual Suspects",
    "tt0110357": "The Lion King",
    "tt0108052": "Schindler's List",
    "tt0816692": "Interstellar",
    "tt0317248": "City of God",
    "tt0088763": "Back to the Future",
    "tt0172495": "Gladiator",
    "tt1345836": "The Dark Knight Rises",
    "tt0407887": "The Departed",
    "tt2582802": "Whiplash",
    "tt0482571": "The Prestige",
    "tt0120689": "The Green Mile",
    "tt0050083": "12 Angry Men",
    "tt0034583": "Casablanca",
    "tt1675434": "The Intouchables",
    "tt0253474": "The Pianist",
    "tt0088247": "The Terminator",
    "tt0073486": "One Flew Over the Cuckoo's Nest",
    "tt0060196": "The Good, the Bad and the Ugly",
    "tt0081505": "The Shining",
    "tt0033467": "Citizen Kane",
    "tt1285016": "The Social Network",
    "tt1663202": "The Revenant",
    "tt0066921": "A Clockwork Orange",
    "tt1853728": "Django Unchained",
    "tt0032553": "The Great Dictator",
    "tt0120586": "American History X",
    "tt0120815": "Saving Private Ryan",
    "tt0112573": "Braveheart",
    "tt2106476": "The Hunt",
    "tt0180093": "Requiem for a Dream",
    "tt0118715": "The Big Lebowski",
    "tt0032138": "The Wizard of Oz",
    "tt0038650": "It's a Wonderful Life",
}
tv_show_ids_json = {
    "tt0903747": "Breaking Bad",
    "tt0944947": "Game of Thrones",
    "tt0306414": "The Wire",
    "tt4574334": "Stranger Things",
    "tt0141842": "The Sopranos",
    "tt0108778": "Friends",
    "tt0386676": "TheOffice",
    "tt1475582": "Sherlock",
    "tt4786824": "The Crown",
    "tt2085059": "Black Mirror",
    "tt0475784": "Westworld",
    "tt8111088": "The Mandalorian",
    "tt7366338": "Chernobyl",
    "tt1190634": "TheBoys",
    "tt2802850": "Fargo",
    "tt2356777": "True Detective",
    "tt5180504": "The Witcher",
    "tt6468322": "Money Heist",
    "tt2707408": "Narcos",
    "tt3032476": "Better Call Saul",
    "tt0096697": "TheSimpsons",
    "tt1520211": "The Walking Dead",
    "tt2861424": "Rick and Morty",
    "tt2306299": "Vikings",
    "tt1856010": "House of Cards",
    "tt2442560": "Peaky Blinders",
    "tt10048342": "The Queen's Gambit",
    "tt0773262": "Dexter",
    "tt0898266": "Big Bang Theory",
    "tt3398228": "BoJack Horseman",
    "tt5753856": "Dark",
    "tt6487482": "Insatiable",
    "tt0460649": "How I Met Your Mother",
    "tt0455275": "Prison Break",
    "tt2467372": "Brooklyn Nine-Nine",
    "tt0460681": "Supernatural",
    "tt0106179": "The X-Files",
    "tt2193021": "Arrow",
    "tt3107288": "The Flash",
    "tt4052886": "Lucifer",
    "tt0436992": "Doctor Who",
    "tt5687612": "Fleabag",
    "tt2243973": "Hannibal",
    "tt0413573": "Grey's Anatomy",
    "tt6763664": "The Haunting of Hill House",
    "tt8714904": "Narcos: Mexico",
    "tt5788792": "The Marvelous Mrs. Maisel",
    "tt1312171": "The Umbrella Academy",
    "tt5071412": "Ozark",
    "tt5290382": "Mindhunter",
}

search_url = "https://www.imdb.com/find/?q={}"


def get_director_data(director_name):
    user_agent = user_agent_rotator.get_random_user_agent()
    headers = {"User-Agent": user_agent}
    response = requests.get(search_url.format(director_name.replace(
        " ", "%20")),
                            headers=headers)
    if response.status_code == 200:
        search_results = BeautifulSoup(response.text, "lxml")
        div_preview = search_results.find("div", class_="sc-b03627f1-2 gWHDBT")
        ul = div_preview.find("ul")
        lis = ul.find_all("li")
        obj_div = lis[0].find("div",
                              class_="ipc-metadata-list-summary-item__c")
        obj_a = obj_div.find("a", class_="ipc-metadata-list-summary-item__t")
        if str(obj_a.text).lower() == director_name.lower():
            director_id_url = obj_a["href"]
            data_response = requests.get(imdb_url + director_id_url,
                                         headers=headers)
            data_results = BeautifulSoup(data_response.text, "lxml")
            # description = data_results.find("meta", attrs={"name": "description"})
            description_div = data_results.find(
                "div",
                class_=
                "ipc-html-content ipc-html-content--baseAlt ipc-html-content--display-inline sc-6e8cf83d-1 bHPaCP",
            )
            description_sub_div = description_div.find(
                "div", class_="ipc-html-content-inner-div")
            text_description = description_sub_div.text

            # finding DOB
            personal_info_section = data_results.find(
                "div", {"data-testid": "nm_pd_hd"})
            personal_info_ul = personal_info_section.find("ul")

            personal_info_lis = personal_info_ul.find_all("li")
            date_born_li = personal_info_ul.find("li",
                                                 {"data-testid": "nm_pd_bl"})
            born_date_li = date_born_li.find(
                "li", class_="ipc-inline-list__item test-class-react")
            date_obj = datetime.strptime(born_date_li.text, "%B %d, %Y")

            director_id_url = director_id_url.split("/")
            return (
                director_id_url[director_id_url.index("name") + 1],
                text_description[:2999],
                date_obj,
            )
    return None, None, None


def handle_db():
    # Thin mode (default): only works with Oracle 18c+ and some features may be limited
    conn = oracledb.connect(user="system",
                            password="YourPassword123",
                            dsn="localhost/XEPDB1")
    cursor = conn.cursor()

    def init_drop():
        cursor.execute("DROP TABLE Movie CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Director CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Movie_Review CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Directs_Movie CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Directs_TV_Show CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Movie_Genre CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Movie_Awards CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Movie_SServices CASCADE CONSTRAINTS")

        cursor.execute("DROP TABLE Writes_Movie CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Writes_Show CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Writer_Media CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Writer CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Acts_Movie CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Acts_Show CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Actor_Media CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Actor CASCADE CONSTRAINTS")
        cursor.execute(
            "DROP TABLE Show_Streaming_Services CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Show_Media CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Show_Genre CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Show_Review CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Show_Award CASCADE CONSTRAINTS")
        cursor.execute("DROP TABLE Tv_Show CASCADE CONSTRAINTS")

    def init_create_tables():
        cursor.execute("""
	    CREATE TABLE Movie(
    	    MID             VARCHAR2(11) CONSTRAINT Movie_MID_PK PRIMARY KEY,
    	    Title           VARCHAR2(50),
    	    Runtime         NUMBER(3),
    	    Year_of_Release NUMBER(4),
    	    User_Rating     NUMBER(3,1)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Director(
    	    DID            VARCHAR2(11) CONSTRAINT Director_MID_PK PRIMARY KEY,
    	    FName          VARCHAR2(20),
    	    MInit          CHAR(1),
    	    LName          VARCHAR2(20),
    	    Date_of_Birth  DATE,
    	    Age            NUMBER(3),
    	    Biography      VARCHAR2(3000)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Movie_Review(
    	    MID            VARCHAR2(11),
    	    Reviewer       VARCHAR2(40),
    	    Title          VARCHAR2(50),
    	    Star           NUMBER(2),
    	    Description    VARCHAR2(3000),
    	    MRDate         DATE,
    	    CONSTRAINT Movie_Review_pk PRIMARY KEY(Mid, Reviewer)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Directs_Movie(
    	    MID            VARCHAR2(11),
    	    DID            VARCHAR2(11),
    	    CONSTRAINT Directs_Movie_mid_did_PK PRIMARY KEY(Mid, Did)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Directs_TV_Show(
    	    TID            VARCHAR2(11),
    	    DID            VARCHAR2(11),
    	    CONSTRAINT Directs_TV_Show_tid_did_PK PRIMARY KEY(Tid, Did)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Movie_Genre(
    	    MID            VARCHAR2(11),
    	    MGenre         VARCHAR2(50),
    	    CONSTRAINT Movie_Genre_Mid_Mgenre_PK PRIMARY KEY(Mid, Mgenre)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Movie_Awards(
    	    MID            VARCHAR2(11),
    	    MAwards        VARCHAR2(200),
    	    CONSTRAINT Movie_Awards_Mid_Mawards_PK PRIMARY KEY(Mid, Mawards)
	    )
	    """)

        cursor.execute("""
	    CREATE TABLE Movie_SServices(
    	    MID            VARCHAR2(11),
    	    MSS            VARCHAR2(100),
    	    CONSTRAINT Movie_SServices_Mid_Mss_PK PRIMARY KEY(Mid, Mss)
	    )
	    """)

        cursor.execute("""
	    ALTER TABLE Movie_Review
	    ADD CONSTRAINT Movie_Review_mid_fk FOREIGN KEY(mid)
	    REFERENCES Movie(mid)
	    """)

        cursor.execute("""
	    ALTER TABLE Movie_Genre
	    ADD CONSTRAINT movie_genre_mid_fk FOREIGN KEY(Mid)
	    REFERENCES Movie(Mid)
	    """)

        cursor.execute("""
	    ALTER TABLE Movie_Awards
	    ADD CONSTRAINT movie_awards_mid_fk FOREIGN KEY(Mid)
	    REFERENCES Movie(Mid)
	    """)

        cursor.execute("""
	    ALTER TABLE Movie_SServices
	    ADD CONSTRAINT movie_sservices_mid_fk FOREIGN KEY(Mid)
	    REFERENCES Movie(Mid)
	    """)

        cursor.execute("""
    	    CREATE TABLE Tv_Show
    	    (
        	    id VARCHAR2(11) CONSTRAINT tv_show_id_pk PRIMARY KEY,
        	    title VARCHAR2(200),
        	    tv_show_rating NUMBER(2,1),
        	    year_of_release VARCHAR(15)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Show_Award
    	    (
        	    tv_show_id VARCHAR2(11),
        	    Saward VARCHAR2(500),
        	    CONSTRAINT show_award_tvid_saward_pk PRIMARY KEY(tv_show_id, Saward)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Show_Review
    	    (
        	    tv_show_id VARCHAR2(11),
        	    reviewing_user_id VARCHAR2(100),
        	    title VARCHAR(50),
        	    description VARCHAR2(3000),
        	    star_rating Number(2),
        	    date_of_review DATE,
        	    CONSTRAINT show_review_tvid_reviwer_id_pk PRIMARY KEY(tv_show_id, reviewing_user_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Show_Genre
    	    (
        	    tv_show_id VARCHAR2(11),
        	    genre VARCHAR2(20),
        	    CONSTRAINT show_genre_tvid_genre_pk PRIMARY KEY(tv_show_id, genre)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Show_Media
    	    (
        	    tv_show_id VARCHAR2(11),
        	    media VARCHAR2(20),
        	    CONSTRAINT show_media_tvid_media_pk PRIMARY KEY(media, tv_show_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Show_Streaming_Services
    	    (
        	    tv_show_id VARCHAR2(11),
        	    streaming_service VARCHAR2(20),
        	    CONSTRAINT showSS_media_tvid_pk PRIMARY KEY(streaming_service, tv_show_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Actor
    	    (
        	    actor_id VARCHAR2(11) CONSTRAINT actor_actor_id_pk PRIMARY KEY,
        	    f_name VARCHAR2(25),
        	    m_initial CHAR(1),
        	    l_name VARCHAR2(25),
        	    biography VARCHAR2(3000),
        	    dob DATE,
        	    age NUMBER(3)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Actor_Media
    	    (
        	    actor_id VARCHAR2(11),
        	    media VARCHAR2(20),
        	    CONSTRAINT actor_media_tvid_media_pk PRIMARY KEY(media, actor_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Acts_Show
    	    (
        	    actor_id VARCHAR2(11),
        	    tv_show_id VARCHAR2(11),
        	    CONSTRAINT acts_show_actorid_tvid_pk PRIMARY KEY(actor_id, tv_show_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Acts_Movie
    	    (
        	    actor_id VARCHAR2(11),
        	    movie_id VARCHAR2(11),
        	    CONSTRAINT acts_movie_actorid_movieid_pk PRIMARY KEY(actor_id, movie_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Writer
    	    (
        	    writer_id VARCHAR2(11) CONSTRAINT writer_writer_id PRIMARY KEY,
        	    f_name VARCHAR2(25),
        	    m_initial CHAR(1),
        	    l_name VARCHAR2(25),
        	    biography VARCHAR2(3000),
        	    dob DATE,
        	    age NUMBER(3)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Writer_Media
    	    (
        	    writer_id VARCHAR2(11),
        	    media VARCHAR2(20),
        	    CONSTRAINT writer_media_tvid_media_pk PRIMARY KEY(media, writer_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Writes_Show
    	    (
        	    writer_id VARCHAR2(11),
        	    tv_show_id VARCHAR2(11),
        	    CONSTRAINT writes_show_writerid_tvid_pk PRIMARY KEY(writer_id, tv_show_id)
    	    )
	    """)

        cursor.execute("""
    	    CREATE TABLE Writes_Movie
    	    (
        	    writer_id VARCHAR2(11),
        	    movie_id VARCHAR2(11),
        	    CONSTRAINT writes_movie_wid_mid_pk PRIMARY KEY(writer_id, movie_id)
    	    )
	    """)

        cursor.execute("""
    	    ALTER TABLE Show_Award
    	    ADD CONSTRAINT ShowA_tv_showid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Show_Review
    	    ADD CONSTRAINT ShowR_tv_showid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Show_Genre
    	    ADD CONSTRAINT ShowG_tv_showid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Show_Media
    	    ADD CONSTRAINT ShowM_tv_showid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Show_Streaming_Services
    	    ADD CONSTRAINT ShowSS_tv_showid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Actor_Media 
    	    ADD CONSTRAINT actorMedia_actorid_fk FOREIGN KEY(actor_id)
    	    REFERENCES Actor(actor_id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Acts_Show
    	    ADD CONSTRAINT actorShow_tvid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Acts_Show
    	    ADD CONSTRAINT actorShow_actorid_fk FOREIGN KEY(actor_id)
    	    REFERENCES Actor(actor_id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Acts_Movie
    	    ADD CONSTRAINT actorMovie_actorid_fk FOREIGN KEY(actor_id)
    	    REFERENCES Actor(actor_id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Acts_Movie
    	    ADD CONSTRAINT actorMovie_movieid_fk FOREIGN KEY(movie_id)
    	    REFERENCES movie(MID)
	    """)

        cursor.execute("""
    	    ALTER TABLE Writer_Media
    	    ADD CONSTRAINT Writer_media_writerid_fk FOREIGN KEY(writer_id)
    	    REFERENCES Writer(writer_id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Writes_Show
    	    ADD CONSTRAINT Writes_show_writerid_fk FOREIGN KEY(writer_id)
    	    REFERENCES Writer(writer_id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Writes_Show
    	    ADD CONSTRAINT Writes_show_tvid_fk FOREIGN KEY(tv_show_id)
    	    REFERENCES Tv_Show(id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Writes_Movie
    	    ADD CONSTRAINT Writes_movie_writerid_fk FOREIGN KEY(writer_id)
    	    REFERENCES Writer(writer_id)
	    """)

        cursor.execute("""
    	    ALTER TABLE Writes_Movie
    	    ADD CONSTRAINT Writes_movie_movieid_fk FOREIGN KEY(movie_id)
    	    REFERENCES movie(MID)
	    """)

    # example:
    # cursor.execute("""
    # INSERT INTO Movie (MID, Title, Runtime, Year_of_Release, User_Rating)
    # VALUES ('tt0034583', 'test movie title', 130, 2013, 9.5)
    # """)

    def fill_movie_data():
        for movie_id, _ in movie_ids_json.items():
            print("Doing movie:", movie_id)
            response = requests.get(main_api_url +
                                    media_data_url.format(movie_id))
            movie_data = json.loads(response.text)

            cursor.execute(
                """
            	INSERT INTO Movie (MID, Title, Runtime, Year_of_Release, User_Rating)
            	VALUES (:1, :2, :3, :4, :5)
        	""",
                (
                    movie_id,
                    movie_data.get("Title"),
                    int(movie_data.get("Runtime")[:3]),
                    int(movie_data.get("Year")),
                    float(movie_data.get("imdbRating")),
                ),
            )
            conn.commit()

            movie_director = movie_data.get("Director")

            try:
                director_id, director_description, director_dob = get_director_data(
                    movie_director)
                if director_id != None:
                    if not is_already_created(cursor, director_id, "director"):
                        # add to directors table since not there
                        director_age = calculate_age(director_dob)
                        cursor.execute(
                            """
                            INSERT INTO  Director (DID, FName, MInit, LName, Date_of_Birth, Age, Biography)
                            VALUES (:1, :2, :3, :4, :5, :6, :7)
                            """,
                            (
                                director_id,
                                movie_director.split(" ")[0],
                                None,
                                movie_director.split(" ")[1],
                                director_dob,
                                director_age,
                                director_description,
                            ),
                        )
                        conn.commit()
                    # directs movie
                    cursor.execute(
                        """
                        INSERT INTO  Directs_Movie (MID, DID) 
                        VALUES (:1, :2)
                        """,
                        (movie_id, director_id),
                    )
                    conn.commit()

                # movie genre
                if movie_data.get("Genre"):
                    genres = movie_data.get("Genre").split(",")
                    for genre in genres:
                        cursor.execute(
                            """
                            INSERT INTO Movie_Genre
                            VALUES (:1, :2)
                            """,
                            (movie_id, genre.strip()),
                        )
                        conn.commit()

                # movie awards

                for movie_award in movie_data.get("Awards").split(","):
                    cursor.execute(
                        """
                        INSERT INTO Movie_Awards
                        VALUES (:1, :2)
                        """,
                        (movie_id, movie_award.strip()),
                    )
                    conn.commit()

                # Movie services

                cursor.execute(
                    """
                    INSERT INTO Movie_SServices
                    VALUES (:1, :2)
                    """,
                    (movie_id, "Netflix"),
                )
                conn.commit()

                # Movie reviews

                user, review_title, user_rating, review_content, review_date = (
                    get_movie_review(movie_id))
                cursor.execute(
                    """
                    INSERT INTO Movie_Review
                    VALUES (:1, :2, :3, :4, :5, :6)
                    """,
                    (
                        movie_id,
                        user,
                        review_title,
                        user_rating,
                        review_content,
                        review_date,
                    ),
                )
                conn.commit()

                # Movie actor
                actors = movie_data.get("Actors").split(",")
                for actor in actors:
                    actor = actor.strip()
                    actor_id, actor_description, actor_dob = get_director_data(
                        actor)
                    if actor_id != None:
                        if not is_already_created(cursor, actor_id, "actor"):
                            # add to directors table since not there
                            actor_age = calculate_age(actor_dob)
                            cursor.execute(
                                """
                                INSERT INTO Actor 
                                VALUES (:1, :2, :3, :4, :5, :6, :7)
                                """,
                                (
                                    actor_id,
                                    actor.split(" ")[0],
                                    None,
                                    actor.split(" ")[1],
                                    actor_description,
                                    actor_dob,
                                    actor_age,
                                ),
                            )
                            conn.commit()

                    # acts in movie
                    cursor.execute(
                        """
                        INSERT INTO  Acts_Movie (actor_id, movie_id) 
                        VALUES (:1, :2)
                        """,
                        (actor_id, movie_id),
                    )
                    conn.commit()

                # writer
                writers = movie_data.get("Writer").split(",")
                for writer in writers:
                    writer = writer.strip()
                    writer_id, writer_description, writer_dob = get_director_data(
                        writer)
                    if writer_id != None:
                        if not is_already_created(cursor, writer_id, "writer"):
                            # add to directors table since not there
                            writer_age = calculate_age(writer_dob)
                            cursor.execute(
                                """
                                INSERT INTO Writer 
                                VALUES (:1, :2, :3, :4, :5, :6, :7)
                                """,
                                (
                                    writer_id,
                                    writer.split(" ")[0],
                                    None,
                                    writer.split(" ")[1],
                                    writer_description,
                                    writer_dob,
                                    writer_age,
                                ),
                            )
                            conn.commit()

                    # writes in movie
                    cursor.execute(
                        """
                        INSERT INTO  Writes_Movie (writer_id, movie_id) 
                        VALUES (:1, :2)
                        """,
                        (writer_id, movie_id),
                    )
                    conn.commit()

            except Exception as e:
                print(f"Skipping director {director_id} ...", str(e))

    def fill_tv_data():
        for show_id, _ in tv_show_ids_json.items():
            try:
                response = requests.get(main_api_url +
                                        media_data_url.format(show_id))
                show_data = json.loads(response.text)
                cursor.execute(
                    """
            	    INSERT INTO Tv_Show
            	    VALUES (:1, :2, :3, :4)
        	    """,
                    (
                        show_id,
                        show_data.get("Title"),
                        float(show_data.get("imdbRating")),
                        show_data.get("Year"),
                    ),
                )
                conn.commit()

                show_director = show_data.get("Director")
                show_writers = show_data.get("Writer").split(",")
                show_actors = show_data.get("Actors").split(",")
                show_awards = show_data.get("Awards").split(",")
                show_genres = show_data.get("Genre").split(",")
                director_id, director_description, director_dob = get_director_data(
                    show_director)
                if director_id != None:
                    if not is_already_created(cursor, show_director,
                                              "director"):
                        director_age = calculate_age(director_dob)
                        cursor.execute(
                            """
                            INSERT INTO  Director (DID, FName, MInit, LName, Date_of_Birth, Age, Biography)
                            VALUES (:1, :2, :3, :4, :5, :6, :7)
                            """,
                            (
                                director_id,
                                show_director.split(" ")[0],
                                None,
                                show_director.split(" ")[1],
                                director_dob,
                                director_age,
                                director_description,
                            ),
                        )
                        conn.commit()

                    # directs tv show
                    cursor.execute(
                        """
                        INSERT INTO  Directs_TV_Show (TID, DID) 
                        VALUES (:1, :2)
                        """,
                        (show_id, director_id),
                    )
                    conn.commit()

                # show awards
                for award in show_awards:
                    cursor.execute(
                        """
                        INSERT INTO Show_Award
                        VALUES (:1, :2)
                        """,
                        (show_id, award.strip()),
                    )
                    conn.commit()

                for genre in show_genres:
                    cursor.execute(
                        """
                        INSERT INTO Show_Genre
                        VALUES (:1, :2)
                        """,
                        (show_id, genre.strip()),
                    )
                    conn.commit()

                # show review

                user, review_title, user_rating, review_content, review_date = (
                    get_movie_review(show_id))

                cursor.execute(
                    """
                    INSERT INTO Show_Review
                    VALUES (:1, :2, :3, :4, :5, :6)
                    """,
                    (
                        show_id,
                        user,
                        review_title,
                        review_content,
                        user_rating,
                        review_date,
                    ),
                )
                conn.commit()

                for actor in show_actors:
                    actor = actor.strip()
                    actor_id, actor_description, actor_dob = get_director_data(
                        actor)
                    if actor_id != None:
                        if not is_already_created(cursor, actor_id, "actor"):
                            # add to directors table since not there
                            actor_age = calculate_age(actor_dob)
                            cursor.execute(
                                """
                                INSERT INTO Actor 
                                VALUES (:1, :2, :3, :4, :5, :6, :7)
                                """,
                                (
                                    actor_id,
                                    actor.split(" ")[0],
                                    None,
                                    actor.split(" ")[1],
                                    actor_description,
                                    actor_dob,
                                    actor_age,
                                ),
                            )
                            conn.commit()

                    # acts in show
                    cursor.execute(
                        """
                        INSERT INTO Acts_Show 
                        VALUES (:1, :2)
                        """,
                        (actor_id, show_id),
                    )
                    conn.commit()

                for writer in show_writers:
                    writer = writer.strip()
                    writer_id, writer_description, writer_dob = get_director_data(
                        writer)
                    if writer_id != None:
                        if not is_already_created(cursor, writer_id, "writer"):
                            # add to directors table since not there
                            writer_age = calculate_age(writer_dob)
                            cursor.execute(
                                """
                                INSERT INTO Writer 
                                VALUES (:1, :2, :3, :4, :5, :6, :7)
                                """,
                                (
                                    writer_id,
                                    writer.split(" ")[0],
                                    None,
                                    writer.split(" ")[1],
                                    writer_description,
                                    writer_dob,
                                    writer_age,
                                ),
                            )
                            conn.commit()

                    # writes in show
                    cursor.execute(
                        """
                        INSERT INTO Writes_Show 
                        VALUES (:1, :2)
                        """,
                        (writer_id, show_id),
                    )
                    conn.commit()

            except Exception as e:
                print("Something went wrong filling tv show... ", str(e))

    try:
        print("Dropping tables ...")
        init_drop()
        sleep(0.5)
    except Exception as e:
        print("Something went wrong dropping tables", str(e))
    try:
        print("Initializing tables ...")
        init_create_tables()
    except Exception as e:
        print("something went wrong creating tables", str(e))

    print("Filling movie data .. ")
    fill_movie_data()
    print("Finished filling movie data")
    print("Filling Tv data ... ")
    fill_tv_data()
    print("Finished filling Tv data")

    # cursor.execute("SELECT * FROM Movie")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    #
    cursor.close()
    conn.close()


handle_db()
