#convert durations from P#DT#H#M#S to a format what we understand
#populate a video type column using the durations column with the rule of video of 1 minute or shorter to be 'Shorts' else normal
from datetime import timedelta, datetime

def parse_duration(duration_str):
#replace characters p & t with nothing
    duration_str = duration_str.replace("P", "").replace("T", "")

#define components we are looking for using a list and initialise their values to zero using a values dictionary
    components = ["D", "H", "M", "S"]
    values = {"D": 0, "H": 0, "M": 0, "S": 0}

#loop through the component, and the split and extract integer value once found
    for component in components:
        if component in duration_str:
            value, duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values["D"], hours=values["H"], minutes=values["M"], seconds=values["S"]
    )

    return total_duration

def transform_data(row):

    duration_td = parse_duration(row["Duration"])

    row["Duration"] = (datetime.min + duration_td).time()

    row["Video_Type"] = "Shorts" if duration_td.total_seconds() <= 60 else "Normal"

    return row