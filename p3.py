from os import system, path, remove
import numpy as np


# ex1:
# we first cut a 1 minute video of BBB
#ffmpeg -i BBB.mp4 -c copy -t 60 BBB_cut.mp4

# we set the audio to mono and export it without video (-vn)
#ffmpeg -i BBB_1min.mp4 -ac 1 -vn monoaudio.ac3

# we set a bitrate half of the original
# we can see the bit rate with ffprobe -v error -show_format -show_streams BBB_1min.mp4
#ffmpeg -i BBB_1min.mp4 -vn -b:a 224k lowrate.ac3 #original 448k

# we create a new container with everything we created
#ffmpeg -i BBB_1min.mp4 -i BBBsubs.srt -i monoaudio.ac3 -i lowrate.ac3 -c:v copy -c:a aac -c:s mov_text -map 0:v:0 -map 2:a:0 -map 3:a:0 -map 1:s:0 container.mp4

class container_manager:
    # ex2: automatize process

    # checks if input is a number
    def input_number(self):
        ok = False

        while not ok:
            inp = input()
            try:
                val = int(inp)
                ok = True
            except ValueError:
                print("please choose a number:")

        return val

    # iterates over especified number of files
    def input_files(self, num, command):
        for i in range(num):
            print("file " + str(i+1) + " name:")
            file = input()
            while not path.exists(file):
                print("this file does not exist. please try again")
                file = input()
            command += "-i " + file + " "
        return command

    # takes the current iteration and returns the proper letter depending on the file
    def map(self, iter, n_files):
        video = n_files[0]
        audio = video + n_files[1]
        if iter < video:
            return "v"
        elif iter < audio:
            return "a"
        else:
            return "s"

    def create_container(self):
        command = "ffmpeg "

        print("how many video streams?")
        n_video = self.input_number()
        command = self.input_files(n_video, command)

        print("how many audios?")
        n_audio = self.input_number()
        command = self.input_files(n_audio, command)

        print("how many subtitle files?")
        n_subs = self.input_number()
        command = self.input_files(n_subs, command)

        command += "-c:v copy -c:a ac3 -c:s mov_text " # elegir codec de audio?

        n_files = np.array([n_video, n_audio, n_subs])

        for i in range(sum(n_files)):
            command += "-map " + str(i) + ":"  + self.map(i, n_files) + ":0 "

        print("container name:")
        output = input()
        command += output

        system(command)

        return output


    # ex3: reads mp4 tracks and tells what broadcasting standard fits

    def tell_standard(self, file = False):
        # ask file name if not in as a param
        if not file:
            print("file name:")
            file = input()
            while not path.exists(file):
                print("this file does not exist. please try again")
                file = input()

        # create a txt where we will extract the codec names
        command = "ffprobe -show_streams " + file + " > output.txt 2>&1"
        system(command)
        list = []

        # Read the entire file line by line
        with open('output.txt', 'r') as reader:
            line = reader.readline()
            while line != '':  # The EOF char is an empty string
                if "codec_name=" in line:
                    # we save the codec names
                    list.append(line[11:])
                line = reader.readline()

        # we erase the txt and polish the strings in list
        remove("output.txt")
        for i in range(len(list)):
            list[i] = list[i][:-1]

        # catalog
        dvb = ["mpeg2", "h264", "aac", "ac3", "mp3"]
        isbd = ["mpeg2", "h264", "aac"]
        atsc = ["mpeg2", "h264", "ac3"]
        dtmb = ["avs", "avs+", "mpeg2", "h264", "dra", "aac", "ac3", "mp2", "mp3"]
        standards = [dvb, isbd, atsc, dtmb]
        standards_names = ["dvb", "isbd", "atsc", "dtmb"]
        some_fit = False

        # check every standard and say if it fits
        count = 0
        print("possible standards:")
        for st in standards:
            if all(item in st for item in list):
                some_fit = True
                print(standards_names[count])
            count += 1

        if not some_fit:
            print("none fit!")


    # ex4: manager
    def __init__(self):
        end = False
        print("Welcome to the container manager!")
        while not end:
            print("do you want to create a new container? [y/n]")
            option = input()

            # option to create a new container and test it or just test any container
            if option == ("y" or "yes" or "Y" or "YES"):
                cont_name = self.create_container()
                self.tell_standard(cont_name)
            elif option == ("n" or "no" or "N" or "NO"):
                self.tell_standard()
            else:
                print("¬¬")

            print("want to test another one? [y/n]")
            option = input()
            if option == ("n" or "no" or "N" or "NO"):
                end = True
            elif option != ("y" or "yes" or "Y" or "YES"):
                print("¬¬")
                end = True


x = container_manager()
