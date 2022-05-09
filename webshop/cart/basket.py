from products.models import Product

class Basket():
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')

        if 'skey' not in request.session:
            basket = self.session['skey'] = {}

        self.basket = basket


    def add(self, product):
        # adding and updating basket session data
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['quantity'] = self.basket[product_id]['quantity'] + 1
        else:
            self.basket[product_id] = {'price': str(product.price), 'quantity': 1}

        self.save()


    def __iter__(self):
        # getting the added products from database using the product ID
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # count quantity of items in basket
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.basket.values())

    
    def delete(self, product):
        # delete item from session data
        productId = str(product)
        if productId in self.basket:
            del self.basket[product]
            self.save()
            data = {
                'quantity': self.__len__(),
                'total': self.get_total_price()
            }
            return data



    def save(self):
        self.session.modified = True
