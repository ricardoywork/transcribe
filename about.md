# Python version

The Python version used for development and testing is 3.10.

# Requirements

The transcript indexer does not depend on third-party libraries. However, the following packages were installed
to provide certain features:

* pytest: tests
* pip-tools: pip-compile, it is used to generate the requirements.txt file from requirements.in
* mypy: static analysis
* black: code formatter
* pylint: linter

Run `pip install -r requirements.txt`

# Tests

Aditional tests were created inside the folder `test`. Run `pytest` to execute them.

# Linter

Run `pylint --rcfile .pylintrc $(find -type f -name "*.py" ! -path "**/venv/**")`.

# Static analysis

Run `mypy .`. All functions were annotated using the `typing` annotations.

# About the project

## Transcript format

The parser is a little more lenient than it could/should be because of the line `Transcribed by https://otter.ai`
at the end of `episode_1.txt`. Therefore, it is implemented as a state machine that waits for a timestamp followed by 
any non-empty string, ignoring empty strings.

## Episode length

The last transcript is not followed by a timestamp that would indicate its end-time, so the episode length must be a
parameter provided to the system.

## No timestamp interval intersection

For any two different `(start-time-X, end-time-X)`, `(start-time-Y, end-time-Y)` intervals from a given episode, 
either `end-time-X <= start-time-Y` or `end-time-Y <= start-time-X` holds.
  
## Data structure

### First attempt

The transcripts are stored in a list ordered by `start-time` and, because of the previous item, also by `end-time` 
(represented by the dataclass `Transcription`). For each transcript, a similar structure was used for the tokens 
(represented by the dataclass `TokenizedTranscription`): to each one of them is assigned a `start-time` and `end-time`
that are evaluated based on the timestamps from the transcript itself and the number of tokens. The chosen type for 
the timestamps is `float` because it provides a more precise control instead of using `int`. 

For example:

```text
0:00
first second third

0:01
fourth
```

The tokens for the first transcript would be stored as:

```text
[
    (text='first', start_time=0., end_time=0.33333),
    (text='second', start_time=0.33333, end_time=0.66666),
    (text='third', start_time=0.6666, end_time=1.),
]
```

And the token for the second transcript would be:

```text
(text='fourth', start-time=1., end_time=2.)
```

if the episode length is 2 seconds.

Given a list `L` of `n` `Transcription`, the list `T` of `TokenizedTranscription` and arguments 
`(param_start_time, param_end_time)`, the method `retrieve_segment_transcript` will:

1. Return the index of each transcript in `L` that satisfies the constraint that the interval 
   `(param_start_time, param_end_time)` covers any part of the transcript;
2. For each transcript, return the tokens whose start and end timestamps are covered by `(param_start_time, param_end_time)`
3. Return a string that is the result of concatenating the tokens using a single space as separator.

The algorithm that searches for intervals that are covered by the start-time and end-time is based on the binary 
search algorithm (methods `search_end_ge` and `search_ini_le` from `index/tokenizer.py`) and can be applied for 
both `Transcription` and `TokenizedTranscription` lists. Firstly, it searches
for the smallest index in the list such that the end-time is greater than or equal to `param_start_time`. Similarly,
it searches for the largest index such that start-time is less than or equal to `param_end_time`. For example, using
`param_start_time=6` and `param_end_time=16` for the following list:

```text
[
    (start_time=0, end_time=5),
    (start_time=5, end_time=10),
    (start_time=10, end_time=15),
    (start_time=15, end_time=20),
    (start_time=20, end_time=25),
]
```

should return the tuple `(1, 3)`.

However, this approach has a problem: if one of the timestamps used as argument for `retrieve_segment_transcript`
is equal to the start-time or end-time of one of the elements from the list, the returned interval will be larger
than expected. For example, if `param_start_time=5` and `param_end_time=16`, the position 0 is the smalled index
that satisfies end-time >= 5, and the result will be the tuple `(0, 3)`.

### Second attempt

To prevent the problem defined previously, a small constant (`EPSILON = 1e-10`) is added to the start-time and
subtracted from the end-time for each element of the lists. So, the list

```text
[
    (start_time=0, end_time=5),
    (start_time=5, end_time=10),
    (start_time=10, end_time=15),
    (start_time=15, end_time=20),
    (start_time=20, end_time=25),
]
```

is converted into

```text
[
    (start_time=0+EPSILON, end_time=5-EPSILON),
    (start_time=5+EPSILON, end_time=10-EPSILON),
    (start_time=10+EPSILON, end_time=15-EPSILON),
    (start_time=15+EPSILON, end_time=20-EPSILON),
    (start_time=20+EPSILON, end_time=25-EPSILON),
]
```

and, for `param_start_time=5` and `param_end_time=16`, the first index returned is 1, because `5-EPSILON` is less than
5 and therefore the position 0 does not satisfy the constraint `end-time >= param_start_time`.

## Complexity

* The algorithms `search_ini_le` and `search_end_ge` are O(log(n)), n = length of the input list.
  
* The lists satisfy the ordering constraint for their timestamps if the transcripts are presented in chronological 
  order. Otherwise, it is possible to run a sort algorithm in O(n(log(n))).
  
## Other considerations

* I think it is possible to use B-Trees instead of lists if it is expected that the transcripts from a episode will
  be updated frequently, given that adding and removing an element from a B-tree are O(log(n)) and the same operations 
  on a list are O(n).
  
* The tokenizer used was just a split based on the regular expression `r"\S+"`. It is possible to inject other
  implementations of `AbstractTokenizer` that requires a more complex algorithm. For example, in Japanese there are no
  spaces to separate words in a single phrase.