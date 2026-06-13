BEGIN;


CREATE TABLE IF NOT EXISTS public."Halls"
(
    hall_id serial NOT NULL,
    full_name character varying(64) NOT NULL,
    short_name character varying(64) NOT NULL,
    PRIMARY KEY (hall_id),
    UNIQUE (full_name),
    UNIQUE (short_name)
);

CREATE TABLE IF NOT EXISTS public."Shelves"
(
    shelf_id serial NOT NULL,
    hall_id integer NOT NULL,
    shelf_index integer NOT NULL,
    PRIMARY KEY (shelf_id),
    UNIQUE (hall_id, shelf_index)
);

CREATE TABLE IF NOT EXISTS public."Books"
(
    book_id serial NOT NULL,
    title character varying(64) NOT NULL,
    isbn character varying(20) NOT NULL,
    copies_count integer NOT NULL DEFAULT 1,
    part integer NOT NULL,
    publication_year integer NOT NULL,
    PRIMARY KEY (book_id),
    UNIQUE (part, publication_year, isbn)
);

CREATE TABLE IF NOT EXISTS public."Authors"
(
    author_id serial NOT NULL,
    author_name character varying(64) NOT NULL,
    PRIMARY KEY (author_id),
    UNIQUE (author_name)
);

CREATE TABLE IF NOT EXISTS public."Book_authors"
(
    book_id integer NOT NULL,
    author_id integer NOT NULL,
    book_author_id serial NOT NULL,
    PRIMARY KEY (book_author_id),
    UNIQUE (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS public."Book_location"
(
    location_id serial NOT NULL,
    book_id integer NOT NULL,
    shelf_id integer NOT NULL,
    shelf_position integer NOT NULL,
    PRIMARY KEY (location_id),
    UNIQUE (book_id, shelf_id, shelf_position),
    UNIQUE (shelf_id, shelf_position)
);

ALTER TABLE IF EXISTS public."Shelves"
    ADD FOREIGN KEY (hall_id)
    REFERENCES public."Halls" (hall_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Book_authors"
    ADD FOREIGN KEY (author_id)
    REFERENCES public."Authors" (author_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Book_authors"
    ADD FOREIGN KEY (book_id)
    REFERENCES public."Books" (book_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Book_location"
    ADD FOREIGN KEY (book_id)
    REFERENCES public."Books" (book_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Book_location"
    ADD FOREIGN KEY (shelf_id)
    REFERENCES public."Shelves" (shelf_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE public."Books"
ADD CONSTRAINT chk_books_title_length 
CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 64);

ALTER TABLE public."Books"
ADD CONSTRAINT chk_books_isbn_length 
CHECK (LENGTH(isbn) >= 1 AND LENGTH(isbn) <= 20);

ALTER TABLE public."Books"
ADD CONSTRAINT chk_books_copies_count_positive 
CHECK (copies_count >= 0);

ALTER TABLE public."Books"
ADD CONSTRAINT chk_books_part_positive 
CHECK (part > 0);

ALTER TABLE public."Books"
ADD CONSTRAINT chk_books_publication_year 
CHECK (
    publication_year > 0
);

ALTER TABLE public."Halls"
ADD CONSTRAINT chk_halls_full_name_length 
CHECK (LENGTH(full_name) >= 1 AND LENGTH(full_name) <= 64);

ALTER TABLE public."Halls"
ADD CONSTRAINT chk_halls_short_name_length 
CHECK (LENGTH(short_name) >= 1 AND LENGTH(short_name) <= 64);

ALTER TABLE public."Shelves"
ADD CONSTRAINT chk_shelves_shelf_index_positive 
CHECK (shelf_index > 0);

ALTER TABLE public."Book_location"
ADD CONSTRAINT chk_book_location_shelf_position_positive 
CHECK (shelf_position > 0);

ALTER TABLE public."Authors"
ADD CONSTRAINT chk_authors_name_length 
CHECK (LENGTH(author_name) >= 1 AND LENGTH(author_name) <= 64);
END;
