states =[{"name": "Alabama", "cities": ["Birmingham", "Montgomery", "Mobile", "Huntsville", "Tuscaloosa", "Hoover", "Dothan", "Auburn", "Decatur", "Madison", "Florence", "Gadsden", "Vestavia Hills", "Prattville", "Phenix City", "Alabaster", "Bessemer", "Enterprise", "Opelika", "Homewood"]},
    {"name": "Alaska", "cities": ["Anchorage", "Fairbanks", "Juneau", "Sitka", "Ketchikan", "Wasilla", "Kenai", "Kodiak", "Bethel", "Palmer", "Homer", "Unalaska", "Barrow", "Valdez", "Nome", "Soldotna", "Dillingham", "Seward", "North Pole", "Houston"]},
    {"name": "Arizona", "cities": ["Phoenix", "Tucson", "Mesa", "Chandler", "Glendale", "Scottsdale", "Gilbert", "Tempe", "Peoria", "Surprise", "Yuma", "Avondale", "Goodyear", "Flagstaff", "Buckeye", "Lake Havasu City", "Casa Grande", "Maricopa", "Sierra Vista", "Oro Valley"]},
    {"name": "Arkansas", "cities": ["Little Rock", "Fort Smith", "Fayetteville", "Springdale", "Jonesboro", "North Little Rock", "Conway", "Rogers", "Bentonville", "Benton", "Pine Bluff", "Hot Springs", "Blytheville", "Sherwood", "Texarkana", "Russellville", "Paragould", "West Memphis", "Van Buren", "Searcy"]},
    {"name": "California", "cities": ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno", "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Anaheim", "Santa Ana", "Riverside", "Stockton", "Chula Vista", "Irvine", "Fremont", "San Bernardino", "Modesto", "Fontana", "Santa Clarita"]},
    {"name": "Colorado", "cities": ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood", "Thornton", "Arvada", "Westminster", "Pueblo", "Centennial", "Boulder", "Greeley", "Longmont", "Loveland", "Broomfield", "Grand Junction", "Castle Rock", "Commerce City", "Littleton", "Northglenn"]},
    {"name": "Connecticut", "cities": ["Bridgeport", "New Haven", "Stamford", "Hartford", "Waterbury", "Norwalk", "Danbury", "New Britain", "Bristol", "Meriden", "Milford", "West Haven", "Middletown", "Shelton", "Norwich", "Torrington", "Naugatuck", "New London", "Ansonia", "Derby"]},
    {"name": "Delaware", "cities": ["Wilmington", "Dover", "Newark", "Middletown", "Smyrna", "Milford", "Seaford", "Georgetown", "Elsmere", "New Castle", "Millsboro", "Laurel", "Harrington", "Camden", "Clayton", "Lewes", "Milton", "Rehoboth Beach", "Felton", "Delaware City"]},
    {"name": "Florida", "cities": ["Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg", "Hialeah", "Tallahassee", "Fort Lauderdale", "Port St. Lucie", "Cape Coral", "Pembroke Pines", "Hollywood", "Miramar", "Gainesville", "Coral Springs", "Miami Gardens", "Clearwater", "Palm Bay", "Pompano Beach", "West Palm Beach"]},
    {"name": "Georgia", "cities": ["Atlanta", "Augusta", "Columbus", "Macon", "Savannah", "Athens", "Roswell", "Albany", "Johns Creek", "Warner Robins", "Valdosta", "Smyrna", "Brookhaven", "Dunwoody", "Peachtree Corners", "Mableton", "Gainesville", "Milton", "Newnan", "Rome"]},
    {"name": "Hawaii", "cities": ["Honolulu", "East Honolulu", "Pearl City", "Hilo", "Kailua", "Waipahu", "Kaneohe", "Mililani Town", "Kahului", "Ewa Gentry", "Kihei", "Makakilo", "Wahiawa", "Schofield Barracks", "Wailuku", "Waianae", "Kapaa", "Lahaina", "Aiea", "Holualoa"]},
    {"name": "Idaho", "cities": ["Boise", "Meridian", "Nampa", "Idaho Falls", "Pocatello", "Caldwell", "Coeur d'Alene", "Twin Falls", "Lewiston", "Post Falls", "Rexburg", "Moscow", "Eagle", "Kuna", "Ammon", "Chubbuck", "Hayden", "Mountain Home", "Blackfoot", "Middleton"]},
    {"name": "Illinois", "cities": ["Chicago", "Aurora", "Rockford", "Joliet", "Naperville", "Springfield", "Peoria", "Elgin", "Waukegan", "Cicero", "Champaign", "Bloomington", "Arlington Heights", "Evanston", "Decatur", "Schaumburg", "Bolingbrook", "Palatine", "Skokie", "Des Plaines"]},
    {"name": "Indiana", "cities": ["Indianapolis", "Fort Wayne", "Evansville", "South Bend", "Carmel", "Bloomington", "Fishers", "Hammond", "Gary", "Muncie", "Lafayette", "Terre Haute", "Anderson", "Noblesville", "Greenwood", "Kokomo", "Elkhart", "Mishawaka", "Lawrence", "West Lafayette"]},
    {"name": "Iowa", "cities": ["Des Moines", "Cedar Rapids", "Davenport", "Sioux City", "Iowa City", "Waterloo", "Ames", "Ankeny", "Dubuque", "Council Bluffs", "West Des Moines", "Urbandale", "Coralville", "Marion", "Bettendorf", "Mason City", "Marshalltown", "Clinton", "Fort Dodge", "Johnston"]},
    {"name": "Kansas", "cities": ["Wichita", "Overland Park", "Kansas City", "Olathe", "Topeka", "Lawrence", "Shawnee", "Manhattan", "Lenexa", "Salina", "Hutchinson", "Leavenworth", "Leawood", "Garden City", "Emporia", "Derby", "Junction City", "Prairie Village", "Gardner", "Pittsburg"]},
    {"name": "Kentucky", "cities": ["Louisville", "Lexington", "Bowling Green", "Owensboro", "Covington", "Richmond", "Georgetown", "Florence", "Elizabethtown", "Nicholasville", "Henderson", "Frankfort", "Jeffersontown", "Paducah", "Radcliff", "Ashland", "Mount Washington", "Shively", "Madisonville", "Winchester"]},
    {"name": "Louisiana", "cities": ["New Orleans", "Baton Rouge", "Shreveport", "Lafayette", "Lake Charles", "Kenner", "Bossier City", "Monroe", "Alexandria", "Houma", "Marrero", "New Iberia", "Central", "Slidell", "Ruston", "Hammond", "Sulphur", "Natchitoches", "Gretna", "Opelousas"]},
    {"name": "Maine", "cities": ["Portland", "Lewiston", "Bangor", "South Portland", "Auburn", "Biddeford", "Augusta", "Saco", "Westbrook", "Waterville", "Brunswick", "Windham", "Gorham", "Kennebunk", "Ellsworth", "Old Orchard Beach", "Bath", "Falmouth", "York", "Rockland"]},
    {"name": "Maryland", "cities": ["Baltimore", "Columbia", "Germantown", "Silver Spring", "Waldorf", "Frederick", "Ellicott City", "Dundalk", "Rockville", "Bethesda", "Gaithersburg", "Towson", "Bowie", "Aspen Hill", "Potomac", "Catonsville", "Bel Air South", "Essex", "Severn", "North Bethesda"]},
    {"name": "Massachusetts", "cities": ["Boston", "Worcester", "Springfield", "Lowell", "Cambridge", "New Bedford", "Brockton", "Quincy", "Lynn", "Fall River", "Newton", "Somerville", "Lawrence", "Framingham", "Waltham", "Haverhill", "Malden", "Medford", "Taunton", "Chicopee"]},
    {"name": "Michigan", "cities": ["Detroit", "Grand Rapids", "Warren", "Sterling Heights", "Ann Arbor", "Lansing", "Flint", "Dearborn", "Livonia", "Troy", "Farmington Hills", "Kalamazoo", "Wyoming", "Southfield", "Waterford", "Taylor", "Pontiac", "St. Clair Shores", "Royal Oak", "Novi"]},
    {"name": "Minnesota", "cities": ["Minneapolis", "St. Paul", "Rochester", "Duluth", "Bloomington", "Brooklyn Park", "Plymouth", "Maple Grove", "Woodbury", "St. Cloud", "Eagan", "Eden Prairie", "Coon Rapids", "Burnsville", "Minnetonka", "Apple Valley", "Blaine", "Lakeville", "Roseville", "Mankato"]},
    {"name": "Mississippi", "cities": ["Jackson", "Gulfport", "Southaven", "Hattiesburg", "Biloxi", "Meridian", "Tupelo", "Greenville", "Olive Branch", "Clinton", "Vicksburg", "Horn Lake", "Pearl", "Starkville", "Columbus", "Pascagoula", "Brandon", "Oxford", "Gautier", "Ocean Springs"]},
    {"name": "Missouri", "cities": ["Kansas City", "St. Louis", "Springfield", "Independence", "Columbia", "Lee's Summit", "O'Fallon", "St. Joseph", "St. Charles", "St. Peters", "Florissant", "Blue Springs", "Chesterfield", "Joplin", "Jefferson City", "Cape Girardeau", "University City", "Wildwood", "Liberty", "Ballwin"]},
    {"name": "Montana", "cities": ["Billings", "Missoula", "Great Falls", "Bozeman", "Helena", "Kalispell", "Butte-Silver Bow", "Anaconda-Deer Lodge County", "Miles City", "Belgrade", "Livingston", "Laurel", "Whitefish", "Lewistown", "Columbia Falls", "Polson", "Hamilton", "Dillon", "Hardin", "Glasgow"]},
    {"name": "Nebraska", "cities": ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney", "Fremont", "Hastings", "Norfolk", "North Platte", "Columbus", "Papillion", "La Vista", "Scottsbluff", "Beatrice", "South Sioux City", "Lexington", "Alliance", "Chadron", "Gering", "Blair"]},
    {"name": "Nevada", "cities": ["Las Vegas", "Henderson", "Reno", "North Las Vegas", "Sparks", "Carson City", "Elko", "Mesquite", "Boulder City", "Fernley", "Fallon", "Winnemucca", "West Wendover", "Ely", "Yerington", "Lovelock", "Wells", "Caliente", "Carlin", "Las Vegas Strip"]},
    {"name": "New Hampshire", "cities": ["Manchester", "Nashua", "Concord", "Derry", "Dover", "Rochester", "Salem", "Merrimack", "Keene", "Bedford", "Portsmouth", "Laconia", "Windham", "Claremont", "Lebanon", "Pelham", "Somersworth", "Durham", "Exeter", "Londonderry"]},
    {"name": "New Jersey", "cities": ["Newark", "Jersey City", "Paterson", "Elizabeth", "Trenton", "Camden", "Clifton", "East Orange", "Passaic", "Union City", "Bayonne", "Vineland", "New Brunswick", "Perth Amboy", "Westfield", "Summit", "Linden", "Hackensack", "Englewood", "Fort Lee"]},
    {"name": "New Mexico", "cities": ["Albuquerque", "Las Cruces", "Rio Rancho", "Santa Fe", "Roswell", "Farmington", "Hobbs", "Clovis", "Alamogordo", "Carlsbad", "Gallup", "Deming", "Los Lunas", "Chaparral", "Sunland Park", "Portales", "Artesia", "Lovington", "Belen", "Silver City"]},
    {"name": "New York", "cities": ["New York", "Buffalo", "Rochester", "Yonkers", "Syracuse", "Albany", "New Rochelle", "Mount Vernon", "Schenectady", "Utica", "White Plains", "Troy", "Niagara Falls", "Binghamton", "Long Beach", "Peekskill", "Glen Cove", "Lackawanna", "Middletown", "Johnstown"]},
    {"name": "North Carolina", "cities": ["Charlotte", "Raleigh", "Greensboro", "Durham", "Winston-Salem", "Fayetteville", "Cary", "Wilmington", "High Point", "Asheville", "Concord", "Gastonia", "Jacksonville", "Chapel Hill", "Rocky Mount", "Burlington", "Wilson", "Huntersville", "Kannapolis", "Apex"]},
    {"name": "North Dakota", "cities": ["Fargo", "Bismarck", "Grand Forks", "Minot", "West Fargo", "Mandan", "Dickinson", "Jamestown", "Williston", "Wahpeton", "Devils Lake", "Valley City", "Grafton", "Beulah", "Rugby", "Horace", "Hazen", "Lincoln", "Belcourt", "Grand Forks AFB"]},
    {"name": "Ohio", "cities": ["Columbus", "Cleveland", "Cincinnati", "Toledo", "Akron", "Dayton", "Parma", "Canton", "Youngstown", "Lorain", "Hamilton", "Springfield", "Kettering", "Elyria", "Middletown", "Lima", "Newark", "Euclid", "Cuyahoga Falls", "Dublin"]},
    {"name": "Oklahoma", "cities": ["Oklahoma City", "Tulsa", "Norman", "Broken Arrow", "Lawton", "Edmond", "Moore", "Midwest City", "Enid", "Stillwater", "Muskogee", "Bartlesville", "Shawnee", "Owasso", "Ardmore", "Ponca City", "Yukon", "El Reno", "Durant", "Jenks"]},
    {"name": "Oregon", "cities": ["Portland", "Eugene", "Salem", "Gresham", "Hillsboro", "Beaverton", "Bend", "Medford", "Springfield", "Corvallis", "Albany", "Tigard", "Lake Oswego", "Keizer", "Grants Pass", "McMinnville", "Oregon City", "Redmond", "Tualatin", "West Linn"]},
    {"name": "Pennsylvania", "cities": ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading", "Scranton", "Bethlehem", "Lancaster", "Levittown", "Altoona", "Harrisburg", "Wilkes-Barre", "York", "State College", "Norristown", "Chester", "Bensalem", "Williamsport", "Easton", "Hazleton"]},
    {"name": "Rhode Island", "cities": ["Providence", "Warwick", "Cranston", "Pawtucket", "East Providence", "Woonsocket", "Newport", "Central Falls", "North Providence", "Cumberland", "Coventry", "West Warwick", "Bristol", "Lincoln", "Smithfield", "Barrington", "East Greenwich", "Narragansett", "Scituate", "North Kingstown"]},
    {"name": "South Carolina", "cities": ["Columbia", "Charleston", "North Charleston", "Mount Pleasant", "Rock Hill", "Greenville", "Summerville", "Goose Creek", "Hilton Head Island", "Florence", "Spartanburg", "Sumter", "Myrtle Beach", "Aiken", "Anderson", "Mauldin", "Greenwood", "Hanahan", "Lancaster", "North Augusta"]},
    {"name": "South Dakota", "cities": ["Sioux Falls", "Rapid City", "Aberdeen", "Brookings", "Watertown", "Mitchell", "Yankton", "Pierre", "Huron", "Vermillion", "Spearfish", "Brandon", "Madison", "Sturgis", "Box Elder", "Belle Fourche", "Tea", "Dell Rapids", "Canton", "Hot Springs"]},
    {"name": "Tennessee", "cities": ["Nashville", "Memphis", "Knoxville", "Chattanooga", "Clarksville", "Murfreesboro", "Franklin", "Jackson", "Johnson City", "Bartlett", "Hendersonville", "Kingsport", "Collierville", "Cleveland", "Smyrna", "Germantown", "Columbia", "Spring Hill", "La Vergne", "Oak Ridge"]},
    {"name": "Texas", "cities": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth", "El Paso", "Arlington", "Corpus Christi", "Plano", "Laredo", "Lubbock", "Garland", "Irving", "Amarillo", "Grand Prairie", "Brownsville", "McKinney", "Frisco", "Pasadena", "Killeen"]},
    {"name": "Utah", "cities": ["Salt Lake City", "West Valley City", "Provo", "West Jordan", "Orem", "Sandy", "Ogden", "St. George", "Layton", "Taylorsville", "South Jordan", "Lehi", "Logan", "Murray", "Draper", "Riverton", "Roy", "Cedar City", "Spanish Fork", "Springville"]},
    {"name": "Vermont", "cities": ["Burlington", "Essex", "South Burlington", "Colchester", "Rutland", "Bennington", "Brattleboro", "Hartford", "Barre", "Williston", "Montpelier", "St. Albans", "Winooski", "St. Johnsbury", "Newport", "Morristown", "Swanton", "Lyndon", "Middlebury", "Waterbury"]},
    {"name": "Virginia", "cities": ["Virginia Beach", "Norfolk", "Chesapeake", "Richmond", "Arlington", "Newport News", "Hampton", "Alexandria", "Portsmouth", "Roanoke", "Suffolk", "Lynchburg", "Harrisonburg", "Leesburg", "Charlottesville", "Danville", "Manassas", "Blacksburg", "Colonial Heights", "Hopewell"]},
    {"name": "Washington", "cities": ["Seattle", "Spokane", "Tacoma", "Vancouver", "Bellevue", "Kent", "Everett", "Renton", "Yakima", "Federal Way", "Bellingham", "Kennewick", "Auburn", "Pasco", "Marysville", "Redmond", "Kirkland", "Lacey", "Olympia", "Sammamish"]},
    {"name": "Washington DC", "cities": ["Washington"]},
    {"name": "West Virginia", "cities": ["Charleston", "Huntington", "Parkersburg", "Morgantown", "Wheeling", "Weirton", "Fairmont", "Beckley", "Martinsburg", "Clarksburg", "South Charleston", "St. Albans", "Vienna", "Bluefield", "Moundsville", "Bridgeport", "Dunbar", "Oak Hill", "Elkins", "Nitro"]},
    {"name": "Wisconsin", "cities": ["Milwaukee", "Madison", "Green Bay", "Kenosha", "Racine", "Appleton", "Waukesha", "Eau Claire", "Oshkosh", "Janesville", "West Allis", "La Crosse", "Sheboygan", "Wausau", "Fond du Lac", "New Berlin", "Brookfield", "Manitowoc", "Greenfield", "Menomonee Falls"]},
    {"name": "Wyoming", "cities": ["Cheyenne", "Casper", "Laramie", "Gillette", "Rock Springs", "Sheridan", "Green River", "Evanston", "Riverton", "Jackson", "Cody", "Rawlins", "Lander", "Torrington", "Powell", "Douglas", "Worland", "Buffalo", "Wheatland", "Newcastle"]}
]
