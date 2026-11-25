# Timestamp Microservice

A microservice that allows users to request a timestamp in various provided formats. Timestamps are based on the computer's timezone.

## Requirements

- Python 3.9+
- [pyzmq](https://pypi.org/project/pyzmq/)

```bash
pip install pyzmq
```

## Running the server

```bash
python timestamp.py
```

The server binds to `tcp://*:5560` and prints:

```
Listening on port: 5560
```

## Protocol

The server uses a ZeroMQ **REP** socket, so clients must use a **REQ** socket and send one request at a time. Every request gets exactly one reply.

### Available Commands

| Command             | Reply                                            | Example                       |
|---------------------|--------------------------------------------------|-------------------------------|
| `date_num`          | Date in number format                            | `02/21/2026`                  |
| `date_text`         | Date with month in text format                   | `February 21, 2026`           |
| `date_condensed`    | Date in number format with no spaces             | `02212026`                    |
| `date_underscore`   | Date in number format, separated by underscores  | `02_21_2026`                  |
| `month_day_num`     | Month & day in number format                     | `12/21`                       |
| `month_day_text`    | Month & day, with month in text format           | `December 21`                 |
| `month_num`         | Month as a number (01-12)                        | `03`                          |
| `month_text`        | Name of the current month                        | `March`                       |
| `day`               | Day as a number (01-31)                          | `20`                          |
| `weekday`           | Name of the current weekday                      | `Friday`                      |
| `year`              | Year (YYYY)                                      | `2026`                        |
| `24h_time`          | Time in 24 hour format                           | `14:30`                       |
| `12h_time`          | Time in 12 hour format                           | `02:30 PM`                    |
| `24h_datetime_num`  | Date & time in 24 hour format, month as a number | `09/22/2026 20:05`            |
| `24h_datetime_text` | Date & time in 24 hour format, month as text     | `September 22, 2026 at 20:05` |
| `12h_datetime_num`  | Date & time in 12 hour format, month as a number | `06/21/2026 04:24 AM`         |
| `12h_datetime_text` | Date & time in 12 hour format, month as text     | `June 21, 2026 at 04:24 AM`   |
| `quit`              | Closes the timestamp microservice                | `Service quitting...`         |

### Reply format

- **Success:** the requested timestamp
- **Invalid command:** `ERROR: Command '<invalid_command>' not recognized. Valid commands: <valid_commands>`
- **Shutdown:** `Service quitting...`

## Example client

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5560")

socket.send_string("weekday")
reply1 = socket.recv_string()
print(reply1)   # e.g. "Wednesday"

socket.send_string("quit")    # optional: shut the server down
reply2 = socket.recv_string()
print(reply2)   # "Service quitting..."
```
