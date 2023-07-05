import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
VALID_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
VALID_YN = ['yes', 'no']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n\n')

    city, month, day = '', '', ''
    month_str_suffix, day_str_suffix = '', ''

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while_count = 0
    while True:
        if while_count > 0:
            print('The city value "' + city + '" you have entered is invalid.\n')
        city = input('What city would you like to view data for? Enter: ' + ', '.join(CITY_DATA) + '\n')
        if city.lower() in CITY_DATA:
            break
        while_count += 1
    print('The city you have selected is ' + city.lower() + '\n')


    # Get user input for month (all, january, february, ... , june)
    while_count = 0
    while True:
        if while_count > 0:
            print('The month value "' + month + '" you have entered is invalid.\n')
        month = input('What month would you like to view data for? Enter January, February, March, April, May, June or all\n')
        if month.lower() in VALID_MONTHS:
            break
        while_count += 1
    if month.lower() == 'all':
        month_str_suffix = ' of them'
    print('The month you have selected is ' + month.lower() + month_str_suffix + '\n')

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while_count = 0
    while True:
        if while_count > 0:
            print('The day value "' + day + '" you have entered is invalid.\n')
        day = input('What day would you like to view data for? Enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all\n')
        if day.lower() in VALID_DAYS:
            break
        while_count += 1
    if day.lower() == 'all':
        day_str_suffix = ' of them'
    print('The day you have selected is ' + day.lower() + day_str_suffix + '\n')


    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month int and day of week name str from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the valid months list to get the corresponding int
        month = VALID_MONTHS.index(month) + 1
        # Filter by given month from user to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by given day of week from user to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month name
    print('\nThe most common month is: \n', VALID_MONTHS[df['month'].mode()[0]-1].title())

    # Display the most common day of week name
    print('\nThe most common day of week is: \n', df['day_of_week'].mode()[0])

    # Display the most common start hour
    print('\nThe most common start hour (24h) is: \n', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('\nThe most common start station is: \n', df['Start Station'].mode()[0])

    # Display most commonly used end station
    print('\nThe most common end station is: \n', df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    df['Combined Stations'] = df['Start Station'] + ' - ' + df['End Station']
    print('\nThe most frequent combination of start station and end station is: \n', df['Combined Stations'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total travel time (seconds) is: \n', df['Trip Duration'].sum())

    # display mean travel time
    print('\nThe mean travel time (seconds) is: \n', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f"\nThe counts of user types is: \n{df['User Type'].value_counts()}")

    # Display counts of gender
    if is_valid_column(df, 'Gender'):
        print(f"\nThe counts of gender is: \n{df['Gender'].value_counts()}")
    else:
        print('\nThe gender column is unavailable for this dataset')

    # Display earliest, most recent, and most common year of birth
    if is_valid_column(df, 'Birth Year'):
        print('\nThe earliest birth year is: \n', int(df['Birth Year'].min()))
        print('\nThe most recent birth year is: \n', int(df['Birth Year'].max()))
        print('\nThe most common birth year is: \n', int(df['Birth Year'].mode()[0]))
    else:
        print('\nThe year of birth is unavailable for this dataset\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city):
    """Displays raw data 5 rows at a time."""

    print('\nDisplaying raw file data...\n')

    file_name = CITY_DATA[city]
    # Skip header row
    file_line_count = 1
    get_lines = ''

    while get_lines.lower() == 'yes' or get_lines.lower() == '':
        while_count = 0
        while True:
            if while_count > 0:
                print('The value "' + get_lines + '" you have entered is invalid.\n')
            get_lines = input('Would you like to display 5 lines of raw data? Enter yes or no\n')
            if get_lines.lower() in VALID_YN:
                break
            while_count += 1
        while_count = 0

        if get_lines.lower() == 'yes':
            with open(file_name, 'r') as file_lines:
                lines = [line for line in file_lines][file_line_count:file_line_count+5]
                print('\n')
                print(*lines, sep='\n')

            file_line_count += 5


def is_valid_column(df, column):
    """
    Checks if a column exists in the data frama.

    Args:
        df - data fram
        (str) column - name of the column
    Returns:
        boolean
    """

    for label, content in df.items():
        if label == column:
            return True
    return False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = ''
        while_count = 0
        while True:
            if while_count > 0:
                print('The value "' + restart + '" you have entered is invalid.\n')
            restart = input('\nWould you like to restart? Enter yes or no\n')
            if restart.lower() in VALID_YN:
                break
            while_count += 1

        if restart.lower() == 'no':
            print('\nGoodbye')
            break


if __name__ == "__main__":
	main()
