import re
import pandas as pd
from datetime import datetime
import calendar


def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:PM|AM)\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Creating a pandas data frame
    df = pd.DataFrame({'user_message': messages, "message_date": dates})

    # Converting the Dates to a datetime format
    for i in range(0, len(df)):
        dt = df["message_date"][i]
        nd = datetime.strptime(dt, "%m/%d/%y, %I:%M %p - ")
        df["message_date"][i] = nd

    df.rename(columns={'message_date': 'date'}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        # if username exists
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    # def custom_date_field(field):
    #     lst = []
    #     for dat in df['date']:
    #         if (field == "month"):
    #             lst.append(calendar.month_name[dat.month])
    #         elif (field == "month_num"):
    #             lst.append(dat.month)
    #         elif (field == "year"):
    #             lst.append(dat.year)
    #         elif (field == "day"):
    #             lst.append(dat.day)
    #         elif (field == "hour"):
    #             lst.append(dat.hour)
    #         elif (field == "minute"):
    #             lst.append(dat.minute)
    #         elif (field == "date"):
    #             lst.append(dat.date())
    #         else:
    #             return "Wrong Field"
    #     return lst
    #
    # df['only_date'] = custom_date_field("date")
    # df['year'] = custom_date_field("year")
    # df['month_num'] = custom_date_field("month_num")
    # df['month'] = custom_date_field("month")
    # df['day'] = custom_date_field("day")
    # df['hour'] = custom_date_field("hour")
    # df['minute'] = custom_date_field("minute")

    df['only_date'] = df["date"].dt.date
    df['year'] = df["date"].dt.year
    df['month_num'] = df["date"].dt.month
    df['month'] = df["date"].dt.month_name()
    df['day'] = df["date"].dt.day
    df['day_name'] = df["date"].dt.day_name()
    df['hour'] = df["date"].dt.hour
    df['minute'] = df["date"].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(hour) + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period

    return df
