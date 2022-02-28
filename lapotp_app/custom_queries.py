from django.db import connection

def top_laptops(limit):
    """-- select avg(laptop_grade),laptop_id, laptops.product from reviews join laptops
     on laptops.id = reviews.laptop_id group by laptop_id, laptops.product
      order by avg(-laptop_grade) limit 5;
    """
    with connection.cursor() as cursor:
        cursor.execute("""
        select avg(laptop_grade),laptop_id, laptops.product from reviews join laptops
        on laptops.id = reviews.laptop_id group by laptop_id, laptops.product
        order by avg(-laptop_grade) limit %s""",
                       [limit])
        rows = cursor.fetchall()
        res_list = [{"avg":row[0],"laptop_id":row[1],"product":row[2]} for row in rows]
        return res_list

def score_by_manu():
        """
        select  l.manufacturer_id,m.name, avg(laptop_grade) as avg_score ,count(laptop_grade)
        from reviews join laptops l join manufactorer m on l.manufacturer_id = m.id on reviews.laptop_id = l.id
        group by l.manufacturer_id, m.name
        """

        with connection.cursor() as cursor:
            cursor.execute("""
            select  l.manufacturer_id,m.name, avg(laptop_grade) as avg_score ,count(laptop_grade)
            from reviews join laptops l join manufactorer m on l.manufacturer_id = m.id on reviews.laptop_id = l.id
            group by l.manufacturer_id, m.name
            """)
            rows = cursor.fetchall()
            res_list = [{"Manufactorer":row[1],"Average Score": row[2],"Reviews Count": row[3]} for row in rows]
            return res_list


def cheap_but_rate(limit):
    """
    select laptop_id, avg(laptop_grade), laptops.price_euro from laptops join reviews r
    on laptops.id = r.laptop_id group by laptop_id, laptops.price_euro order by laptops.price_euro,avg(-laptop_grade) limit 5;
    """
    with connection.cursor() as cursor:
        cursor.execute("""
        select laptop_id, avg(laptop_grade), laptops.price_euro from laptops join reviews r
    on laptops.id = r.laptop_id group by laptop_id, laptops.price_euro order by laptops.price_euro,avg(-laptop_grade) limit %s;""",
                       [limit])
        rows = cursor.fetchall()
        res_list = [{"laptop_id":row[0],"laptop grade":row[1],"laptop price":row[2]} for row in rows]
        return res_list
