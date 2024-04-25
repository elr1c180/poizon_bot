from get_cny import get_cny
import sqlite3

def calc_order_func(price, item_type, promo=None):
    weigth = 0
    rate = get_cny()["rub_rate_plus"]
    
    if item_type == 'summer':
        weigth = 1.5
    
    if item_type == 'winter':
        weigth = 2.5
    
    if item_type == 'shirt':
        weigth = 0.5

    if item_type == 'jeans':
        weigth = 1
    
    if item_type == 'parf':
        weigth = 0.5
    
    if item_type == 'bag':
        weigth = 1.5
    
    if item_type == 'socks':
        weigth = 0.3
    
    if promo:
        with sqlite3.connect('promo.db') as conn:
            cur = conn.cursor()
            cur.execute(f''' SELECT * FROM promo WHERE name='{promo}' ''')
            try:
                print(1)
                disc = int(cur.fetchone()[2])
                price_rub = price * rate
                perc = 0.25 - (disc / 100)
                weigth = weigth * 600

                total = ( price_rub + (price_rub * perc) + weigth )
                total_without_promo = ( price_rub + (price_rub * 0.25) + weigth )
                return {'total': total,'total_without_promo':round(total_without_promo,2)}
            except Exception as e:
                print(e, 2)
                weigth = weigth * 600
                print(weigth)
                price_rub = (price * rate + ((price * rate)) * 0.25) + weigth
                return {'total':price_rub,'total_without_promo':price_rub}
    else:
        print(3)
        # Цена * Z + X + (25% – W(промо код)) + кол-во кг*Y(600руб)
        weigth = weigth * 600
        print(weigth)
        price_rub = (price * rate + ((price * rate)) * 0.25) + weigth
        return {'total':price_rub,'total_without_promo':price_rub}
