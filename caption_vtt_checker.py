import argparse
import os
import sys
import time
from datetime import datetime


def f_convert_to_seconds (time_item):
    sec = datetime.strptime(time_item, '%H:%M:%S.%f')
    total_seconds = sec.second + sec.minute * 60 + sec.hour * 3600
    return total_seconds

def f_match_duration (caption_duration, video_duration):
    caption_duration_sec = f_convert_to_seconds(caption_duration)
    video_duration_sec = f_convert_to_seconds(video_duration)
    if video_duration_sec - 210 <= caption_duration_sec <= video_duration_sec + 210:
        print("The video matches to the captioned duration.\n")
    else:
        print("The video doesn't match to the captioned duration.\n")

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Check process of VTT file')
    # Add the arguments
    parser.add_argument('input_vtt', help='Input vtt format file')
    parser.add_argument('video_length', type = str, help = 'Duration estimation')
    # Execute the parse_args() method
    args = parser.parse_args()
    with open(args.input_vtt) as f_vtt:

    #Check whether the path is correct
        if not os.path.isfile(args.input_vtt):
            print("The file %s specified does not exist" % f_vtt)
            sys.exit()

        # Clean the timestamps of the file
        final_list_seconds = []
        clean_timestamps = []
        for line in f_vtt:
            remove_spaces = line.replace("\n", "")
            if ' --> ' in remove_spaces:
                clean_timestamps = remove_spaces.split(' --> ')
                # Convert the timestamps from HH:MM:SS to seconds. Get rid of miliseconds.
                for item in clean_timestamps:
                    final_list_seconds.append(f_convert_to_seconds(item))
        size = len(final_list_seconds)
        index = 0
        number_of_gaps = 0
        while index < size - 1:
            if final_list_seconds[index + 1] - final_list_seconds[index] > 120:
                number_of_gaps += 1
            index += 1
        if number_of_gaps == 0:
            print("No gaps found")
        else:
            print("Number of gaps bigger than 120 seconds: " + str(number_of_gaps))

        # Print the total duration of the captions.
        captioned_length_sec = final_list_seconds[-1] - final_list_seconds[0]
        print("Total captioned duration: " + time.strftime('%H:%M:%S',time.gmtime(captioned_length_sec)))

        # Return true or false in case that the real duration is the same than the input value
        video_sec = datetime.strptime(args.video_length, '%H:%M:%S')
        video_duration_sec = video_sec.second + video_sec.minute * 60 + video_sec.hour * 3600
        if video_duration_sec - 210 <= captioned_length_sec <= video_duration_sec + 210:
            print("The video matches to the captioned duration.\n")
        else:
            print("The video doesn't match to the captioned duration.\n")

main()
