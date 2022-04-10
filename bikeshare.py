import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for chicago, new york, or washington? ').lower()
        if city in ['chicago', 'new york', 'washington']:
            break
    
    while True:
        choice = input('Would you like to filter the data by month, day, both, or not at all? Type "none" for no time filter. ').lower()
        if choice in ['month', 'day', 'none', 'both']:
            break
                    
    month = 'all'
    # TO DO: get user input for month (all, january, february, ... , june)
    if choice in ['month', 'both']:
        while True:
            month = input('Which month - January, February, March, April, May, or June? Type "all" to apply no month filter. ').lower()
            if month.title() in ['January', 'February', 'March', 'April', 'May', 'June', 'All']:
                break
    
    day = 'all'
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if choice in ['day', 'both']:
        while True:
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type "all" to apply no day filter. ').lower()
            if day.title() in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
                break


    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def view_raw_data_samples(df):
    """ Displays 5 rows from the data"""
    
    while True:
        view_sample_rows = input('\nWould you like to see raw data? Enter yes or no.\n')
        if view_sample_rows in ['yes', 'no']:
            break
    
    start_index = 0
    while True:
       
        if view_sample_rows == 'yes':
            if start_index > df.shape[0]:
                print('No more raw data to display.')
                return
          
            print(df.iloc[start_index:start_index+5, :])
            start_index += 5
        else:
            break
            
        while True:
            view_sample_rows = input('\nWould you like to see 5 more rows of the data? Enter yes or no.\n')
            if view_sample_rows in ['yes', 'no']:
                break
        
        
    
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df['month'].mode()[0]
    print('Most Frequent month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent day_of_week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_station)
    
    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_station)

    df['Trip stations'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Trip stations'].mode()[0]
    print('Most frequent combination of start station and end station trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is:',  df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Avg travel time is:',  df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth is:',  df['Birth Year'].min())
        print('Most recent year of birth is:',  df['Birth Year'].max())
        print('Most common year of birth is:',  df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        view_raw_data_samples(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
