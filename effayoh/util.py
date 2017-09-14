import os
import csv

EFFAYOH_DIR, _ = os.path.split(__file__)
RESOURCES_DIR = os.path.join(EFFAYOH_DIR, "resources")
FAOSTAT_DIR = os.path.join(RESOURCES_DIR, "faostat")
USDA_DIR = os.path.join(RESOURCES_DIR, "usda")
PSD_DIR = os.path.join(USDA_DIR, "psd")
