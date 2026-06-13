WITH duplicates AS (
    SELECT DISTINCT b1.book_id
    FROM public."Books" b1
    JOIN public."Books" b2 ON b1.isbn = b2.isbn
    WHERE b1.publication_year < b2.publication_year
),
deleted_locations AS (
    DELETE FROM public."Book_location" bl
    USING duplicates d
    WHERE bl.book_id = d.book_id
),
deleted_authors AS (
    DELETE FROM public."Book_authors" ba
    USING duplicates d
    WHERE ba.book_id = d.book_id
)
DELETE FROM public."Books" b
USING duplicates d
WHERE b.book_id = d.book_id;