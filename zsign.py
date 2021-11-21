def zsign(daybirth):
    day = int(daybirth.split(".")[0])
    month = int(daybirth.split(".")[1])
    
    if (day>=21 and day<=31 and month==3) or( month==4 and day>=1 and day<=19):

        zz = "Овен"
        return zz

    elif (day>=20 and day<=30 and month==4) or( month==5 and day>=1 and day<=20):

        zz = "Телец"
        return zz

    elif (day>=21 and day<=31 and month==5) or( month==6 and day>=1 and day<=20):

        zz = "Близнецы"
        return zz

    elif (day>=21 and day<=30 and month==6) or( month==7 and day>=1 and day<=22):

        zz = "Рак"
        return zz

    elif (day>=23 and day<=31 and month==7) or( month==8 and day>=1 and day<=22):

        zz = "Лев"
        return zz

    elif (day>=23 and day<=31 and month==8) or( month==9 and day>=1 and day<=22):

        zz = "Дева"
        return zz

    elif (day>=23 and day<=30 and month==9) or( month==10 and day>=1 and day<=22):

        zz = "Весы"
        return zz

    elif (day>=23 and day<=31 and month==10) or( month==11 and day>=1 and day<=22):
        
        zz = "Скорпион"
        return zz

    elif (day>=23 and day<=30 and month==11) or( month==12 and day>=1 and day<=21):
        
        zz = "Стрелец"
        return zz

    elif (day>=22 and day<=31 and month==12) or( month==1 and day>=1 and day<=19):

        zz = "Козерог"
        return zz

    elif (day>=20 and day<=31 and month==1) or( month==2 and day>=1 and day<=18):

        zz = "Водолей"
        return zz

    elif (day>=19 and day<=29 and month==2) or( month==3 and day>=1 and day<=20):

        zz = "Рыбы"
        return zz

zsignmatch = {"Водолей": "Овен, Близнецы, Весы, Стрелец", "Рыбы": "Телец, Рак ,Дева, Скорпион, Козерог", "Овен": "Близнецы, Весы, Стрелец, Водолей", "Телец": "Рак, Скорпион, Лев, Рыбы, Козерог", "Близнецы": "Овен, Лев, Весы, Стрелец, Водолей", "Рак": "Телец, Лев, Козерог, Рыбы, Скорпион", "Лев": "Рак, Стрелец, Близнецы, Скорпион, Весы", "Дева": "Телец, Рак, Скорпион, Козерог, Рыба", "Весы": "Овен, Близнецы, Лев, Стрелец, Водолей", "Скорпион": "Телец, Рак, Дева, Лев, Козерог", "Стрелец": "Овен, Близнецы, Лев, Весы, Водолей", "Козерог": "Телец, Рак, Дева, Скорпион, Рыбы"}