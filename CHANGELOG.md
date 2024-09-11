## v0.4.8

#### Bugs
- Fixed a bug where the web interface would not update when not using a key with your worker.

## v0.4.7

#### Features
- There is now a run now control for jobs (via the web interface).
- There is now a pause control for jobs (via the web interface).
- All the controls features are disabled by default use the robit.set_controls(True) to activate the controls which are only available in the web interface.

#### Bugs
- Pipe connection between webserver should stop blocking now and provide a better user experience with the web interface.

## v0.4.6

#### Changes
- Exceptions and Logging now include full stack trace.

## v0.4.5

#### Changes
- Updated the included alpine to version 3.13.5

#### Bugs
- Fixed a bug where the interface would not update when not using a key with your worker.

## v0.4.4

#### Features
- Job results can now be backup to a sqlite database for longer term storage of results.
  - Usage: robit.set_database_logging(True)

#### Changes
- Improved web interface for job results and ability to look at last 1000 results if you are using database logging.
- Reduced the verbosity of the results when an exception occurs during a job run.
- Add more information to the web interface (version and timezone).

#### Bugs
- Added error logging for failed job key lookups in the api.
- Fixed log rotation for log files.
- Improved testing of robit by a slight amount.

## v0.4.3

#### Features
- Implemented logging to files and a better logging structure for debugging.

#### Bug Fix
- Correct issue with logging the wrong information if a job exhausts all of its retry attempts.

## v0.4.2

#### Features
- Added pytz to the project to provide support for daylight savings, timezones and all the other date goodness.

#### Changes
- Default timezone is now set to 'UTC'.
- Updated setup to include pytz as a dependency.

#### Bug Fixes
- Removed a default causing dates to set to UTC for mountain standard time.

## v0.4.1

#### Bug Fixes
- Fixed weird circular import that appears in certain versions of python.

## v0.4.0

#### Features
- All jobs can now access the worker object through the kwargs dictionary of any method in a job.
- Added alerts that allow you to have a method called when the health of the worker drops below a certain health threshold.
- Jobs now support retries. 
  - Use the retry_attempts argument when adding a job.

#### Changes
- Updated the web server api to now give more information.
  - /your-key/api/ - Provides basic worker information.
  - /your-key/api/worker/ - Provides worker and group information.
  - /your-kwy/api/job/id/ - Provide detailed job information.

#### Bug Fixes
- Better handling for exiting all processes.
- Job execution is now at the right second.
- Fixed job status to properly manage job execution from getting stuck in an infinite run cycle.

## v0.3.3

#### Features
- Cron now supports seconds by adding an additional parameter to the start of your cron string with the same functionality as minutes.

#### Changes
- Clock better supports a UTC adjustment now.
- You can now configure Robit's UTC globally.
- Monitor web interface has been removed.
- Worker web interface updates every second now.
- Removed socket communication in favor of shared memory communication.

#### Bug Fixes
- Health is now correctly updating.

## v0.3.2.3
- Deque for log record recording.
- Lower results log to 10 most recent records.

## v0.3.2.2
- Error handling when connecting to socket from client.

## v0.3.2.1
- Updating default socket port to 8100.

## v0.3.2
- Separate processes for web server.
- Socket communication for web server and worker.
- Queue for ready jobs.
- Thread pool executor for jobs.
- Class structure for modules.
- Cron Class Structure.

## v0.3.0
- Cron next date time bug fix.

## v0.3.0
- Switched from vue-petite.js to alpine.js.

## v2.3.0
- Stuff.