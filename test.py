import re
message = "10-11"
agemin = int(re.search("\d\d(?=\-)", str(message)).group(0))
agemax = int(re.search("(?<=\-)\d\d", str(message)).group(0))