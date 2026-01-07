stocks = [
    {'symbol': 'APA', 'pe': 5.75, 'price': 23.88, 'high': 27.72},
    {'symbol': 'GM', 'pe': 7.14, 'price': 81.00, 'high': 83.68},
    {'symbol': 'DAL', 'pe': 10.12, 'price': 70.52, 'high': 73.16},
    {'symbol': 'UAL', 'pe': 10.84, 'price': 117.27, 'high': 119.21}, # Using snippet 4.2 price
    {'symbol': 'VZ', 'pe': 8.58, 'price': 40.80, 'high': 47.36},
    {'symbol': 'MO', 'pe': 10.74, 'price': 55.22, 'high': 68.60},
    {'symbol': 'BAC', 'pe': 13.21, 'price': 57.25, 'high': 57.55},
    {'symbol': 'C', 'pe': 13.10, 'price': 68.00, 'high': 68.00}, # Estimate based on "New High"
    {'symbol': 'HE', 'pe': 15.44, 'price': 13.41, 'high': 13.41},
    {'symbol': 'CVS', 'pe': 11.25, 'price': 80.42, 'high': 85.15},
    {'symbol': 'PFE', 'pe': 14.67, 'price': 25.45, 'high': 27.69},
    {'symbol': 'MOS', 'pe': 6.24, 'price': 24.10, 'high': 38.23},
    {'symbol': 'EQT', 'pe': 18.24, 'price': 53.46, 'high': 62.23},
    {'symbol': 'NUE', 'pe': 23.63, 'price': 169.35, 'high': 171.94},
    {'symbol': 'BMY', 'pe': 18.05, 'price': 53.58, 'high': 63.33},
]

for s in stocks:
    s['y'] = 1 - (s['price'] / s['high'])

# Find Pareto Front (Min PE, Min Y)
front = []
for s in stocks:
    is_dominated = False
    for other in stocks:
        if s['symbol'] == other['symbol']:
            continue
        # Check if 'other' dominates 's'
        # Dominates if other.pe <= s.pe AND other.y <= s.y AND (at least one strict)
        if (other['pe'] <= s['pe'] and other['y'] <= s['y']) and \
           (other['pe'] < s['pe'] or other['y'] < s['y']):
            is_dominated = True
            break
    if not is_dominated:
        front.append(s)

# Sort front by PE
front.sort(key=lambda x: x['pe'])
print("Pareto Front:")
for f in front:
    print(f)
    
# Check near front (dominated by only 1-2 points?)
