import os
import csv
import itertools


SCRIPTS_DIR, _ = os.path.split(__file__)
EFFAYOH_DIR, _ = os.path.split(SCRIPTS_DIR)
TESTS_DIR = os.path.join(EFFAYOH_DIR, "tests")
RESOURCES_DIR = os.path.join(TESTS_DIR, "resources")


years = [str(year) for year in range(2005, 2010)]

def make_psd_dummy_data(n=4):
    """ Generate dummy PSD data for n countries. """

    header = [
        "Commodity_Code",
        "Commodity_Description",
        "Country_Code",
        "Country_Name",
        "Market_Year",
        "Attribute_ID",
        "Attribute_Description",
        "Value"
    ]

    commodities = [
        ("0430000", "Barley"),
        ("0440000", "Corn"),
        ("0459100", "Millet"),
        ("0459900", "Mixed Grain"),
        ("0452000", "Oats"),
        ("0422110", "Rice, Milled"),
        ("0451000", "Rye"),
        ("0459200", "Sorghum"),
        ("0410000", "Wheat")
    ]

    countries = [
        ("US","United States"),
        ("CH","China, Peoples Republic of"),
        ("GM","Germany"),
        ("RS","Russian Federation")
    ]

    if len(countries) < n:
        msg = "There are fewer available PSD countries than requested."
        raise ValueError(msg)

    attributes = [
        ("176", "Ending Stocks"),
        ("125", "Domestic Consumption")
    ]

    PSD_DIR = os.path.join(RESOURCES_DIR, "usda", "psd")
    fname = "psd_simple-{n}-network.csv".format(**locals())
    fpath = os.path.join(PSD_DIR, fname)

    with open(fpath, "w") as fh:
        writer = csv.writer(fh, delimiter=",")
        writer.writerow(header)
        for i in range(n):
            country_code, country_name = countries[i]
            value = i + 1
            combinations = itertools.product(commodities, years, attributes)
            for (ccode, cdesc), year, (attr_id, attr_desc) in combinations:
                writer.writerow([
                    ccode,
                    cdesc,
                    country_code,
                    country_name,
                    year,
                    attr_id,
                    attr_desc,
                    value
                ])

def make_fbs_dummy_data(n=4):

    header = [
        "Area Code",
        "Area",
        "Item Code",
        "Item",
        "Element Code",
        "Element",
        "Y1961", "Y1961F",
        "Y1962", "Y1962F",
        "Y1963", "Y1963F",
        "Y1964", "Y1964F",
        "Y1965", "Y1965F",
        "Y1966", "Y1966F",
        "Y1967", "Y1967F",
        "Y1968", "Y1968F",
        "Y1969", "Y1969F",
        "Y1970", "Y1970F",
        "Y1971", "Y1971F",
        "Y1972", "Y1972F",
        "Y1973", "Y1973F",
        "Y1974", "Y1974F",
        "Y1975", "Y1975F",
        "Y1976", "Y1976F",
        "Y1977", "Y1977F",
        "Y1978", "Y1978F",
        "Y1979", "Y1979F",
        "Y1980", "Y1980F",
        "Y1981", "Y1981F",
        "Y1982", "Y1982F",
        "Y1983", "Y1983F",
        "Y1984", "Y1984F",
        "Y1985", "Y1985F",
        "Y1986", "Y1986F",
        "Y1987", "Y1987F",
        "Y1988", "Y1988F",
        "Y1989", "Y1989F",
        "Y1990", "Y1990F",
        "Y1991", "Y1991F",
        "Y1992", "Y1992F",
        "Y1993", "Y1993F",
        "Y1994", "Y1994F",
        "Y1995", "Y1995F",
        "Y1996", "Y1996F",
        "Y1997", "Y1997F",
        "Y1998", "Y1998F",
        "Y1999", "Y1999F",
        "Y2000", "Y2000F",
        "Y2001", "Y2001F",
        "Y2002", "Y2002F",
        "Y2003", "Y2003F",
        "Y2004", "Y2004F",
        "Y2005", "Y2005F",
        "Y2006", "Y2006F",
        "Y2007", "Y2007F",
        "Y2008", "Y2008F",
        "Y2009", "Y2009F",
        "Y2010", "Y2010F",
        "Y2011", "Y2011F",
        "Y2012", "Y2012F",
        "Y2013","Y2013F"
    ]

    countries = [
        ("231", "United States of America"),
        ("351", "China"),
        ("79", "Germany"),
        ("185", "Russian Federation")
    ]

    items = [
        # A list of (item, code) tuples.
        ("Wheat and products", "2511"),
        ("Rice (Milled Equivalent)", "2805"),
        ("Barley and products", "2513"),
        ("Maize and products", "2514"),
        ("Cereals, other", "2520"),
        ("Rye and products", "2515"),
        ("Oats", "2516"),
        ("Millet and products", "2517"),
        ("Sorghum and products", "2518"),
        ("Infant food", "2680")
    ]

    elements = [
        ("Food", "5142"),
        ("Feed", "5521"),
        ("Seed", "5527"),
        ("Processing", "5131"),
        ("Waste", "5123"),
        ("Other uses", "5154"),
        ("Production", "5511")
    ]

    FBS_DIR = os.path.join(RESOURCES_DIR, "fao", "fbs")
    fname = "fbs_simple-{n}-network.csv".format(**locals())
    fpath = os.path.join(FBS_DIR, fname)

    with open(fpath, "w") as fh:
        writer = csv.writer(fh, delimiter=",")
        writer.writerow(header)

        for i in range(n):
            country_code, country_name = countries[i]
            value = i + 1
            combinations = itertools.product(items, elements)
            for (item, icode), (elem, ecode) in combinations:
                writer.writerow([
                    country_code,
                    country_name,
                    icode,
                    item,
                    ecode,
                    elem
                ] + ([str(value)]*106))

def make_dtm_dummy_data(n=4):

    header = [
        "Reporter Country Code",
        "Reporter Countries",
        "Partner Country Code",
        "Partner Countries",
        "Item Code",
        "Item",
        "Element Code",
        "Element",
        "Y1986", "Y1986F",
        "Y1987", "Y1987F",
        "Y1988", "Y1988F",
        "Y1989", "Y1989F",
        "Y1990", "Y1990F",
        "Y1991", "Y1991F",
        "Y1992", "Y1992F",
        "Y1993", "Y1993F",
        "Y1994", "Y1994F",
        "Y1995", "Y1995F",
        "Y1996", "Y1996F",
        "Y1997", "Y1997F",
        "Y1998", "Y1998F",
        "Y1999", "Y1999F",
        "Y2000", "Y2000F",
        "Y2001", "Y2001F",
        "Y2002", "Y2002F",
        "Y2003", "Y2003F",
        "Y2004", "Y2004F",
        "Y2005", "Y2005F",
        "Y2006", "Y2006F",
        "Y2007", "Y2007F",
        "Y2008", "Y2008F",
        "Y2009", "Y2009F",
        "Y2010", "Y2010F",
        "Y2011", "Y2011F",
        "Y2012", "Y2012F",
        "Y2013", "Y2013F"
    ]

    countries = [
        ("231", "United States of America"),
        ("351", "China"),
        ("79", "Germany"),
        ("185", "Russian Federation")
    ]

    items = [
        ("Wheat", "15"),
        ("Flour, wheat", "16"),
        ("Macaroni", "18"),
        ("Bread", "20"),
        ("Bulgur", "21"),
        ("Pastry", "22"),
        ("Rice - total  (Rice milled equivalent)", "30"),
        ("Cereals, breakfast", "41"),
        ("Barley", "44"),
        ("Barley, pearled", "46"),
        ("Malt", "49"),
        ("Maize", "56"),
        ("Germ, maize", "57"),
        ("Flour, maize", "58"),
        ("Popcorn", "68"),
        ("Rye", "71"),
        ("Oats", "75"),
        ("Oats rolled", "76"),
        ("Millet", "79"),
        ("Sorghum", "83"),
        ("Buckwheat", "89"),
        ("Fonio", "94"),
        ("Flour, fonio", "95"),
        ("Triticale", "97"),
        ("Canary seed", "101"),
        ("Grain, mixed", "103"),
        ("Flour, mixed grain", "104"),
        ("Infant food", "109"),
        ("Infant food", "110"),
        ("Flour, cereals", "111"),
        ("Cereal preparations, nes", "113"),
        ("Mixes and doughs", "114"),
        ("Food preparations, flour, malt extract", "115")
    ]

    elements = [
        ("Export Quantity", "5910")
    ]

    DTM_DIR = os.path.join(RESOURCES_DIR, "fao", "dtm")
    fname = "dtm_simple-{n}-network.csv".format(**locals())
    fpath = os.path.join(DTM_DIR, fname)

    with open(fpath, "w") as fh:
        writer = csv.writer(fh, delimiter=",")
        writer.writerow(header)

        for i in range(n):
            reporter_country_code, reporter_country_name = countries[i]
            value = 0.1 * (i+1)
            partner_countries = countries[:i] + countries[i+1:n]
            combinations = itertools.product(partner_countries, items, elements)
            for (pcode, partner), (item, icode), (elem, ecode) in combinations:
                writer.writerow([
                    reporter_country_code,
                    reporter_country_name,
                    pcode,
                    partner,
                    icode,
                    item,
                    ecode,
                    elem
                ] + ([str(value)]*56))

def main():
    make_psd_dummy_data()
    make_fbs_dummy_data()
    make_dtm_dummy_data()

if __name__ == "__main__":
    main()
