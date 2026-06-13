with count_shelf as(
    select count(*) c, shelf_id from public."Book_location" b_l
    group by shelf_id
),
max_c_s as(
    select c_s.shelf_id from count_shelf c_s
    join public."Shelves" s on s.shelf_id= c_s.shelf_id
    where c=(select max(c) from count_shelf)
    order by s.shelf_index asc
    limit 1
)
select distinct b.title from public."Books" b
join public."Book_location" b_l on b_l.book_id= b.book_id
join max_c_s m on b_l.shelf_id= m.shelf_id;