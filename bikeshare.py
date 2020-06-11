import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
    end_city_loop = 0
    while end_city_loop != 1:
        city = input('Would you like to see data for Chicago, New York City or Washington? (Will prompt for input again if it\'s invalid) ').lower()
        if city in CITY_DATA.keys():
            end_city_loop += 1

    # TO DO: get user input for month (all, january, february, ... , june)
    end_month_loop = 0
    valid_months = ['january','february','march','april','may','june','all']
    while end_month_loop != 1:
        month = input('Which month\'s data would you like to see? Please enter January, February, March, April, May, June or all. (Will prompt for input again if it\'s invalid) ').lower()
        if month in valid_months:
            end_month_loop += 1

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    end_day_loop = 0
    valid_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while end_day_loop != 1:
        day = input('Which day of the week\'s data would you like to see? Please enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all. (Will prompt for input again if it\'s invalid) ').lower()
        if day in valid_days:
            end_day_loop += 1

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
    # read data by city provided
    df = pd.read_csv(CITY_DATA[city])

    # get month and day of week filters for df
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # check for all months case
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # check for all days case
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # create a dictionary for months to map on the numeric months
    months = {1: "January", 2: "February", 3:"March", 4:"April", 5:"May", 6:"June"}
    most_popular_month = months[df['month'].mode()[0]]
    print('Most popular month: ', most_popular_month)

    # TO DO: display the most common day of week
    most_popular_day = df['day_of_week'].mode()[0]
    print('Most popular day of week: ', most_popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: ', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', most_popular_start_station)

    # TO DO: display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', most_popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    start_end_station = df.groupby(['Start Station','End Station']).size().reset_index().rename(columns={0:'count'}).sort_values(by='count', ascending=False)
    print('Most popular combination of start and end station : ', start_end_station['Start Station'].values[0], ' and ', start_end_station['End Station'].values[0],', count: ', start_end_station['count'].values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travle time (in seconds): {}'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travle time (in seconds): {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Total customer count: {}'.formate(user_type['Customer']))
    print('Total subscriber count: {}'.format(user_type['Subscriber']))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('Male count: {}'.format(gender_count['Male']))
        print('Female count: {}'.format(gender_count['Female']))
    else:
        print('Gender data not available.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest birth year: {}'.formate(df['Birth Year'].min()))
        print('Most recent birth year: {}'.format(df['Birth Year'].max()))
        print('Most common birth year: {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('Birth year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data on bikeshare users."""

    valid_input = ['yes', 'no']
    loop_end = 0
    counter = 0

    while loop_end != 1:
        #prompt user for input to see raw data
        display_raw_data = input('\nWould you like to see five lines of raw data? Enter yes or no.\n').lower()
        #check if input is valid
        if display_raw_data in valid_input:
            # display 5 rows of data
            if display_raw_data == 'yes':
                print(df.iloc[counter*5:(counter*5)+5])
                counter+=1
            # end loop if user prompt "no"
            elif display_raw_data == 'no':
                loop_end+=1

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
