# VideoCoding_P3
## Practice 3 of Video Coding: Python and video

### Parts

**Part 1:** Create a new BBB mp4 container with:
- BBB into 1 minute only video.
- BBB (1min) audio as a mono track.
- BBB (1min) audio in lower bitrate
- Subtitles of BBB and cut only the first minute.

**Part 2:** Create a python script able to automatize the creation of MP4 containers. It can be like the previous one, more or less complex...be creative!

**Part 3:** Create a script which reads the tracks from an MP4 container, and it’s able to say which broadcasting standard fits.

**Part 4:** Create a testing script, which will generate containers to launch against exercise 3.

**Part 5:** Integrate everything inside a class.

### Code

This code uses the ffmpeg package for python.

It already creates a container class, which starts part 4 testing that calls both functions for parts 2 and 3. The first option is to either create a new container or not. In both cases, the broadcasting standard test is launched afterwards.

For part 2 we can specify how many video streams, audios and subtitle files we want in the container and then write the names of existing files.

For part 3, the function will ask for the input name in case it is not specified as a parameter. It will then show on screen which broadcasting standards the container fits depending on the codecs of its video and audio files from this list:
- DVB
- ISBD
- ATSC 
- DTMB
