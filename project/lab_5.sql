create or replace function check_shelf_distance() returns trigger as$$ 
declare 
    v_book_title varchar(64);
    v_new_shelf_index integer; 
    v_min_index integer; 
    v_max_index integer; 
begin 
    select title into v_book_title from public."Books" where book_id= NEW.book_id;
    select shelf_index into v_new_shelf_index from public."Shelves" where shelf_id= NEW.shelf_id;
    
    select max(s.shelf_index), min(s.shelf_index) into v_max_index, v_min_index 
    from public."Book_location" bl 
    join public."Shelves" s on s.shelf_id= bl.shelf_id 
    join public."Books" b on b.book_id= bl.book_id 
    where b.title= v_book_title;
    
    if v_min_index is not null then 
        if abs(v_new_shelf_index-v_min_index)> 5 or abs(v_new_shelf_index-v_max_index)> 5 then 
            raise exception 'Книга "%" не может быть добавлена на позицию%', v_book_title, v_new_shelf_index; 
        end if; 
    end if; 
    
    return NEW; 
end; 
$$ LANGUAGE plpgsql;

create trigger trg_check_shelf_distance 
before insert on public."Book_location" 
for each row 
execute function check_shelf_distance();