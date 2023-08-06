#!/usr/bin/env python3

from fah_api.Connection import Connection

__connection = None
__password = None

def set_password(new_pass):
    global __password
    __password = new_pass

def heartbeat() -> int:
    return __basic_command('heartbeat')

def info() -> dict:
    return __basic_command('info')

def num_slots() -> int:
    return __basic_command('num-slots')

def options() -> dict:
    return __basic_command('options -a')

def pause(slot_id: int):
    __start_conversation()
    if slot_id is None:
        __send_command('pause')
    else:
        __send_command('pause %d' % (slot_id))
    __end_conversation()

def queue_info() -> list:
    return __basic_command('queue-info')

def save_all_options():
    __start_conversation()
    __send_command('save')
    __end_conversation()

def set_idle(idle :bool =True, slot_id :int =None):
    __start_conversation()
    if idle:
        if slot_id is None:
            __send_command('on_idle')
        else:
            __send_command('on_idle %d' % (slot_id))
    else:
        if slot_id is None:
            __send_command('always_on')
        else:
            __send_command('always_on %d' % (slot_id))
    __end_conversation()

def set_power(power):
    power = power.upper()
    if power != 'LIGHT' and power != 'MEDIUM' and power != 'FULL':
        raise Exception('Argument to set_power() must be LIGHT, MEDIUM, or FULL')
    __start_conversation()
    __send_command('options power="%s"' % (power))
    __send_command('save')
    __end_conversation()

def set_slot_option(slot_id :int, key, value):
    __start_conversation()
    opts = __send_command_and_parse('slot-options %d %s=%s' % (slot_id, key, value))
    __end_conversation()
    return opts

def slot_info() -> list:
    __start_conversation()
    slots = __send_command_and_parse('slot-info')
    for slot in slots:
        slot['options'] = __send_command_and_parse('slot-options %s -a' % slot['id'])
    __end_conversation()
    return slots

def unpause(slot_id :int):
    __start_conversation()
    if slot_id is None:
        __send_command('unpause')
    else:
        __send_command('unpause %d' % (slot_id))
    __end_conversation()

###

def __start_conversation():
    global __password
    conn = __get_connection()
    conn.read_data()
    if __password is not None:
        conn.write_data(b'auth %s\n' % (__password.encode('utf-8')))
        return conn.read_data()
    else:
        return None


def __get_connection():
    global __connection
    if __connection is None: __connection = Connection()
    return __connection


def __end_conversation():
    global __connection
    if __connection is not None: __connection.close()


def __basic_command(chars):
    __start_conversation()
    rval = __send_command_and_parse(chars)
    __end_conversation()
    return rval


def __send_command(chars):
    conn = __get_connection()
    conn.write_data(b'%s\n' % (chars.encode('utf-8')))
    conn.read_data()


def __send_command_and_parse(chars):
    conn = __get_connection()
    conn.write_data(b'%s\n' % (chars.encode('utf-8')))
    text = conn.read_data()
    pyon = conn.parse_pyon(text)
    return pyon
