companies1 = []
companies = ['google', 'adobe', 'amazone', 'facebook']
for var in reversed(range(len(companies))):
    companies1.append(companies[var])
print(companies1)


#######################################

company = ['google', 'adobe', 'amazone', 'facebook', 'flipkart']
user_id = ['a', 'b', 'c', 'd']
user_age = [1, 2, 3, 4, 7]
print(list(zip(company, user_id, user_age)))
print(dict(zip(company, user_id)))
