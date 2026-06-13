select distinct b.title,
    a.author_name,
    count(*) over (partition by a.author_id) count_books,
    count(*) over (partition by b.book_id) count_coauthors
from "Books" b
join "Book_authors" ba on ba.book_id = b.book_id
join "Authors" a on a.author_id = ba.author_id
order by b.title, a.author_name;