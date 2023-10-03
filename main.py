# import calendar

# # Define the year and month for the calendar
# year = 2023
# month = 9

# # Create a TextCalendar object for the specified year and month
# cal = calendar.TextCalendar(calendar.MONDAY)  # You can choose the first day of the week (e.g., SUNDAY or MONDAY)

# # Generate and print the calendar for the specified month
# calendar_text = cal.formatmonth(year, month)
# print(calendar_text)


# import calendar
# year = 2020
# month = 2
# days_in_month = calendar.monthcalendar(year, month)
# days_list = [day for week in days_in_month for day in week if day != 0]

# print(days_in_month)

# import calendar

# from datetime import datetime, timedelta
# import json

# first object year: 2020
# first object month: 9
# first object day: 14
# last object year: 2025
# last object month: 9
# last object day: 14
# Define the begin and end dates
# begin_date = datetime(2020, 9, 14)
# end_date = datetime(2021, 8, 31)

# # Initialize the result list
# result = []

# # Loop through the years
# current_year = begin_date.year
# while current_year <= end_date.year:
#     year_data = {
#         "name": str(current_year),
#         "kirim": "mystring",
#         "chiqim": "mystring",
#         "months": []
#     }

#     # Loop through the months
#     current_month = 1 if current_year == begin_date.year else begin_date.month
#     while current_month <= 12 and (current_year < end_date.year or current_month <= end_date.month):
#         month_name = datetime(current_year, current_month, 1).strftime("%B").lower()
#         month_data = {
#             "name": month_name,
#             "kirim": 3210,
#             "chiqim": 5432,
#             "days": []
#         }

#         # Loop through the days in the month
#         current_day = 1 if current_year == begin_date.year and current_month == begin_date.month else 1
#         last_day = calendar.monthrange(current_year, current_month)[1]
#         while current_day <= last_day and (current_year < end_date.year or current_month < end_date.month or current_day <= end_date.day):
#             day_data = {
#                 "name": str(current_day),
#                 "kirim": 123,
#                 "chiqim": 543
#             }
#             month_data["days"].append(day_data)
#             current_day += 1

#         year_data["months"].append(month_data)
#         current_month += 1

#     result.append(year_data)
#     current_year += 1

# # Write the result to a JSON file
# with open('data.json', 'w') as json_file:
#     json.dump(result, json_file, indent=4)



# import calendar
# from datetime import datetime
# import json

# # Define the begin and end dates
# begin_date = datetime(2020, 9, 14)
# end_date = datetime(2021, 9, 14)

# # Initialize the result list
# result = []

# # Loop through the years
# current_year = begin_date.year
# while current_year <= end_date.year:
#     year_data = {
#         "name": str(current_year),
#         "kirim": "mystring",
#         "chiqim": "mystring",
#         "months": []
#     }

#     # Loop through the months
#     current_month = 1 if current_year == begin_date.year else begin_date.month
#     while (current_year < end_date.year or (current_year == end_date.year and current_month <= end_date.month)):
#         # Check if the current_month is greater than 12, reset to 1 for the next year
#         if current_month > 12:
#             current_month = 1
#             current_year += 1

#         month_name = datetime(current_year, current_month, 1).strftime("%B").lower()
#         month_data = {
#             "name": month_name,
#             "kirim": 3210,
#             "chiqim": 5432,
#             "days": []
#         }

#         # Loop through the days in the month
#         current_day = 1
#         last_day = calendar.monthrange(current_year, current_month)[1]
#         while current_day <= last_day:
#             day_data = {
#                 "name": str(current_day),
#                 "kirim": 123,
#                 "chiqim": 543
#             }
#             month_data["days"].append(day_data)
#             current_day += 1

#         year_data["months"].append(month_data)
#         current_month += 1

#     result.append(year_data)
#     current_year += 1

# # Write the result to a JSON file
# with open('data.json', 'w') as json_file:
#     json.dump(result, json_file, indent=4)





# mylis=[1,2,3,4,1]
# target=[i if mylis[i]==1 else 0 for i in range(len(mylis))]
# print(mylis)




mylis = [1, 2, 3, 4, 1]

# Create a new list 'target' with indices where the value is equal to 1
target = [i for i in range(len(mylis)) if mylis[i] == 1]

# Print the 'mylis' list
print(mylis)
# Print the 'target' list
print(target)