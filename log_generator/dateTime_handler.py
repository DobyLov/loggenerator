""" Gestionnnaire de date """

from datetime import datetime, date, timedelta

# Retourne la date et l heure
def get_dateNow():    
    my_dateTimeNow = datetime.now()
    my_years = str(my_dateTimeNow.year)
    my_months = addZero(str(my_dateTimeNow.month))
    my_days = addZero(str(my_dateTimeNow.day))
    my_hours = addZero(str(my_dateTimeNow.hour))
    my_minutes = addZero(str(my_dateTimeNow.minute))
    my_seconds = addZero(str(my_dateTimeNow.second))
    my_concatened_dateNow: str = my_years + "-" + my_months + "-" + my_days + "T" + my_hours + ":" + my_minutes + ":" + my_seconds
    
    return my_concatened_dateNow

# Ajoute 0 devant les unitees ( jours et mois )
def addZero(mystr: str):
    if len(mystr) == 1:
        zeroBeforeValue = mystr.zfill(2)
    else:
        zeroBeforeValue = mystr
    
    return zeroBeforeValue

# retourne
#def set_dateTime_start_end_script():
#    #global script_start_dateTime, script_end_dateTime
#    return get_dateNow()

# Calcule le temp ecoulé d'execution du script
def calculat_elapsed_time(datetime_end, datetime_start):

    return datetime.fromisoformat(datetime_end) - datetime.fromisoformat(datetime_start)