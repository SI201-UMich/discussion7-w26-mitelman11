import unittest
import os
import csv

###############################################################################
##### TASK 1: CSV READER
###############################################################################
def load_listings(f):
    listings = []

    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    with open(full_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # uses header row as keys
        for row in reader:
            listings.append(row)

    return listings
    # Do not modify this code
    # This opens the CSV and saves it as a list of lists
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    # TODO: Read the CSV using csv.reader and convert it to a list a dictionaries


###############################################################################
##### TASK 2: CALCULATION FUNCTION (single calculation)
###############################################################################
def calculate_avg_price_by_neighbourhood_group_and_room(listings):
    totals = {}   
    counts = {}   

    for listing in listings:
        neighbourhood_group = listing['neighbourhood_group']
        room_type = listing['room_type']

        try:
            price = float(listing['price'])
        except (ValueError, TypeError):
            continue 

        key = (neighbourhood_group, room_type)

        if key not in totals:
            totals[key] = 0.0
            counts[key] = 0

        totals[key] += price
        counts[key] += 1

    averages = {}
    for key in totals:
        averages[key] = totals[key] / counts[key]

    return averages



###############################################################################
##### TASK 3: CSV WRITER
###############################################################################
def write_summary_csv(out_filename, avg_prices):
    """
    Write the summary statistics to a CSV file.

    Parameters:
        out_filename : str
            Path to output CSV file.
        avg_prices : dictionary
            dict mapping (neighbourhood_group, room_type) -> average_price (float)
            e.g. { ('Manhattan', 'Entire home/apt'): 123.45, ... }

    Returns:
        None
            Writes a CSV file with header: neighbourhood_group, room_type, average_price
    """
    pass

###############################################################################
##### UNIT TESTS (Do not modify the code below!)
###############################################################################
class TestAirbnbListings(unittest.TestCase):
    def setUp(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        full_path = os.path.join(base_path, 'new_york_listings_2024.csv')
        self.listings = load_listings(full_path)

    def test_load_listings(self):
        # Test that listings were loaded successfully
        self.assertIsInstance(self.listings, list)
        self.assertGreater(len(self.listings), 0)
        # Check that each listing is a dictionary
        self.assertIsInstance(self.listings[0], dict)
        # Check for expected keys
        expected_keys = ['neighbourhood_group', 'room_type', 'price']
        for key in expected_keys:
            self.assertIn(key, self.listings[0])

    def test_calculate_avg_price_by_neighbourhood_group_and_room(self):
        averages = calculate_avg_price_by_neighbourhood_group_and_room(self.listings)
        
        # Test a few key combinations from the real data
        self.assertAlmostEqual(averages[('Manhattan', 'Entire home/apt')], 253.74735249621784, places=2)

        self.assertAlmostEqual(averages[('Brooklyn', 'Private room')], 161.65877598152426, places=2)

        self.assertAlmostEqual(averages[('Queens', 'Entire home/apt')], 179.92875157629257, places=2)

        self.assertAlmostEqual(averages[('Bronx', 'Private room')], 97.30147058823529, places=2)

        self.assertAlmostEqual(averages[('Staten Island', 'Entire home/apt')], 139.85256410256412, places=2)

    def test_write_and_read_summary(self):
        averages = calculate_avg_price_by_neighbourhood_group_and_room(self.listings)
        test_output = 'test_summary_output.csv'
        
        write_summary_csv(test_output, averages)
        
        with open(test_output, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            # Check that we have the expected number of rows
            self.assertEqual(len(rows), 18)
            
            # Verify header
            self.assertEqual(reader.fieldnames, ['neighbourhood_group', 'room_type', 'average_price'])
        

def main():
    unittest.main(verbosity=2)

if __name__ == '__main__':
    main()
