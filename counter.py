import jdatetime
from datetime import datetime, timedelta


def get_date_str(konkur_date: jdatetime.date) -> str:
    target_gdate = konkur_date.togregorian()
    target_datetime = datetime(target_gdate.year, target_gdate.month, target_gdate.day, 0, 0, 0)
    now = datetime.now()

    delta = target_datetime - now

    if delta.total_seconds() > 0:
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        _date_str: str = f"{days} روز، {hours} ساعت، {minutes} دقیقه، {seconds} ثانیه باقی مانده است."
        
        return _date_str
    
    else:
        return 'زمان برگزاری گذشته است!'
    