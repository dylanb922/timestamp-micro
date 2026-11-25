from datetime import datetime
import zmq

timestamp_formats = {
    "date_num": "%m/%d/%Y",
    "date_text": "%B %d, %Y",
    "month_day_num": "%m/%d",
    "month_day_text": "%B %d",
    "month_num": "%m",
    "month_text": "%B",
    "day": "%d",
    "weekday": "%A",
    "year": "%Y",
    "12h_time": "%I:%M %p",
    "24h_time": "%H:%M",
    "24h_datetime_num": "%m/%d/%Y %H:%M",
    "24h_datetime_text": "%B %d, %Y %H:%M",
    "12h_datetime_num": "%m/%d/%Y %I:%M %p",
    "12h_datetime_text": "%B %d, %Y at %I:%M %p"
}

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5560")
    print("Listening on port: 5560")

    try:
        while True:
            request = socket.recv_string().strip().lower()

            stamp_format = timestamp_formats.get(request)

            # Ensure format is valid & catch invalid commands
            if stamp_format:
                reply = datetime.now().strftime(stamp_format)
            else:
                valid_formats = ", ".join(timestamp_formats.keys())
                reply = f"ERROR: Command '{request}' not recognized. Valid commands: {valid_formats}"

            socket.send_string(reply)
    finally:
        print("Shutting down service...")
        socket.close()
        context.term()

if __name__ == "__main__":
    main()