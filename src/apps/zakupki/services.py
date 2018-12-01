from datetime import date, timedelta


def create_file_name(request_date: date, num: int):
    prev_date = request_date - timedelta(days=1)
    return f'notification_Tomskaja_obl_2018113000_{request_date:}00_{num:3}.xml.zip'
