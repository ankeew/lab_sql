create or replace view book_full_info as 
select b.book_id, b.title, b.copies_count, b.isbn, b.publication_year, b.part, 
       s.shelf_id, s.shelf_index, bl.shelf_position 
from "Books" b 
join "Book_location" bl on b.book_id= bl.book_id 
join "Shelves" s on s.shelf_id= bl.shelf_id;


create or replace function insert_original_books() returns trigger as$$
begin 
    update "Books" set copies_count= NEW.copies_count where book_id= OLD.book_id; 
    return new; 
end; 
$$ language plpgsql;


create trigger insert_view_books 
instead of update on book_full_info 
for each row 
execute function insert_original_books();