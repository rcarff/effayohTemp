"""
Provides the FAOSTATPopulationFilter class.

The FAOSTATPopulationFilter implements a filter for excluding countries
with populations of less than or equal to half a million people.

"""

import os
import csv
import io

from effayoh.mungers import FAOCountry
from effayoh.mungers.fbs import FBSItem, FBSElement

from effayoh.rectification.political_entities import FAOPolitEnt
from effayoh.resources.faostat import map as map_

from effayoh.util import FAOSTAT_DIR


data_path = os.path.join(
    FAOSTAT_DIR,
    "food-balance-sheets/",
    "FoodBalanceSheets_E_All_Data.csv"
)

POPULATION_ITEM = FBSItem(item="Population", code="2501")
POPULATION_ELEMENT = FBSElement(element="Total Population - Both sexes",
                                code="511")

# Some countries do not have population data reported in the food
# balance sheets and must be manually excluded.
EXCLUDED_COUNTRIES = [
    map_[FAOCountry("Seychelles", "196")],
    FAOPolitEnt.MALTA,
    FAOPolitEnt.COOK_ISLANDS,
    FAOPolitEnt.ANDORRA,
    FAOPolitEnt.FAROE_ISLANDS,
    FAOPolitEnt.GUAM,
    FAOPolitEnt.GREENLAND,
    FAOPolitEnt.FRENCH_GUIANA,
    FAOPolitEnt.GIBRALTAR,
    FAOPolitEnt.CHRISTMAS_ISLAND,
    FAOPolitEnt.CAYMAN_ISLANDS,
    FAOPolitEnt.GUADELOUPE,
    FAOPolitEnt.COCOS,
    FAOPolitEnt.FALKLAND_ISLANDS,
    FAOPolitEnt.ARUBA,
    FAOPolitEnt.LIECNTENSTEIN,
    FAOPolitEnt.BRITISH_INDIAN_OCEAN_TERRITORY,
]

years = list(range(2006, 2010+1))


class FAOSTATPopulationFilter:

    def __init__(self, years=years, threshold=500000.0):
        """
        Compute the countries that do not reach the threshold.

        """

        self.country_populations = {}
        self.excluded_countries = set(EXCLUDED_COUNTRIES)
        years_fields = [(year, "Y" + str(year)) for year in years]

        with io.open(data_path, mode='rb') as fh:

            reader = csv.DictReader(fh)

            for row in reader:

                country = FAOCountry(
                    country=row["Area"],
                    code=row["Area Code"]
                )

                item = FBSItem(
                    item=row["Item"],
                    code=row["Item Code"]
                )
                if not item is POPULATION_ITEM:
                    continue

                element = FBSElement(
                    element=row["Element"],
                    code=row["Element Code"]
                )
                if not element is POPULATION_ELEMENT:
                    continue

                values = []
                for year, field in years_fields:
                    try:
                        value = float(row[field])
                        values.append(value)
                    except ValueError as ve:
                        pass

                if not values:
                    print(("FAOCountry {country} does not have any "
                           "population in the time period including the"
                           " years {years}").format(**locals()))
                    continue

                population = sum(values) / len(values)
                # Adjust for the fact that the Food Balance Sheet
                # reports values in units of "1000 persons"
                population *= 1000.0

                effpent = map_.get(country, None)
                if effpent is None:
                    continue

                self.country_populations[effpent] = population

                if population <= threshold:
                    self.excluded_countries.add(effpent)

        if FAOPolitEnt.LUXEMBOURG in self.excluded_countries:
            self.excluded_countries.remove(FAOPolitEnt.LUXEMBOURG)

    def excludes(self, effpent):
        return effpent in self.excluded_countries
