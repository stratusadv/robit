from robit import Monitor

mo = Monitor(
    name='Robit Example Monitor',
    key='Your-Own-Unique-Monitor-Key-That-Secure',
    utc_offset=-7,
)

if __name__ == '__main__':
    mo.start()
