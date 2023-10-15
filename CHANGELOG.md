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