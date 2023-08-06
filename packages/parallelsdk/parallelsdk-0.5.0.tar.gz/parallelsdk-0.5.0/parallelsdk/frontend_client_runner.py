import logging
import ssl
import threading
try:
    import thread
except ImportError:
    import _thread as thread
import time
from threading import Thread, Lock, Condition
import websocket

k_default_web_socket_port = 8080
k_condition = Condition()
k_queue = []
k_current_model = None
k_process_completed = "__PROCESS_COMPLETED__"
k_health_message = "__HEALTH_CHECK_STATUS_OK__"
k_error_message = "__ERROR_MESSAGE__"
k_info_message = "__INFO_MESSAGE__"


def on_message(ws, message):
    global k_current_model
    global k_queue
    global k_condition
    if isinstance(message, str) and message.startswith(k_health_message):
        pass
    elif isinstance(message, str) and message.startswith(k_error_message):
        logging.info(message)
        print("Received an error message from the back-end server, return")
        return
    elif isinstance(message, str) and message.startswith(k_info_message):
        logging.info(message)
        print(message)
    else:
        if k_current_model is None:
            msg = "The model is not set, return"
            logging.info(msg)
            print(msg)
            return

        if isinstance(message, str) and message.startswith(k_process_completed):
            k_condition.acquire()

            # Append the message to the queue
            k_queue.append(message)
            k_condition.notify()
            k_condition.release()
        else:
            # Proceed in parsing the protobuf message
            k_current_model.on_message(message)


def on_error(ws, error):
    logging.error(error)
    print(error)


def on_close(ws):
    msg = "### Connection closed ###"
    logging.info(msg)


def on_open(ws):
    msg = "Client connected to back-end server"
    logging.info(msg)
    print(msg)


class FrontendClientRunner:
    address = ""
    port = 0
    websocket = None
    ws_url = ""

    def __init__(
            self,
            addr,
            port=k_default_web_socket_port,
            use_protobuf=True):
        # websocket.enableTrace(True)

        # Set port if defined, otherwise use standard port 8080
        self.port = port

        # Set the address
        self.address = addr

        # Prepare the full address
        if use_protobuf:
            self.ws_url = "ws://" + self.address + \
                ":" + str(self.port) + "/proto_service"
        else:
            self.ws_url = "ws://" + self.address + \
                ":" + str(self.port) + "/optilab_service"

    def connect_to_server_impl(self, wbsocket):
        # , sockopt=((socket.IPPROTO_TCP, socket.TCP_NODELAY),)
        wbsocket.run_forever(
            sslopt={
                "cert_reqs": ssl.CERT_NONE,
                "check_hostname": False})

    def connect_to_server(self):
        # websocket.enableTrace(True)
        logging.info("Connecting to back-end server...")
        # print(self.wsURL)
        header = {
            'Sec-WebSocket-Protocol': 'graphql-subscriptions'
        }
        try:
            self.websocket = websocket.WebSocketApp(self.ws_url,
                                                    header=header,
                                                    on_message=on_message,
                                                    on_error=on_error,
                                                    on_close=on_close)

            self.websocket.on_open = on_open

            # self.websocket.run_forever()
            th = threading.Thread(
                target=self.connect_to_server_impl, args=(
                    self.websocket, ), daemon=True)
            th.start()
        except BaseException:
            err_msg = "Cannot connect to the back-end server, return"
            logging.error(err_msg)
            return False
        return True

    def disconnect_from_server(self):
        # Initiate closing protocol with server
        if not self.websocket or not self.websocket.sock:
            return
        self.websocket.sock.send("__CLIENT_LOG_OFF__")

        # Wait to logoff from server
        time.sleep(1)
        try:
            self.websocket.sock.close()
        except BaseException:
            logging.info("Connection close and exception threw")
        finally:
            msg = "### Connection closed ###"
            print(msg)
        # self.websocket.sock.close()

    def send_message_to_backend_server(self, model):
        if self.websocket is None:
            logging.error("Client not connected to back-end server, return")
            return
        # Set the current global model and send the request to the back-end
        global k_current_model
        k_current_model = model
        self.websocket.sock.send_binary(model.serialize())

    def get_message_from_backend_server(self):
        global k_queue
        global k_condition
        k_condition.acquire()
        if not k_queue:
            k_condition.wait()
        msg = k_queue.pop(0)
        k_condition.notify()
        k_condition.release()
        return msg

    def wait_on_process_completion(self):
        msg = ""
        while msg != k_process_completed:
            msg = self.get_message_from_backend_server()

        # Give time for connections to close-up
        time.sleep(1)
