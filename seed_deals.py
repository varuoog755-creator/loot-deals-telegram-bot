import database

def seed():
    deals = [
        {
            "title": "Roadster Women Round Neck T-shirt",
            "price": "₹179",
            "mrp": "₹599",
            "discount": "70% OFF",
            "link": "https://earnkaro.com/top-selling-products/today-best-deals",
            "category": "Loot"
        },
        {
            "title": "HERE&NOW Men Printed Casual T-Shirt",
            "price": "₹384",
            "mrp": "₹699",
            "discount": "45% OFF",
            "link": "https://earnkaro.com/top-selling-products/today-best-deals",
            "category": "Loot"
        },
        {
            "title": "Men Stylish Casual Sneakers",
            "price": "₹199",
            "mrp": "₹999",
            "discount": "80% OFF",
            "link": "https://earnkaro.com/top-selling-products/today-best-deals",
            "category": "Loot"
        },
        {
            "title": "Steal Deal: Fast Charging USB Cable & OTG",
            "price": "₹63",
            "mrp": "₹299",
            "discount": "79% OFF",
            "link": "https://earnkaro.com/top-selling-products/today-best-deals",
            "category": "Under99"
        },
        {
            "title": "Ultra-light Digital LED Sports Watch",
            "price": "₹87",
            "mrp": "₹499",
            "discount": "82% OFF",
            "link": "https://earnkaro.com/top-selling-products/today-best-deals",
            "category": "Under99"
        },
        {
            "title": "Daily Essential Personal Grooming Combo",
            "price": "₹75",
            "mrp": "₹249",
            "discount": "70% OFF",
            "link": "https://earnkaro.com/top-selling-products/today-best-deals",
            "category": "Under99"
        }
    ]
    for d in deals:
        database.add_deal(d["title"], d["price"], d["mrp"], d["discount"], d["link"], d["category"])
    print("Default deals seeded successfully!")

if __name__ == "__main__":
    seed()
