# PConc A3Q1
# ICS3UI-01, Ms Harris
# Jonathan H
# Began: Nov 9, 2019
# Finished : Nov 11, 2019

'''
I/O Question: Find a data set you are interested in. If stuck,
go to Environment Canada or UW weather stats and
download something. The data set must have at least 100
rows and 10 columns. Create a flowchart, then write a program
that reads in your txt or csv file and writes out a summary file
containing averages and/or max and min values for the data set
and whatever other total information is relevant.
'''

# For this question I am going to be looking at world population over time
# I am using UN population data since 1960
# Dataset was taken from https://github.com/datasets/population/blob/master/data/population.csv
# Since there are so many countries, printing all the data is going to take a long time
# I am going to make a summary file that covers a few important countries and prints their data
# The summary file is located in data/summary.txt

import csv, os, time

# Country class
# contains some helpful methods for computing the summary file
class Country:
    def __init__(self, name, code):
        # name and code
        self.name = name
        self.code = code

        # dictionary mapping year to population count
        self.yearly_populations = {}

    # gets the population from 2016
    def pop_in(self, year):
        return self.yearly_populations[year]

    # adds/updates a yearly population number
    def add_year(self, year, value):
        self.yearly_populations[year] = value

    # computes population difference between two years, negative if decreased
    def difference(self, year1, year2):
        latest = year1 if year1 > year2 else year2
        oldest = year1 if latest is year2 else year2
        return self.yearly_populations[latest] - self.yearly_populations[oldest]

    # gets average population growth over time
    def avg_growth_over(self, year1, year2):
        latest = year1 if year1 > year2 else year2
        oldest = year1 if latest is year2 else year2

        difference_sum = 0
        years = 0
        for year in range(oldest + 1, latest + 1, 2):
            difference_sum += self.difference(year, year - 1)
            years += 1
        return difference_sum/years

    # returns a string summary of the country
    def get_summary(self):
        # Current population
        cur_pop = "Current population: {}".format(round(self.yearly_populations[2016]))

        # Change from 1960 to 2019
        change = "Change in population from 1960 to 2016: {}".format(round(self.difference(2016, 1960)))

        # Average yearly growth
        avg_growth = "Average yearly growth: {}".format(round(self.avg_growth_over(2016, 1960)))

        sum = "{} ({})\n===================\n{}\n{}\n{}".format(self.name, self.code, cur_pop, change, avg_growth)
        return sum

class DataLoader:
    # use os.path.join to make sure things work on linux, mac, and windows
    data_file = os.path.join(os.path.join(os.path.dirname(__file__), "data"), "world_population.csv")
    summary_file = os.path.join(os.path.join(os.path.dirname(__file__), "data"), "summary.txt")

    @staticmethod
    def load_data_as_obj():
        with open(DataLoader.data_file, "r") as dataset:
            reader = csv.reader(dataset)
            next(reader)

            # csv format
            # Name, Code, Year, Population

            countries = {}

            for line in reader:
                # for convenience
                name = line[0]
                code = line[1]
                year = int(line[2])
                pop = float(line[3])

                # serialize into country object
                if name not in countries:
                    countries[name] = Country(name, code)
                countries[name].add_year(year, pop)

            dataset.close()
            return countries

    @staticmethod
    def write_summary():
        # open the csv file and use the data
        countries = DataLoader.load_data_as_obj()

        # create the summary file
        with open(DataLoader.summary_file, "w") as summary:

            # Some basic information text
            summary.write("Summary file for A3Q1, created at {}\n".format(time.time()))
            summary.write("Interesting trends and statistics from world_population.csv\n\n")

            # Write the summary data

            # Overview
            pop_1960_high = countries["Afghanistan"]
            pop_1960_low = countries["Afghanistan"]
            pop_2016_high = countries["Afghanistan"]
            pop_2016_low = countries["Afghanistan"]
            for key in countries:
                c = countries[key]
                if 1960 not in c.yearly_populations or 2016 not in c.yearly_populations:
                    continue
                else:
                    if c.pop_in(1960) > pop_1960_high.pop_in(1960):
                        pop_1960_high = c
                    if c.pop_in(1960) < pop_1960_low.pop_in(1960):
                        pop_1960_low = c
                    if c.pop_in(2016) > pop_2016_high.pop_in(2016):
                        pop_2016_high = c
                    if c.pop_in(2016) < pop_2016_low.pop_in(2016):
                        pop_2016_low = c

            summary.write("Country Overview\n===================\n")
            summary.write("Most populous country in 1960: {} with {} people\n".format(pop_1960_high.name, round(pop_1960_high.pop_in(1960))))
            summary.write("Least populous country in 1960: {} with {} people \n".format(pop_1960_low.name, round(pop_1960_low.pop_in(1960))))
            summary.write("Most populous country in 2016: {} with {} people\n".format(pop_2016_high.name, round(pop_2016_high.pop_in(2016))))
            summary.write("Least populous country in 2016: {} with {} people\n\n".format(pop_2016_low.name, round(pop_2016_low.pop_in(2016))))

            # Canada
            summary.write("{}\n\n".format(countries["Canada"].get_summary()))

            # UK
            summary.write("{}\n\n".format(countries["United Kingdom"].get_summary()))

            # France
            summary.write("{}\n\n".format(countries["France"].get_summary()))

            # Germany
            summary.write("{}\n\n".format(countries["Germany"].get_summary()))

            # Italy
            summary.write("{}\n\n".format(countries["Italy"].get_summary()))

            # Spain
            summary.write("{}\n\n".format(countries["Spain"].get_summary()))

            # Russian Federation
            summary.write("{}\n\n".format(countries["Russian Federation"].get_summary()))

            # USA
            summary.write("{}\n\n".format(countries["United States"].get_summary()))

            # China
            summary.write("{}\n\n".format(countries["China"].get_summary()))

            # India
            summary.write("{}\n\n".format(countries["India"].get_summary()))

            # Japan
            summary.write("{}\n\n".format(countries["Japan"].get_summary()))

            # Egypt
            summary.write("{}\n\n".format(countries["Egypt, Arab Rep."].get_summary()))

            summary.close()

# Writes the summary
DataLoader.write_summary()
