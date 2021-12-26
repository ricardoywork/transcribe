# Clever.fm: Take Home Problem
ddd

## Context

The Clever.fm podcast app allows users to transcribe a segment of the audio
they just heard in the episode.

## Question

We want you to implement a data structure to store transcripts and a script to
retrieve transcript segments between a start and end time. The full episode
transcript is available as a .txt file in the same folder as the main.py file.
Episodes are identified by a unique ID.

For example,
```
retrieve_segment_transcript(episode_id, start_time, end_time)
```
retrieves the segment of transcript between `start_time` -> `end_time` for the
episode corresponding to `episode_id`.

This means that the three inputs to the script are:
- start_time (float, seconds from the begining of the episode)
- end_time (float, seconds from the begining of the episode)
- episode_id (str, to identify the transcript file)

The `main.py` file contains a stub for you to fill out. It includes a few test
cases, but you can add more of your own as you see fit. We'll run the main.py
file to execute the solution, but you are free to structure your code as you
want.

## Transcript format

```
0:01  
When I was a kid, apples were garbage. They were called Red Delicious and they were red. They were not delicious. They looked beautiful, but then you bite into it, and almost always it would be mushy and mealy, just nasty.

0:15  
It was a really bad time to be an apple eater. It was also a really bad time to be an apple grower.

0:21  
Everybody really just about literally everybody was growing Red Delicious.

```

Here's a link to the episode above: https://www.npr.org/transcripts/410085320

Note: This isn't needed to solve the problem and provided just in case you are
curious.

## Explanation of format

- The file is guaranteed to repeat the following three line format:
```
timestamp
transcript
blank line
```
- The timestamp line specifies the start time of the first word in `transcript` that follows
- Timestamp is in the format h:m:ss

## General comments

- The problem is general on purpose and we have left out some details on purpose.
If you think some information is missin, please feel free to make an assumption and document it. 
- During the in-person interview, we'll expand upon the same problem. So, I encourage you to dig deep and think about how we might integrate this functionality into a backend system.
