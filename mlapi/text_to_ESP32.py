import socket

def send_to_ESP32(message):
    # connect to the esp32 socket
    sock = socket.socket()

    try:
        sock.connect(("microphone.local", 5002))
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        
        # Send the message
        sock.sendall(message.encode('utf-8'))
        
    except Exception as e:
        print(f"Failed to connect or send message: {e}")
        
    #finally:
    #    sock.close()


send_to_ESP32("Hello, ESP32!")
