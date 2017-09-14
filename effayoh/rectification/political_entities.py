import enum

@enum.unique
class FAOPolitEnt(enum.Enum):

    AFGHANISTAN = "Afghanistan"
    ALAND_ISLANDS = "Aland Islands"
    ALBANIA = "Albania"
    ALGERIA = "Algeria"
    ANDORRA = "Andorra"
    ANGOLA = "Angola"
    ANGUILLA = "Anguilla"
    ANTARCTICA = "Antarctica"
    ANTIGUA_AND_BARBUDA = "Antigua and Barbuda"
    ARGENTINA = "Argentina"
    ARMENIA = "Armenia"
    ARUBA = "Aruba"
    AUSTRALIA = "Australia"
    AUSTRIA = "Austria"
    AZERBAIJAN = "Azerbaijan"
    BAHAMAS = "Bahamas"
    BAHRAIN = "Bahrain"
    BANGLADESH = "Bangladesh"
    BARBADOS = "Barbados"
    BELARUS = "Belarus"
    BELGIUM = "Belgium"
    BELGIUM_LUXEMBOURG = "Belgium-Luxembourg"
    BELIZE = "Belize"
    BENIN = "Benin"
    BERMUDA = "Bermuda"
    BHUTAN = "Bhutan"
    BOLIVIA = "Bolivia (Plurinational State of)"
    BOSNIA_AND_HERZEGOVINA = "Bosnia and Herzegovina"
    BOTSWANA = "Botswana"
    BOUVET_ISLAND = "Bouvet Island"
    BRAZIL = "Brazil"
    BRITISH_INDIAN_OCEAN_TERRITORY = "British Indian Ocean Territory"
    BRUNEI_DARUSSALAM = "Brunei Darussalam"
    BULGARIA = "Bulgaria"
    BURKINA_FASO = "Burkina Faso"
    BURUNDI = "Burundi"
    CABO_VERDE = "Cabo Verde"
    CAMBODIA = "Cambodia"
    CAMEROON = "Cameroon"
    CANADA = "Canada"
    CARIBBEAN = "Caribbean"
    CAYMAN_ISLANDS = "Cayman Islands"
    CENTRAL_AFRICAN_REPUBLIC = "Central African Republic"
    CHAD = "Chad"
    CHANNEL_ISLANDS = "Channel Islands"
    CHILE = "Chile"
    CHINA = "China"
    CHINA_EXC_HK_MACAO = "China (exc. Hong Kong & Macao)"
    CHINA_HK_SAR = "China, Hong Kong SAR"
    CHINA_MACAO_SAR = "China, Macao SAR"
    CHINA_MAINLAND = "China, mainland"
    CHINA_TAIWAN = "China, Taiwan Province of"
    CHRISTMAS_ISLAND = "Christmas Island"
    COCOS = "Cocos (Keeling) Islands"
    COLOMBIA = "Colombia"
    COMOROS = "Comoros"
    CONGO = "Congo"
    COOK_ISLANDS = "Cook Islands"
    COSTA_RICA = "Costa Rica"
    COTE_DIVOIRE = "Cote d'Ivoire"
    CROATIA = "Croatia"
    CUBA = "Cuba"
    CURACAO = "Curacao"
    CZECHIA = "Czechia"
    CZECHOSLOVAKIA = "Czechoslovakia"
    NORTH_KOREA = "Democratic People's Republic of Korea"
    CONGO_DR = "Democratic Republic of the Congo"
    DENMARK = "Denmark"
    DJIBOUTI = "Djibouti"
    DOMINICA = "Dominica"
    DOMINICAN_REPUBLIC = "Dominican Republic"
    ECUADOR = "Ecuador"
    EGYPT = "Egypt"
    EL_SALVADOR = "El Salvador"
    EQUATORIAL_GUINEA = "Equatorial Guinea"
    ERITREA = "Eritrea"
    ESTONIA = "Estonia"
    ETHIOPIA = "Ethiopia"
    ETHIOPIA_PDR = "Ethiopia PDR"
    FALKLAND_ISLANDS = "Falkland Islands (Malvinas)"
    FAROE_ISLANDS = "Faroe Islands"
    FIJI = "Fiji"
    FINLAND = "Finland"
    FRANCE = "France"
    FRENCH_GUIANA = "French Guiana"
    FRENCH_POLYNESIA = "French Polynesia"
    GABON = "Gabon"
    GAMBIA = "Gambia"
    GEORGIA = "Georgia"
    GERMANY = "Germany"

    # FAOSTAT refers to West Germany as "Germany fr".
    WEST_GERMANY = "West Germany"
    # East Germany has a country name of Germany Nl in the FAOSTAT
    # standards and definitions.
    EAST_GERMANY = "East Germany"

    GHANA = "Ghana"
    GIBRALTAR = "Gibraltar"
    GREECE = "Greece"
    GREENLAND = "Greenland"
    GRENADA = "Grenada"
    GUADELOUPE = "Guadeloupe"
    GUAM = "Guam"
    GUATEMALA = "Guatemala"
    GUINEA = "Guinea"
    GUINEA_BISSAU = "Guinea-Bissau"
    GUYANA = "Guyana"
    HAITI = "Haiti"
    HONDURAS = "Honduras"
    HUNGARY = "Hungary"
    INDIA = "India"
    INDONESIA = "Indonesia"
    IRAN = "Iran (Islamic Republic of)"
    IRAQ = "Iraq"
    IRELAND = "Ireland"
    ISRAEL = "Israel"
    ITALY = "Italy"
    JAMAICA = "Jamaica"
    JAPAN = "Japan"
    JORDAN = "Jordan"
    KAZAKHSTAN = "Kazakhstan"
    KENYA = "Kenya"
    KIRIBATI = "Kiribati"
    KOSOVO = "Kosovo"
    KUWAIT = "Kuwait"
    KYRGYZSTAN = "Kyrgyzstan"
    LAOS = "Lao People's Democratic Republic"
    LATVIA = "Latvia"
    LEBANON = "Lebanon"
    LESOTHO = "Lesotho"
    LIBERIA = "Liberia"
    LIBYA = "Libya"
    LIECNTENSTEIN = "Liechtenstein"
    LITHUANIA = "Lithuania"
    LUXEMBOURG = "Luxembourg"
    MADAGASCAR = "Madagascar"
    MALAWI = "Malawi"
    MALAYSIA = "Malaysia"
    MALDIVES = "Maldives"
    MALI = "Mali"
    MALTA = "Malta"
    MAURITANIA = "Mauritania"
    MAURITIUS = "Mauritius"
    MEXICO = "Mexico"
    MONGOLIA = "Mongolia"
    MONTENEGRO = "Montenegro"
    MOROCCO = "Morocco"
    MOZAMBIQUE = "Mozambique"
    MYANMAR = "Myanmar"
    NAMIBIA = "Namibia"
    NEPAL = "Nepal"
    NETHERLANDS = "Netherlands"
    NETHERLANDS_ANTILLES = "Netherlands Antilles"
    NEW_CALEDONIA = "New Caledonia"
    NEW_ZEALAND = "New Zealand"
    NICARAGUA = "Nicaragua"
    NIGER = "Niger"
    NIGERIA = "Nigeria"
    NORWAY = "Norway"
    OMAN = "Oman"
    PAKISTAN = "Pakistan"
    PANAMA = "Panama"
    PAPUA_NEW_GUINEA = "Papua New Guinea"
    PARAGUAY = "Paraguay"
    PERU = "Peru"
    PHILIPPINES = "Philippines"
    POLAND = "Poland"
    PORTUGAL = "Portugal"
    PUERTO_RICO = "Puerto Rico"
    QATAR = "Qatar"
    SOUTH_KOREA = "Republic of Korea"
    MOLDOVA = "Republic of Moldova"
    REUNION = "Reunion"
    ROMANIA = "Romania"
    RUSSIA = "Russian Federation"
    RWANDA = "Rwanda"
    SAINT_KITTS_AND_NEVIS = "Saint Kitts and Nevis"
    SAINT_LUCIA = "Saint Lucia"
    SAINT_VINCENT_AND_THE_GRENADINES = "Saint Vincent and the Grenadines"
    SAMOA = "Samoa"
    SAO_TOME_AND_PRINCIPE = "Sao Tome and Principe"
    SAUDI_ARABIA = "Saudi Arabia"
    SENEGAL = "Senegal"
    SERBIA = "Serbia"
    SERBIA_AND_MONTENEGRO = "Serbia and Montenegro"
    SEYCHELLES = "Seychelles"
    SIERRA_LEONE = "Sierra Leone"
    SINGAPORE = "Singapore"
    SLOVAKIA = "Slovakia"
    SLOVENIA = "Slovenia"
    SOLOMON_ISLANDS = "Solomon Islands"
    SOMALIA = "Somalia"
    SOUTH_AFRICA = "South Africa"
    SOUTH_SUDAN = "South Sudan"
    SPAIN = "Spain"
    SRI_LANKA = "Sri Lanka"
    SUDAN = "Sudan"
    SUDAN_FORMER = "Sudan (former)"
    SURINAME = "Suriname"
    SWAZILAND = "Swaziland"
    SWEDEN = "Sweden"
    SWITZERLAND = "Switzerland"
    SYRIA = "Syrian Arab Republic"
    TAJIKISTAN = "Tajikistan"
    THAILAND = "Thailand"
    MACEDONIA = "The former Yugoslav Republic of Macedonia"
    TIMOR_LESTE = "Timor-Leste"
    TOGO = "Togo"
    TRINIDAD_AND_TOBAGO = "Trinidad and Tobago"
    TUNISIA = "Tunisia"
    TURKEY = "Turkey"
    TURKMENISTAN = "Turkmenistan"
    UGANDA = "Uganda"
    UKRAINE = "Ukraine"
    UNITED_ARAB_EMIRATES = "United Arab Emirates"
    UNITED_KINGDOM = "United Kingdom"
    TANZANIA = "United Republic of Tanzania"
    USA = "United States of America"
    URUGUAY = "Uruguay"
    USSR = "USSR"
    UZBEKISTAN = "Uzbekistan"
    VENEZUELA = "Venezuela (Bolivarian Republic of)"
    VIETNAM = "Viet Nam"
    YEMEN = "Yemen"
    # Yemen Arab Republic aka North Yemen.
    NORTH_YEMEN = "Yemen Ar Rp"
    # Democratic Republic of Yemen aka South Yemen.
    SOUTH_YEMEN = "South Yemen"
    VANUATU = "Vanuatu"
    # Socialist Federal Republic of Yugoslavia.
    # The Yugoslavia of 1945-1992.
    YUGOSLAVIA = "Yugoslav SFR"
    ZAMBIA = "Zambia"
    ZIMBABWE = "Zimbabwe"

    # USDA PSD Derived effayoh political entities.
    OTHER = "Other"
    CYPRUS = "Cyprus"
    EU_15 = "EU-15"
    EU_25 = "EU-25"
    EU = "European Union"
    ICELAND = "Iceland"
    # The name of present-day Djibouti between 1967 and 1977.
    FTAI = "Fr.Ter.Africa-Issas"
    # From Wikipedia: French Equatorial Africa (AEF) was the federation
    # of French colonial possessions in Central Africa which comprised
    # present-day: Chad, Central African Republic, Cameroon, the
    # Republic of Congo and Gabon.
    FRENCH_EQUATORIAL_AFRICA = "French Equatorial Africa"
    # Well this is very interesting to find in the USDA PSD countries.
    NORTH_VIETNAM = "North Vietnam"
    SOUTH_VIETNAM = "South Vietnam"
    # Western Sahara is a disputed territory between Morocco and Sahrawi
    # nationalists. It breaks the 500,000 population threshold. We
    # include it here for possible combination with Morocco since it is
    # partially occupied by Morocco.
    WESTERN_SAHARA = "Western Sahara"
    # Yugoslavia from 2001-2006
    YUGOSLAVIA_GT_01 = "Yugoslavia (>01/2001)"
    # Yugoslavia from 1992-2000
    YUGOSLAVIA_GT_92 = "Yugoslavia (>05/92)"
    # Ryukyu Islands
    RYUKYU = "Ryukyu Islands/Nansei Islands"


effpent_to_iso = {
    FAOPolitEnt.AFGHANISTAN: "AFG",
    #ALAND_ISLANDS: ,
    FAOPolitEnt.ALBANIA: "ALB",
    FAOPolitEnt.ALGERIA: "DZA",
    FAOPolitEnt.ANDORRA: "AND",
    FAOPolitEnt.ANGOLA: "AGO",
    #ANGUILLA: ,
    #ANTARCTICA: ,
    FAOPolitEnt.ANTIGUA_AND_BARBUDA: "ATG",
    FAOPolitEnt.ARGENTINA: "ARG",
    FAOPolitEnt.ARMENIA: "ARM",
    #ARUBA: ,
    FAOPolitEnt.AUSTRALIA: "AUS",
    FAOPolitEnt.AUSTRIA: "AUT",
    FAOPolitEnt.AZERBAIJAN: "AZE",
    FAOPolitEnt.BAHAMAS: "BHS",
    FAOPolitEnt.BAHRAIN: "BHR",
    FAOPolitEnt.BANGLADESH: "BGD",
    FAOPolitEnt.BARBADOS: "BRB",
    FAOPolitEnt.BELARUS: "BLR",
    FAOPolitEnt.BELGIUM: "BEL",
    #BELGIUM_LUXEMBOURG: ,
    FAOPolitEnt.BELIZE: "BLZ",
    FAOPolitEnt.BENIN: "BEN",
    #BERMUDA: ,
    FAOPolitEnt.BHUTAN: "BTN",
    FAOPolitEnt.BOLIVIA: "BOL",
    FAOPolitEnt.BOSNIA_AND_HERZEGOVINA: "BIH",
    FAOPolitEnt.BOTSWANA: "BWA",
    #BOUVET_ISLAND: ,
    FAOPolitEnt.BRAZIL: "BRA",
    #BRITISH_INDIAN_OCEAN_TERRITORY: ,
    FAOPolitEnt.BRUNEI_DARUSSALAM: "BRN",
    FAOPolitEnt.BULGARIA: "BGR",
    FAOPolitEnt.BURKINA_FASO: "BFA",
    FAOPolitEnt.BURUNDI: "BDI",
    FAOPolitEnt.CABO_VERDE: "CPV",
    FAOPolitEnt.CAMBODIA: "KHM",
    FAOPolitEnt.CAMEROON: "CMR",
    FAOPolitEnt.CANADA: "CAN",
    #CARIBBEAN: ,
    #CAYMAN_ISLANDS: ,
    FAOPolitEnt.CENTRAL_AFRICAN_REPUBLIC: "CAF",
    FAOPolitEnt.CHAD: "TCD",
    #CHANNEL_ISLANDS: ,
    FAOPolitEnt.CHILE: "CHL",
    FAOPolitEnt.CHINA: "CHN",
    #CHINA_EXC_HK_MACAO: ,
    #CHINA_HK_SAR: ,
    #CHINA_MACAO_SAR: ,
    #CHINA_MAINLAND: ,
    #CHINA_TAIWAN: ,
    #CHRISTMAS_ISLAND: ,
    #COCOS: ,
    FAOPolitEnt.COLOMBIA: "COL",
    FAOPolitEnt.COMOROS: "COM",
    FAOPolitEnt.CONGO: "COG",
    FAOPolitEnt.COOK_ISLANDS: "COK",
    FAOPolitEnt.COSTA_RICA: "CRI",
    FAOPolitEnt.COTE_DIVOIRE: "CIV",
    FAOPolitEnt.CROATIA: "HRV",
    FAOPolitEnt.CUBA: "CUB",
    #CURACAO: ,
    FAOPolitEnt.CZECHIA: "CZE",
    #CZECHOSLOVAKIA: ,
    FAOPolitEnt.NORTH_KOREA: "PRK",
    FAOPolitEnt.CONGO_DR: "COD",
    FAOPolitEnt.DENMARK: "DNK",
    FAOPolitEnt.DJIBOUTI: "DJI",
    FAOPolitEnt.DOMINICA: "DMA",
    FAOPolitEnt.DOMINICAN_REPUBLIC: "DOM",
    FAOPolitEnt.ECUADOR: "ECU",
    FAOPolitEnt.EGYPT: "EGY",
    FAOPolitEnt.EL_SALVADOR: "SLV",
    FAOPolitEnt.EQUATORIAL_GUINEA: "GNQ",
    FAOPolitEnt.ERITREA: "ERI",
    FAOPolitEnt.ESTONIA: "EST",
    #ETHIOPIA: ,
    FAOPolitEnt.ETHIOPIA_PDR: "ETH",
    #FALKLAND_ISLANDS: ,
    FAOPolitEnt.FAROE_ISLANDS: "FRO",
    FAOPolitEnt.FIJI: "FJI",
    FAOPolitEnt.FINLAND: "FIN",
    FAOPolitEnt.FRANCE: "FRA",
    #FRENCH_GUIANA: ,
    #FRENCH_POLYNESIA: ,
    FAOPolitEnt.GABON: "GAB",
    FAOPolitEnt.GAMBIA: "GMB",
    FAOPolitEnt.GEORGIA: "GEO",
    FAOPolitEnt.GERMANY: "DEU",
    #WEST_GERMANY: ,
    #EAST_GERMANY: ,
    FAOPolitEnt.GHANA: "GHA",
    #GIBRALTAR: ,
    FAOPolitEnt.GREECE: "GRC",
    #GREENLAND: ,
    FAOPolitEnt.GRENADA: "GRD",
    #GUADELOUPE: ,
    #GUAM: ,
    FAOPolitEnt.GUATEMALA: "GTM",
    FAOPolitEnt.GUINEA: "GIN",
    FAOPolitEnt.GUINEA_BISSAU: "GNB",
    FAOPolitEnt.GUYANA: "GUY",
    FAOPolitEnt.HAITI: "HTI",
    FAOPolitEnt.HONDURAS: "HND",
    FAOPolitEnt.HUNGARY: "HUN",
    FAOPolitEnt.INDIA: "IND",
    FAOPolitEnt.INDONESIA: "IDN",
    FAOPolitEnt.IRAN: "IRN",
    FAOPolitEnt.IRAQ: "IRQ",
    FAOPolitEnt.IRELAND: "IRL",
    FAOPolitEnt.ISRAEL: "ISR",
    FAOPolitEnt.ITALY: "ITA",
    FAOPolitEnt.JAMAICA: "JAM",
    FAOPolitEnt.JAPAN: "JPN",
    FAOPolitEnt.JORDAN: "JOR",
    FAOPolitEnt.KAZAKHSTAN: "KAZ",
    FAOPolitEnt.KENYA: "KEN",
    FAOPolitEnt.KIRIBATI: "KIR",
    #KOSOVO: ,
    FAOPolitEnt.KUWAIT: "KWT",
    FAOPolitEnt.KYRGYZSTAN: "KGZ",
    FAOPolitEnt.LAOS: "LAO",
    FAOPolitEnt.LATVIA: "LVA",
    FAOPolitEnt.LEBANON: "LBN",
    FAOPolitEnt.LESOTHO: "LSO",
    FAOPolitEnt.LIBERIA: "LBR",
    FAOPolitEnt.LIBYA: "LBY",
    #LIECNTENSTEIN: ,
    FAOPolitEnt.LITHUANIA: "LTU",
    FAOPolitEnt.LUXEMBOURG: "LUX",
    FAOPolitEnt.MADAGASCAR: "MDG",
    FAOPolitEnt.MALAWI: "MWI",
    FAOPolitEnt.MALAYSIA: "MYS",
    FAOPolitEnt.MALDIVES: "MDV",
    FAOPolitEnt.MALI: "MLI",
    FAOPolitEnt.MALTA: "MLT",
    FAOPolitEnt.MAURITANIA: "MRT",
    FAOPolitEnt.MAURITIUS: "MUS",
    FAOPolitEnt.MEXICO: "MEX",
    FAOPolitEnt.MONGOLIA: "MNG",
    FAOPolitEnt.MONTENEGRO: "MNE",
    FAOPolitEnt.MOROCCO: "MAR",
    FAOPolitEnt.MOZAMBIQUE: "MOZ",
    FAOPolitEnt.MYANMAR: "MMR",
    FAOPolitEnt.NAMIBIA: "NAM",
    FAOPolitEnt.NEPAL: "NPL",
    FAOPolitEnt.NETHERLANDS: "NLD",
    #NETHERLANDS_ANTILLES: ,
    #NEW_CALEDONIA: ,
    FAOPolitEnt.NEW_ZEALAND: "NZL",
    FAOPolitEnt.NICARAGUA: "NIC",
    FAOPolitEnt.NIGER: "NER",
    FAOPolitEnt.NIGERIA: "NGA",
    FAOPolitEnt.NORWAY: "NOR",
    FAOPolitEnt.OMAN: "OMN",
    FAOPolitEnt.PAKISTAN: "PAK",
    FAOPolitEnt.PANAMA: "PAN",
    FAOPolitEnt.PAPUA_NEW_GUINEA: "PNG",
    FAOPolitEnt.PARAGUAY: "PRY",
    FAOPolitEnt.PERU: "PER",
    FAOPolitEnt.PHILIPPINES: "PHL",
    FAOPolitEnt.POLAND: "POL",
    FAOPolitEnt.PORTUGAL: "PRT",
    #PUERTO_RICO: ,
    FAOPolitEnt.QATAR: "QAT",
    FAOPolitEnt.SOUTH_KOREA: "KOR",
    FAOPolitEnt.MOLDOVA: "MDA",
    #REUNION: ,
    FAOPolitEnt.ROMANIA: "ROU",
    FAOPolitEnt.RUSSIA: "RUS",
    FAOPolitEnt.RWANDA: "RWA",
    FAOPolitEnt.SAINT_KITTS_AND_NEVIS: "KNA",
    FAOPolitEnt.SAINT_LUCIA: "LCA",
    FAOPolitEnt.SAINT_VINCENT_AND_THE_GRENADINES: "VCT",
    FAOPolitEnt.SAMOA: "WSM",
    FAOPolitEnt.SAO_TOME_AND_PRINCIPE: "STP",
    FAOPolitEnt.SAUDI_ARABIA: "SAU",
    FAOPolitEnt.SENEGAL: "SEN",
    FAOPolitEnt.SERBIA: "SRB",
    #SERBIA_AND_MONTENEGRO: ,
    FAOPolitEnt.SEYCHELLES: "SYC",
    FAOPolitEnt.SIERRA_LEONE: "SLE",
    FAOPolitEnt.SINGAPORE: "SGP",
    FAOPolitEnt.SLOVAKIA: "SVK",
    FAOPolitEnt.SLOVENIA: "SVN",
    FAOPolitEnt.SOLOMON_ISLANDS: "SLB",
    FAOPolitEnt.SOMALIA: "SOM",
    FAOPolitEnt.SOUTH_AFRICA: "ZAF",
    FAOPolitEnt.SOUTH_SUDAN: "SSD",
    FAOPolitEnt.SPAIN: "ESP",
    FAOPolitEnt.SRI_LANKA: "LKA",
    FAOPolitEnt.SUDAN: "SDN",
    #SUDAN_FORMER: ,
    FAOPolitEnt.SURINAME: "SUR",
    FAOPolitEnt.SWAZILAND: "SWZ",
    FAOPolitEnt.SWEDEN: "SWE",
    FAOPolitEnt.SWITZERLAND: "CHE",
    FAOPolitEnt.SYRIA: "SYR",
    FAOPolitEnt.TAJIKISTAN: "TJK",
    FAOPolitEnt.THAILAND: "THA",
    FAOPolitEnt.MACEDONIA: "MKD",
    FAOPolitEnt.TIMOR_LESTE: "TLS",
    FAOPolitEnt.TOGO: "TGO",
    FAOPolitEnt.TRINIDAD_AND_TOBAGO: "TTO",
    FAOPolitEnt.TUNISIA: "TUN",
    FAOPolitEnt.TURKEY: "TUR",
    FAOPolitEnt.TURKMENISTAN: "TKM",
    FAOPolitEnt.UGANDA: "UGA",
    FAOPolitEnt.UKRAINE: "UKR",
    FAOPolitEnt.UNITED_ARAB_EMIRATES: "ARE",
    FAOPolitEnt.UNITED_KINGDOM: "GBR",
    FAOPolitEnt.TANZANIA: "TZA",
    FAOPolitEnt.USA: "USA",
    FAOPolitEnt.URUGUAY: "URY",
    #USSR: ,
    FAOPolitEnt.UZBEKISTAN: "UZB",
    FAOPolitEnt.VENEZUELA: "VEN",
    FAOPolitEnt.VIETNAM: "VNM",
    FAOPolitEnt.YEMEN: "YEM",
    #NORTH_YEMEN: ,
    #SOUTH_YEMEN: ,
    #VANUATU: ,
    #YUGOSLAVIA: ,
    FAOPolitEnt.ZAMBIA: "ZMB",
    FAOPolitEnt.ZIMBABWE: "ZWE",
#    OTHER: ,
#    CYPRUS: ,
#    EU_15: ,
#    EU_25: ,
#    EU: ,
#    ICELAND: ,
#    FTAI: ,
#    FRENCH_EQUATORIAL_AFRICA: ,
#    NORTH_VIETNAM: ,
#    SOUTH_VIETNAM: ,
#    WESTERN_SAHARA: ,
#    YUGOSLAVIA_GT_01: ,
#    YUGOSLAVIA_GT_92: ,
#    RYUKYU: ,
}

iso_to_effpent = {value: key for key, value in effpent_to_iso.items()}

effpent_name_to_iso = {key.name: value for key, value in effpent_to_iso.items()}
effpent_iso_to_name = {value:key.name for key, value in effpent_to_iso.items()}