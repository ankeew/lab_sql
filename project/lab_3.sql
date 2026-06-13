create or replace function get_author_p(author varchar(64))
returns numeric as$$ 
declare 
    p numeric; 
begin 
    select coalesce(sum(1.0/count(ba2.author_id)),0) into p 
    from "Authors" a 
    join "Book_authors" ba on ba.author_id= a.author_id 
    join "Book_authors" ba2 on ba2.book_id = ba.book_id
    where a.author_name= author 
    group by ba.book_id;
    
    return coalesce(p,0.0); 
end; 
$$ LANGUAGE plpgsql;

--пример вызова функции
select get_author_p('Толстой Лев Николаевич');