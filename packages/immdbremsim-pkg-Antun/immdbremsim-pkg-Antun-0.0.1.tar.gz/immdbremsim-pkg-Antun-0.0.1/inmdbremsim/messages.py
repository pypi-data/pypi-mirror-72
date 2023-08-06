
class DeviceStatuses(object):

    def __init__(self, flags):
        self.vmc_cc_ready = bool(flags[0])
        self.vmc_bl_ready = bool(flags[1])
        self.vmc_cl1_ready = bool(flags[2])
        self.vmc_cl2_ready = bool(flags[3])

        self.cc = bool(flags[4])
        self.bl = bool(flags[5])
        self.cl1 = bool(flags[6])
        self.cl2 = bool(flags[7])


class StatusMessage(object):

    def __init__(self, is_ok, msg):
        self.ok = is_ok
        self.msg = msg
