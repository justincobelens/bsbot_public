import time
import random


def wait(sleep_seconds=1):
    """ @wait(sleep_seconds=int)

        Sleeps after inner is called

        function -> sleep

        If you want to sleep before function, use @delay(delay_seconds=int)

     """

    def wrapper(func):
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(sleep_seconds)
            return result

        return inner

    return wrapper


def delay(delay_seconds=1):
    """ @delay(sleep_seconds=int)

        Sleeps before inner is called

        sleep -> function

        If you want to sleep after function, use @wait(delay_seconds=int)


     """

    def wrapper(func):
        def inner(*args, **kwargs):
            time.sleep(delay_seconds)
            result = func(*args, **kwargs)
            return result

        return inner

    return wrapper


def repeat(cycles=5):
    """
    @repeat(cycles=int)
    Repeats a function for the given amount of cycles until a result is found

    Could combine it with @wait or @delay:


    @repeat

    @wait

    def func(*args,**kwargs):

         """

    def wrapper(func):
        def inner(*args, **kwargs):
            result = False
            for _ in range(0, cycles):
                result = func(*args, **kwargs)
                if result:
                    return result
            return result

        return inner

    return wrapper


def timer(timeout=60, sleep=1):
    def wrapper(func):

        def inner(*args, **kwargs):
            start = time.time()
            while True:
                result = func(*args, **kwargs)
                print(f"result: {result}, timer: {time.time() - start}")
                if result:
                    return result

                elif time.time() - start > timeout:
                    print(f'Timed out after {timeout} seconds.')
                    return False

                time.sleep(sleep)

        return inner

    return wrapper


@timer(timeout=30, sleep=1)
def test():
    lst = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, False, False, False, False, False, False, False, False, False, False, False, False, False,
           False, False, 'string', 1, True, None]
    random.shuffle(lst)
    return lst[0]


if __name__ == "__main__":
    test()
