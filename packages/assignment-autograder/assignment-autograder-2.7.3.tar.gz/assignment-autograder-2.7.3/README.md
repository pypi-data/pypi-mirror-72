This utility aims to provide a simple, yet highly configurable way to autograde programming assignments.

I consider it to be finished. From now on, I will only be adding extra grading languages if necessary and fixing bugs if any are reported.
# Features
* Most features are demonstrated in examples/ directory
* Easy to grade (simply running `autograder` on a directo#filesry with assignments and testcases)
* Easy-to-write testcases
* Testcase grade can be based on student's output in stdout
* A per-testcase grade can be any number out of 100 points
* Support for grading C, C++, Java, and Python code
* A result file can be generated for each student (it is done by default)
* You can customize the total points for the assignment, timeout for the running time of student's program, file names to be considered for grading, and filters for checking output
* Anti-Cheating capabilities that make it nearly impossible for students to break the grader and choose their results (randomized result exit codes and --precompile_testcases option). You can read more on this in implementation details section.
* You can pass arguments to language compilers during testcase (or submission) precompilation and compilation using config.ini
* You can grade submissions in multiple programming languages at once, as long as there are testcases written in each language
# Installation (Linux-only) (Python >= 3.6)
* Run `pip3 install assignment-autograder`
* If you want to update to a newer version, run `pip3 install --upgrade --no-cache-dir assignment-autograder`
# Quickstart
* Run `autograder path/to/directory/you'd/like/to/grade --guide`. The guide will create all of the necessary configurations and directories for grading.
# Usage
1) Create tests directory in the same directory as student submissions. It has to follow the same structure as one of the examples.
2) Write testcases as described below. You can use examples/ as reference.
3) Create input and output text files in their respective directories for each testcase. If a test does not require input and/or output, the respective text file is also not required.
4) run `autograder path/to/submissions/dir` from command line. If you are in the same directory as submissions, you can simply run `autograder`.
## Advanced Usage
* If you create config.ini in tests, you can customize grader's behavior. Use `autograder --generate_config` to generate a default config if your directory is already set up. If you remove some configuration fields, grader will use the respective fields from default config.
* To check output, you can specify output formatters in a file output_formatters.py in the directory with your testcase folder. They will format output to allow you to give credit to students even if their output is not exactly the same as expected. To see how to write this file, you can look at autograder/default_formatters.py
## Writing testcases
* Write a main that follows the same structure as the respective example. The main should usually call student's code and check its result (when working with output, you usually don't check the result, and simply allow grader to handle that)
* Assume that student's code is available in your namespace. Examples demonstrate exactly how to call students' functions.
* Assume that helper functions CHECK_OUTPUT(), RESULT(int r), PASS(), FAIL() are predefined and use them to return student scores to the grader
* Each helper function terminates the execution of the program and returns its respective exit code that signifies student's score for the testcase
* Each testcase is graded out of 100%, which means that you can fully control how much partial credit is given
* ### Helper functions
    * CHECK_OUTPUT() indicates that we do not check student's return values for the testcase and that we only care about their output (stdout).
    * RESULT(int r) returns student's score r back to the grader (0 - 100)
    * PASS() returns the score of 100% back to the grader and is equivalent to RESULT(100)
    * FAIL() returns the score of 0% back to the grader and is equivalent to RESULT(0)
# Command line help
```
usage: autograder [-h] [-p [min_score]] [--no_output] [--generate_config]
                  [-s [<submission_name> [<submission_name> ...]]] [-g]
                  [submission_path]

positional arguments:
  submission_path       Path to directory that contains student submissions

optional arguments:
  -h, --help            show this help message and exit
  -p [min_score], --print [min_score]
                        Use after already graded to print assignments with
                        score >= min_score
  --no_output           Do not output any code to the console
  --generate_config     Generate a default config file in the
                        <submission_path>
  -s [<submission_name> [<submission_name> ...]], --submissions [<submission_name> [<submission_name> ...]]
                        Only grade submissions with specified file names
                        (without full path)
  -g, --guide           Guide you through setting up a grading environment
```
# Implementation details
* I used exit codes to specify student grades. Currently, I pick all exit codes that are not used by the system, randomize them, and cut off the ones I don't need. Then I use the first 101 exit codes for the results, and one more for checking output. So a student has no way of knowing which exit codes correspond to which results. The chance of trying out a number and getting anything above a 90 is about 5%. If you are worried that students will simply read the correct exit codes from the testcase file, you can use `--precompile_submissions` to make only the testcase bytecode available.
* If you want to add a new language for grading, you have to create a subclass of TestCase in autograder/testcases.py following the pattern of other subclasses and a respective test helper module in autograder/tests/test_helpers directory, then import the subclass into autograder/grader.py, and add it to ALLOWED_LANGUAGES dictionary
* At the point of writing this readme, output checking is a PASS or FAIL process (i.e. no partial credit possible). The reason is that allowing for 'partial similarity' of outputs is too error-prone and could yield too many points for students that did not actually complete the task properly. If you want to increase the chances of students' output matching, you should use FILTER_FUNCTION(s) defined in autograder/grader.py instead
* If you don't prototype student functions you want to test in your C/C++ testcases, you will run into undefined behavior. 
* Multiprocessing was a feature in the past but it has so many drawbacks that it was deemed unnecessary for the task
