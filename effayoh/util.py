import os
import csv

TRIPS_BASE = os.environ['TRIPS_BASE']
EFFAYOH_DIR, _ = os.path.split(__file__)
RESOURCES_DIR = os.path.join(TRIPS_BASE, "src/ABN2/resources")
FAOSTAT_DIR = os.path.join(RESOURCES_DIR, "faostat")
USDA_DIR = os.path.join(RESOURCES_DIR, "usda")
PSD_DIR = os.path.join(USDA_DIR, "psd")
