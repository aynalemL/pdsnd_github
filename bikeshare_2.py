import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv'
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    city = ''
    city = input(' Which city do you want to check first? >').lower().strip()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Wrong selection, please choose from chicago, new york city, washington >')

        # TO DO: get user input for month (all, january, february, ... , june)

    month = input('For which month of the year? >').lower().strip()
    if month not in ['all', 'January', 'February', 'March', 'April', 'May', 'june']:
        month = input('Invalid selection please choose either all or from January,\
                      February, March, April, May, june')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('For which days of the week? >').lower().strip()
    if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Invalid selection: please choose all or from day between Monday to Sunday')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        months = ['January', 'February', 'March', 'April', 'May', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        day = time.strptime(day, "%A").tm_wday
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month is:', most_common_month)

    # print("The most common month is: {}".format(
    #    str(df['month'].mode().values[0]))
    # )

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day is:', popular_day_of_week)

    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_start_time = df['Start Time'].mode()[0]
    print('The most common start hour is:', common_start_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_st_station = df['Start Station'].mode()
    print('The most popular start station is {}'.format(popular_st_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()
    print('The most popular end station is {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    start_end_popular_station = df[['Start Station', 'End Station']]. \
        groupby(['Start Station', 'End Station']).size().nlargest(1)

    print('\n Most Commonly used start and end station is:', start_end_popular_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_tr_time = df['Trip Duration'].sum()
    print('Total travel time:', total_tr_time / 86400, " Days")
    # TO DO: display mean travel time
    avg_trv_time = df['Trip Duration'].mean()
    print('Average travel time:', avg_trv_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users. If washington selected there is no gender or birth_year column"""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_of_user_type = df['User Type'].value_counts()
    print('User count of user by user type:', count_of_user_type)

    # TO DO: Display counts of gender
    if city != 'washington':
         count_of_gender = df['Gender'].value_counts()
         print('The count of gender:', count_of_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
       earliest = df['Birth Year'].min()
       latest = df['Birth Year'].max()
       mode = df['Birth Year'].mode()
       print('Oldest were born on: {}.\nThe youngest were born on: {}.'
          '\nThe most popular birth year is {}.'.format(earliest, latest, mode))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def display_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """

    start_loc = 0
    end_loc = 5

    display_active = input("Do you want to see the raw data?: ").lower()

    if display_active == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc, :])
            start_loc += 5
            end_loc += 5

            end_display = input("Do you wish to continue?: ").lower()
            if end_display == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
