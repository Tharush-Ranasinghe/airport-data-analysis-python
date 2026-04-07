"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 20240613 UOW ID:w2181565
 4. Date: 23/11/2025
****************************************************************************
"""
from graphics import *
import csv
import re

data_list = []  # empty list to load and hold data from csv file

# Dictionaries for airport and airline codes
airports = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

airlines = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}


def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)


def get_city_code():
    # Get the city code from user
    while True:
        city_code = input("Please enter a three letter city code: ").upper()
        if len(city_code) != 3:
            print("Wrong code length - please enter a three-letter city code: ")
            continue
        if city_code not in airports:
            print("Unavailable city code - please enter a valid city code:")
            continue
        return city_code


def get_year():
    # get the year from user
    while True:
        year = input("Please enter a four digit year: ")
        if len(year) != 4 or not year.isdigit():
            print("Wrong data type - please enter a valid four digit year:")
            continue
        if int(year) < 2000 or int(year) > 2025:
            print("Out of range - please enter a value from 2000 to 2025:")
            continue
        return year


def extract_temperature(weather_text):
    # Extract the first numeric temperature value from weather text (e.g., "14°C light rain")
    match = re.search(r"\d+", weather_text)
    return int(match.group()) if match else None


def time_to_minutes(time_text):
    # Convert HH:MM text into total minutes for proper time comparison
    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)


def results():  # calculate required values from data_list
    # variables for calculations
    terminal2_dept = 0
    under_600 = 0
    air_france = 0
    temp_under15 = 0
    british_airways = 0
    af_delayed = 0
    rain_hours = set()
    travelled = {}
    total_flights = len(data_list)

    for data in data_list:
        if data[8] == "2":
            terminal2_dept += 1

        if int(data[5]) < 600:
            under_600 += 1

        if data[1].startswith("AF"):
            air_france += 1

        temperature = extract_temperature(data[10])
        if temperature is not None and temperature < 15:
            temp_under15 += 1

        if data[1].startswith("BA"):
            british_airways += 1

        if data[1].startswith("AF") and time_to_minutes(data[3]) > time_to_minutes(data[2]):
            af_delayed += 1

        if "rain" in data[10].lower():
            hour = data[2].split(":")[0]
            rain_hours.add(hour)

        if data[4] not in travelled:
            travelled[data[4]] = 1
        else:
            travelled[data[4]] += 1

    ba_per_hour = round(british_airways / 12, 2)
    ba_depts_percentage = round((british_airways / total_flights) * 100, 2)
    delayed_af_percentage = round((af_delayed / air_france) * 100, 2) if air_france > 0 else 0
    least_travelled = [d for d in travelled if travelled[d] == min(travelled.values())]

    return (  # return all calculated values
        total_flights,
        terminal2_dept,
        under_600,
        air_france,
        temp_under15,
        ba_per_hour,
        ba_depts_percentage,
        delayed_af_percentage,
        len(rain_hours),
        least_travelled
    )


#print output to idle

def idle_output(
    # call calculated values as parameters
    total_flights,
    terminal2_dept,
    under_600,
    air_france,
    temp_under15,
    ba_per_hour,
    ba_depts_percentage,
    delayed_af_percentage,
    rain_hours,
    least_travelled,
    selected_data_file,
    city_code,
    year):
    # Print output according to the format
    print("*" * 85)
    print(f"File {selected_data_file} selected - Planes departing {airports[city_code]} {year}")
    print("*" * 85)
    print()
    print(f"The total number of flights from this airport was {total_flights}\n")
    print(f"The total number of flights departing Terminal Two was {terminal2_dept}\n")
    print(f"The total number of departures on flights under 600 miles was {under_600}\n")
    print(f"There were {air_france} Air France flights from this airport\n")
    print(f"There were {temp_under15} flights departing in temperatures below 15 degrees\n")
    print(f"There was an average of {ba_per_hour} British Airways flights per hour from this airport\n")
    print(f"British Airways planes made up {ba_depts_percentage}% of all departures\n")
    print(f"{delayed_af_percentage}% of Air France departures were delayed\n")
    print(f"There were {rain_hours} hours in which rain fell\n")
    least_travelled_names = [airports.get(code, code) for code in least_travelled]  # get the full name of the least common destinations
    print(f"The least common destinations are {least_travelled_names}\n")


#write output to a text file

def file_output(
    # call calculated values as parameters
    total_flights,
    terminal2_dept,
    under_600,
    air_france,
    temp_under15,
    ba_per_hour,
    ba_depts_percentage,
    delayed_af_percentage,
    rain_hours_count,
    least_travelled,
    selected_data_file,
    city_code,
    year
):
    # save the output on a text file
    with open("results.txt", "a") as file:
        file.write("*" * 85 + "\n")
        file.write(f"File {selected_data_file} selected - Planes departing {airports[city_code]} {year}\n")
        file.write("*" * 85 + "\n")
        file.write(f"The total number of flights from this airport was {total_flights}\n")
        file.write(f"The total number of flights departing Terminal Two was {terminal2_dept}\n")
        file.write(f"The total number of departures on flights under 600 miles was {under_600}\n")
        file.write(f"There were {air_france} Air France flights from this airport\n")
        file.write(f"There were {temp_under15} flights departing in temperatures below 15 degrees\n")
        file.write(f"There was an average of {ba_per_hour} British Airways flights per hour from this airport.\n")
        file.write(f"British Airways planes made up {ba_depts_percentage}% of all departures\n")
        file.write(f"{delayed_af_percentage}% of Air France departures were delayed\n")
        file.write(f"There were {rain_hours_count} hours in which rain fell\n")
        least_travelled_names = [airports.get(code, code) for code in least_travelled]
        file.write(f"The least common destinations are {least_travelled_names}\n")
        file.write("\n")  # Add blank line between entries


def create_histogram(city_code, year):
    # create a histogram for a selected airline
    while True:
        airline = input("Enter a two-character Airline code to plot a histogram: ").upper()
        if airline not in airlines:
            print("Unavailable Airline code, please try again.")
        else:
            break

    flights_per_hour = [0] * 12
    # Filter data for the selected airline only
    for flight in data_list:
        flight_number = flight[1]  # Flight number is at index 1
        flight_airline = flight_number[:2]  # Extract first 2 characters as airline code

        if flight_airline == airline:  # Check if airline code matches
            time = flight[2]  # Departure time is at index 2
            hour = int(time.split(":")[0])
            if 0 <= hour <= 11:
                flights_per_hour[hour] += 1

    # Create histogram window
    histogram = GraphWin("Flight Departure Chart", 800, 600)
    histogram.setBackground("black")

    # Histogram Title
    title = Text(
        Point(400, 40),
        f"Departures by hour for {airlines[airline]} from {airports[city_code]} {year}"
    )
    title.setSize(16)
    title.setStyle("bold")
    title.setTextColor("white")
    title.draw(histogram)

    # Left labels
    hours_label = Text(Point(70, 200), "Hours")
    hours_label.setSize(12)
    hours_label.setStyle("bold")
    hours_label.setTextColor("white")
    hours_label.draw(histogram)

    time_range = Text(Point(70, 280), "00:00\nto\n12:00")
    time_range.setSize(10)
    time_range.setTextColor("white")
    time_range.draw(histogram)

    # Vertical axis
    v_axis = Line(Point(150, 80), Point(150, 520))
    v_axis.setWidth(2)
    v_axis.setFill("white")
    v_axis.draw(histogram)

    # Bottom horizontal axis
    h_axis = Line(Point(150, 520), Point(700, 520))
    h_axis.setWidth(2)
    h_axis.setFill("white")
    h_axis.draw(histogram)

    # bars to show flights per hour
    max_value = max(flights_per_hour) if max(flights_per_hour) > 0 else 1
    bar_height = 25
    spacing = 10
    y = 100 + (11 * (bar_height + spacing))

    for hour in range(11, -1, -1):
        count = flights_per_hour[hour]
        bar_length = (count / max_value) * 500 if max_value > 0 else 0

        # Hour label
        hour_label = Text(Point(120, y + bar_height / 2), f"{hour:02d}")
        hour_label.setSize(11)
        hour_label.setTextColor("white")
        hour_label.draw(histogram)

        # Bar
        bar = Rectangle(Point(150, y), Point(150 + bar_length, y + bar_height))
        bar.setFill(color_rgb(0, 120, 255))
        bar.setOutline("white")
        bar.draw(histogram)

        # Count of the flights on the bar
        count_label = Text(Point(165 + bar_length, y + bar_height / 2), str(count))
        count_label.setSize(10)
        count_label.setTextColor("white")
        count_label.draw(histogram)

        y -= bar_height + spacing  # move upward for next bar

    try:
        histogram.getMouse()
        histogram.close()
    except GraphicsError:
        # Window was already closed by user clicking X
        pass


def process_data_file():
    # Clear data_list for new run
    data_list.clear()

    # Get city code and year
    city_code = get_city_code()
    year = get_year()

    selected_data_file = city_code + year + ".csv"
    print(selected_data_file, "selected - Planes departing", airports[city_code], year)

    # Load the CSV file
    try:
        load_csv(selected_data_file)
    except FileNotFoundError:
        print(f"Error: File {selected_data_file} not found. Please try again.")
        return False

    # Calculate results
    calculations = results()

    # Display results to idle
    idle_output(*calculations, selected_data_file, city_code, year)
    return calculations, selected_data_file, city_code, year


def main():
    while True:
        process_result = process_data_file()
        if not process_result:
            # If file not found, ask if they want to try again
            while True:
                retry = input("Would you like to try a different file? Y/N: ").upper()
                if retry in ['Y', 'N']:
                    break
                print("Invalid input. Please enter Y or N.")
            if retry == 'N':
                print("Thank you. End of run")
                break
            continue

        calculations, selected_data_file, city_code, year = process_result

        # Save results to text file
        file_output(*calculations, selected_data_file, city_code, year)
        print("Results saved to results.txt")

        # Offer histogram view
        while True:
            histogram_choice = input("Do you want to display a histogram? Y/N: ").upper()
            if histogram_choice in ['Y', 'N']:
                break
            print("Invalid input. Please enter Y or N.")
        if histogram_choice == 'Y':
            create_histogram(city_code, year)

        # Ask if user wants to process another file
        while True:
            choice = input("\nDo you want to select a new data file? Y/N: ").upper()
            if choice in ['Y', 'N']:
                break
            print("Invalid input. Please enter Y or N.")

        if choice == 'N':
            print("Thank you. End of run")
            break


#start of the program
if __name__ == "__main__":
    main()
