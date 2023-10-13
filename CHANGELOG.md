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