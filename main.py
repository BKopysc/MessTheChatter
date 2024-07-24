import multiprocessing
from mess_web import mess_host
from characterai_web import cai_host
import time

if __name__ == '__main__':
    try:
        users_queue = multiprocessing.Queue()
        bot_queue = multiprocessing.Queue()

        messenger_proc = multiprocessing.Process(target=mess_host.main, args=(users_queue, bot_queue))
        messenger_proc.start()
        cai_proc = multiprocessing.Process(target=cai_host.main, args=(users_queue, bot_queue))
        cai_proc.start()

        # Monitoring loop
        while True:
            if not messenger_proc.is_alive():
                print("Messenger process exited. Terminating CAI process...")
                cai_proc.terminate()
                break
            if not cai_proc.is_alive():
                print("CAI process exited. Terminating Messenger process...")
                messenger_proc.terminate()
                break
            time.sleep(1)  # Check every second

    except KeyboardInterrupt:
        print("Exiting...")
        messenger_proc.terminate()
        cai_proc.terminate()

    finally:
        messenger_proc.join()
        cai_proc.join()
        print("Exited")