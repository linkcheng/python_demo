import logging
import threading
 
def get_logger():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.DEBUG)
 
    fh = logging.FileHandler("threading_multi_logging.log")
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    logger.addHandler(fh)
    return logger
 
 
def doubler(number):
    """
    A function that can be used by a thread
    """
    logger = get_logger()
    logger.debug('doubler function executing')
    result = number * 2
    logger.debug('doubler function ended with: {}'.format(
        result))
 
 
if __name__ == '__main__':
    # logger = get_logger()
    thread_names = ['Mike', 'George', 'Wanda', 'Dingbat', 'Nina']
    for i in range(5):
        my_thread = threading.Thread(
            target=doubler, name=thread_names[i], args=(i,))
        my_thread.start()


