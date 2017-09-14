import os
import csv

TRIPS_BASE = os.environ['TRIPS_BASE']
EFFAYOH_DIR, _ = os.path.split(__file__)
RESOURCES_DIR = os.path.join(EFFAYOH_DIR, "resources")
FAOSTAT_DIR = os.path.join(TRIPS_BASE, "faostat")
USDA_DIR = os.path.join(RESOURCES_DIR, "usda")
PSD_DIR = os.path.join(USDA_DIR, "psd")
