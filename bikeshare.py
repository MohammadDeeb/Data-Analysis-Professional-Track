from calendar import month
from pickle import NONE
import pandas as pd
import numpy as np 
import time



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january','february','march','april','may','june','july','august','september','october','november','december']
days_of_week = ['saturday','sunday','monday','tuesday','wednesday','thursday','friday']
date_data = ['month','day','both','none']

def get_filters(city = None , month = None , day = None):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
        if city not in CITY_DATA:
            print("Please enter the correct city name:")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        fill_data = input("Would you like to filter the data by month, day, both or not at all? Type 'none' for no time filter\n").lower()
        if fill_data not in date_data:
            print("Please enter the correct date name:")
        else:
            break
    while fill_data == 'month':
        month = input("Which month - January, February, March, April, May, or June?\n").lower()
        if month not in months:
            print("Please enter the correct month name:")
        else:
            break
    while fill_data == 'day':            
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
        if day not in days_of_week:
            print("Please enter the correct day name:")
        else:
            break
    while fill_data == 'both':
        month = input("Which month - January, February, March, April, May, or June?\n").lower()
        if month not in months:
            print("Please enter the correct month name:")
        if month in months:
            while True:
                day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n").lower()
                if day not in days_of_week:
                    print("Please enter the correct day name:")
                else:
                    break
        if month in months and day in days_of_week:
            break
        if fill_data == 'none':
            break
        # else:
        #     break

    # get user input for day of week (all, monday, tuesday, ... sunday)
        

    print('-'*40)
    return city , month, day

def load_data(city = NONE, month = NONE , day = NONE):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month

    # extract day from the Start Time column to create an day column
    df['day_of_week'] = df['Start Time'].dt.day_name() # weekday_name was removed from DatetimeProperties

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    # popular_hour = df['hour'].mode()
    # print('Most Frequent Start Hour:', popular_hour)

    # now we have 3 cases of filter by month , day , both 
    if month != None and day == None:
        # fix index of months in the list 
        month = months.index(month) + 1
        # create new df
        df = df[df['month'] == month]
    if day != None and month == None:
        df = df[df['day_of_week'] == day.title()]
    if month != None and day != None:
        month = months.index(month) + 1
        df1 = df[df['month'] == month ] 
        df2 = df[df['day_of_week'] == day.title()]
        combine_df = [df1,df2]
        df = pd.concat(combine_df,axis=1, join='inner')

    return df

def display_raw_data(df):
    i=5
    while True:
        if i==5:
            display = input("Do you like to see raw data? yes or no? ").lower()
            if display == 'yes' or display == 'y':
                print(df.head())
            else:
                break
        display= input("Do you like to see more raw data? ").lower()
        if display == 'yes' or display == 'y':
            print(df.iloc[i:i+5, :])
            i+= 5
        else:
            break
    return display

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]

    # display the most common start hour
    common_start_hour = df['hour'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("{} : is the most common month\n{} : is the most common day of the week\n{} : is the most common start hour\n".format(most_common_month,common_day_of_week,common_start_hour))
    print('-'*40)            

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['most_frequent_combination'] = df['Start Station'] + " - " + df['End Station']
    most_frequent_combination = df['most_frequent_combination'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("({}) is the most common start station\n\
({}) is the most common end station\n\
({}) is the most frequent combination".format(most_common_start_station,most_common_end_station,most_frequent_combination))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("{} : is the total travel time in seconds\n\
{} : is the total average travel time in hours".format(total_travel_time/3600,average_travel_time/3600))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    if city != 'washington':
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        # print(gender_counts)
        # Display earliest, most recent, and most common year of birth
        early_year_of_birth = df['Birth Year'].min()
        most_recent_year_of_birth = df['Birth Year'].max()
        most_common_year_of_birth = df['Birth Year'].mode()[0]
    print("the user type counts is:\n{}".format(user_types_counts))
    print("the gender counts is:\n{}".format(gender_counts))
    print("{} is the early year of birth\n\
{} is the most recent rear of birth\n{} is the most common year of birth".format(early_year_of_birth,most_recent_year_of_birth,most_common_year_of_birth))    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)
        time_stats(df)
        station_stats(df) 
        trip_duration_stats(df)
        user_stats(df,city)
        restart = input("Do you want to start new analysis? yes or no? ").lower()
        if restart == 'yes' or  restart == 'y':
            continue
        else:
            break
        #df.info()H
        #print(df.head())
        #print(city,month,day)

if __name__ == "__main__":
	main()