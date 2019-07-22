from flask import current_app
from functools import reduce
import datetime
import calendar
import pytz

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)

def end_of_the_day(any_day):
    return any_day.replace(hour=23, minute=59, second=59, microsecond=999999)

def start_of_the_day(any_day):
    return any_day.replace(hour=0, minute=0, second=0, microsecond=0)

def on_inserted_records(items):
    dates = []
    for x in items:
        if not x['date'] in dates:
            dates.append(x['date'])
    for x in dates:
        recalculate_balance(x)

def on_replaced_records(item, original):
    recalculate_balance(item.date)

def on_updated_records(updates, original):
    dates = []
    for x in updates:
         if not x['date'] in dates:
            dates.append(x['date'])
    for x in dates:
        recalculate_balance(x)

def on_deleted_item_records(item):
    recalculate_balance(item.date)

def recalculate_balance(date):
    utc=pytz.UTC
    current_user = current_app.auth.get_request_auth_value()
    first_day = utc.localize(start_of_the_day(date.replace(day = 1)))
    last_day = utc.localize(end_of_the_day(last_day_of_month(date)))

    records = current_app.data.driver.db['records']
    current_records = [record for record in records.find({'account_id' : current_user, 
                                                            'date' : { '$gte' : first_day,
                                                                        '$lt' : last_day}})]

    print(current_records)

    total_income = sum([record['amount'] for record in current_records if record['recordtype'] == income])
    total_days = calendar.monthrange(date.year, date.month)[1]
    day_limit = round(total_income / total_days, 2)

    balance_records = current_app.data.driver.db['balance']
    balance_records.delete_many({})
    balance_records.delete_many({'account_id' : current_user,
                                    'date' : { '$gte' : first_day,
                                                '$lt' : last_day}},)
    current_day = first_day
    last_day_balance = 0
    new_balance_records = []
    while current_day < last_day:
        print(current_day, end_of_the_day(current_day))
        day_records = [record for record in current_records if record['date'] >= current_day and record['date'] <= end_of_the_day(current_day)]
        day_income = sum([record['amount'] for record in day_records if record['recordtype'] == income])
        day_expenses = sum([record['amount'] for record in day_records if record['recordtype'] == expenses])
        day_balance = day_limit + last_day_balance - day_expenses
        current_balance_record = {
                                    'account_id' : current_user,
                                    'date' : current_day,
                                    'income' : day_income,
                                    'expenses' : day_expenses,
                                    'balance' : day_balance
                                }
        new_balance_records.append(current_balance_record)
        last_day_balance = day_balance
        current_day += datetime.timedelta(days=1)
        print(current_day)
        print(current_balance_record)
    balance_records.insert_many(new_balance_records)

income = 'income'
expenses = 'expenses'