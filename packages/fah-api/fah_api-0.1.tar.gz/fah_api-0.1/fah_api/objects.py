#!/usr/bin/env python3

from dateutil.parser import isoparse

class Error:
    def __init__(self, message=None):
        self.message = message

    def message(self):
        return self.message

    def __repr__(self):
        if self.message is None:
            return '<Error object message=None>'
        else:
            return '<Error object message=%s>' % self.message


class Options:
    def __init__(self, obj):
        self.child = bool(obj['child'])
        self.daemon = bool(obj['daemon'])
        self.fold_anon = bool(obj['fold-anon'])
        self.log_date = bool(obj['log-date'])
        # self.password = obj['password']
        if obj['password'] is not None:
            self.password_set = True
        else:
            self.password_set = False

        self.power = obj['power'] # LIGHT
        self.team = obj['team']
        self.user = obj['user']

    def to_dict(self):
        return { 
            'child': self.child,
            'daemon': self.daemon,
            'fold_anon': self.fold_anon,
            'log_date': self.log_date,
            # 'password': self.password,
            'password_set': self.password_set,
            'power': self.power,
            'team': self.team,
            'user': self.user,
        }

    def __repr__(self):
        return self.to_dict().__str__()


class Slot:
    def __init__(self, obj):
        self.id = int(obj['id'])
        self.status = obj['status']
        self.description = obj['description']
        self.options = obj['options']
        self.reason = obj['reason']
        self.idle = obj['idle']

    def to_dict(self):
        return { 
            'id': self.id,
            'status': self.status,
            'description': self.description,
            'options': self.options,
            'reason': self.reason,
            'idle': self.idle,
        }

    def __repr__(self):
        return self.to_dict().__str__()


class Unit:
    def __init__(self, obj):
        self.id = int(obj['id'])
        self.assigned = isoparse(obj['assigned'])
        self.attempts = obj['attempts']
        self.base_credit = int(obj['basecredit'])
        self.clone = obj['clone'] #int
        self.core = obj['core'] #hex?
        self.credit_estimate = int(obj['creditestimate'])
        self.cs = obj['cs']
        self.deadline = isoparse(obj['deadline'])
        self.error = obj['error'] #str
        self.eta = obj['eta'] #str
        self.frames_done = int(obj['framesdone'])
        self.gen = obj['gen'] #int
        self.next_attempt = obj['nextattempt']
        self.percent_done = float(obj['percentdone'][:-1]) / 100
        self.project = obj['project'] #int
        self.run = obj['run'] #int
        self.slot = int(obj['slot'])
        self.state = obj['state'] #str
        self.timeout = isoparse(obj['timeout'])
        self.time_remaining = obj['timeremaining']
        self.total_frames = int(obj['totalframes'])
        self.tpf = obj['tpf']
        self.unit = obj['unit'] #hex?
        self.waiting_on = obj['waitingon']
        self.ws = obj['ws']


    def to_dict(self):
        return {
            'id': self.id,
            'assigned': self.assigned,
            'attempts': self.attempts,
            'base_credit': self.base_credit,
            'clone': self.clone,
            'core': self.core,
            'credit_estimate': self.credit_estimate,
            'cs': self.cs,
            'deadline': self.deadline,
            'error': self.error,
            'eta': self.eta,
            'frames_done': self.frames_done,
            'gen': self.gen,
            'next_attempt': self.next_attempt,
            'percent_done': self.percent_done,
            'project': self.project,
            'run': self.run,
            'slot': self.slot,
            'state': self.state,
            'timeout': self.timeout,
            'time_remaining': self.time_remaining,
            'total_frames': self.total_frames,
            'tpf': self.tpf,
            'unit': self.unit,
            'waiting_on': self.waiting_on,
            'ws': self.ws,
        }


    def __repr__(self):
        return self.to_dict().__str__()
