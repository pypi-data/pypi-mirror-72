# -*- coding: utf-8 -*-
"""
@author: YagoDel

Modified from Odemis and patched together with nplab.instrument.Andor code
Copyright © 2012-2013 Éric Piel, Delmic

Useful links:
    ftp://ftp.piacton.com/Public/Manuals/Princeton%20Instruments/PVCAM%202.7%20Software%20User%20Manual.pdf
    https://github.com/delmic/odemis/blob/master/src/odemis/driver/pvcam.py
    http://www.pi-j.jp/pdf/manual/ST-133_ControllerManual.pdf
    https://github.com/nanophotonics/nplab/blob/master/nplab/instrument/ccd/pixis.py

This tries to support the PVCam SDK from Roper/Princeton Instruments/Photometrics.
However, the library is slightly different between the companies.
Original Odemis was tested on Linux with a PI PIXIS. This was tested on Windows with an ST133 controller

"""


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import


from builtins import str
from builtins import range
from builtins import object
import ctypes as ct
from nplab.instrument.camera.ST133 import *  # Dictionary linking metadata names with codes
import math
import numpy as np
import os
import threading
import time
from nplab.instrument.camera.camera_scaled_roi import CameraRoiScale, DisplayWidgetRoiScale
import nplab.datafile as df
from nplab.utils.notified_property import NotifiedProperty
from nplab.utils.gui import QtCore, QtGui, QtWidgets, uic
from nplab.utils.log import create_logger
from nplab.ui.ui_tools import UiTools
from nplab.utils.notified_property import register_for_property_changes
import operator
from . import pvcam_h as pv  # Dictionary linking variables with values
from weakref import WeakSet


def index_closest(val, l):
    """
    finds in a list the index of the closest existing value from a given value
    Works also with dict and tuples.
    """
    if isinstance(l, dict):
        return min(list(l.items()), key=lambda x: abs(x[1] - val))[0]
    else:
        return min(enumerate(l), key=lambda x: abs(x[1] - val))[0]


class PVCamError(Exception):
    def __init__(self, errno, strerror, *args, **kwargs):
        super(PVCamError, self).__init__(errno, strerror, *args, **kwargs)
        self.args = (errno, strerror)

    def __str__(self):
        return self.args[1]


class CancelledError(Exception):
    """
    raise to indicate the acquisition is cancelled and must stop
    """
    pass


class PVCamDLL(ct.WinDLL):
    """
    Subclass of CDLL specific to PVCam library, which handles error codes for
    all the functions automatically.
    It works by setting a default _FuncPtr.errcheck.
    """

    def __init__(self):
        if os.name == "nt":
            ct.WinDLL.__init__(self, "pvcam32")
            self.pl_pvcam_init()
        else:
            raise OSError('Operating system not recognised')
        #     # Global so that other libraries can access it
        #     # need to have firewire loaded, even if not used
        #     try:
        #         self.raw1394 = ct.CDLL("libraw1394.so.11", RTLD_GLOBAL)
        #         #self.pthread = CDLL("libpthread.so.0", RTLD_GLOBAL) # python already loads libpthread
        #         # TODO: shall we use  ctypes.util.find_library("pvcam")?
        #         CDLL.__init__(self, "libpvcam.so", RTLD_GLOBAL)
        #     except OSError:
        #         self._logger.exception("Failed to find the PVCam driver. You need to "
        #                           "check that libraw1394 and libpvcam are installed.")
        #         raise
        #     try:
        #         self.pl_pvcam_init()
        #     except PVCamError:
        #         pass # if opened several times, initialisation fails but it's all fine

    def pv_errcheck(self, result, func, *args):
        """
        Analyse the return value of a call and raise an exception in case of
        error.
        Follows the ctypes.errcheck callback convention
        """
        if not result:  # functions return (rs_bool = int) False on error
            try:
                err_code = self.pl_error_code()
            except Exception:
                raise PVCamError(0, "Call to %s failed" % func.__name__)
            # res = False
            try:
                err_mes = ct.create_string_buffer(pv.ERROR_MSG_LEN)
                res = self.pl_error_message(err_code, err_mes)
                if res:
                    raise PVCamError(result, "Call to %s failed with error code %d: %s" %
                                     (func.__name__, err_code, err_mes.value))
            except Exception:
                # if not res:
                raise PVCamError(result, "call to %s failed with unknown error code %d" %
                                     (func.__name__, err_code))

        return result

    def __getitem__(self, name):
        try:
            func = super(PVCamDLL, self).__getitem__(name)
        except Exception:
            raise AttributeError("Failed to find %s" % (name,))
        func.__name__ = name
        if name not in self.err_funcs:
            func.errcheck = self.pv_errcheck
        return func

    # names of the functions which are used in case of error (so should not
    # have their result checked
    err_funcs = ("pl_error_code", "pl_error_message", "pl_exp_check_status")

    def reinit(self):
        """
        Does a fast uninit/init cycle
        """
        try:
            self.pl_pvcam_uninit()
        except PVCamError:
            pass  # whatever
        try:
            self.pl_pvcam_init()
        except PVCamError:
            pass  # whatever

    def __del__(self):
        try:
            self.pl_pvcam_uninit()
        except:
            self._logger.exception("Failed during PVCam uninitialization")
            pass


# all the values that say the acquisition is in progress
STATUS_IN_PROGRESS = (pv.ACQUISITION_IN_PROGRESS, pv.EXPOSURE_IN_PROGRESS, pv.READOUT_IN_PROGRESS)

# The only way I've found to detect the camera is not responding is to check for
# weird camera temperature. However, it's pretty unreliable as depending on the
# camera, the weird temperature is different.
# It seems that the ST133 gives -120°C
TEMP_CAM_GONE = -120


class PvcamSdk(object):
    """
    Represents one PVCam camera and provides all the basic interfaces typical of
    a CCD/CMOS camera.
    This implementation is for the Roper/PI/Photometrics PVCam library... or at
    least for the PI version.

    Odemis tested on Linux with SDK 2.7, this was tested on Windows using the documentation found here:
    ftp://ftp.piacton.com/Public/Manuals/Princeton%20Instruments/PVCAM%202.7%20Software%20User%20Manual.pdf

    Be aware that the library resets almost all the values to their default
    values after initialisation. The library doesn't call the dimensions
    horizontal/vertical but serial/parallel (because the camera could be rotated).
    But we stick to: horizontal = serial (max = width - 1)
                     vertical = parallel (max = height - 1)

    Here area few more non-obvious requirements given by the PI technical
    support:
    * PIXIS, must allocate an even number of frame buffers.
    * One must not turn off or disconnect the camera with the camera open.
    * One must not call other PVCAM parameters such as PARAM_TEMP to get the
     current temperature during data collection. Only functions or parameters
     designated as 'online' may be called.
    * Order dependency issue: can't turn on continuous clean before external
     sync (strobed mode) is enabled.
    * InGaAs camera cannot do hardware binning

    Provides low-level methods corresponding to the SDK functions.
    """

    def __init__(self, device, *args, **kwargs):
        """
        Initialises the device
        device (int or string): number of the device to open, as defined in
         pvcam, cf scan(), or the name of the device (as in /dev/).
        Raise an exception if the device cannot be opened.
        """
        self.pvcam = PVCamDLL()
        self.current_image = None
        if "logger" in kwargs:
            self._logger = kwargs["logger"]
        elif not hasattr(self, "_logger"):
            self._logger = create_logger("PvcamSdk")
            self._logger.setLevel("DEBUG")

        # so that it's really not possible to use this object in case of error
        self._handle = None
        self._temp_timer = None
        # pick the right selection method depending on the type of "device"
        if isinstance(device, int):
            try:
                self._devname = self.cam_get_name(device)  # for reinit
            except PVCamError:
                raise Exception("Failed to find PI PVCam camera (%d)"
                                "Check the device is turned on and connected to "
                                "the computer. "
                                "You might need to turn it off and on again."
                                % (device))
        elif isinstance(device, str):
            # # check the file exists
            # if not os.path.exists("/dev/" + device):
            #     raise Exception("Failed to find PI PVCam camera %s (at %s). "
            #                   "Check the device is turned on and connected to "
            #                   "the computer. "
            #                   "You might need to turn it off and on again."
            #                   % (name, device))
            self._devname = device
        else:
            raise ValueError("Unexpected type for device: %s" % device)

        try:
            self._logger.info("Initializing camera, can be long (~15 s)...")
            self._handle = self.cam_open(self._devname, pv.OPEN_EXCLUSIVE)
            # raises an error if camera has a problem
            self.pvcam.pl_cam_get_diags(self._handle)
        except PVCamError as e:
            self._logger.info("PI camera seems connected but not responding, "
                              "you might want to try turning it off and on again.")
            print(e)
            raise IOError("Failed to open PVCam camera %s (%s)" % (device, self._devname))

        self._logger.info("Opened device %s successfully", device)

        # Describe the camera
        # up-to-date metadata to be included in dataflow
        # self._metadata = {MD_HW_NAME: self.getModelName()}

        # drivers
        self._swVersion = self.get_sw_version()
        self._hwVersion = self.get_hw_version()
        self.resolution = self.get_sensor_size()

        # setup everything best (fixed)
        self._prev_settings = [None, None, None, None, None]  # image, exposure, readout, gain, shutter period
        # Bit depth is between 6 and 16, but data is _always_ uint16
        self._shape = self.resolution + (2 ** self.get_param(pv.PARAM_BIT_DEPTH),)

        # put the detector pixelSize
        self.pixelSize = self.get_pixel_size()

        # to be used to separate acquisition and offline-only parameters (like PARAM_TEMP)
        # self._online_lock = threading.Lock()

        # Strong cooling for low (image) noise
        try:
            self.temperature = self.get_temp()
        except PVCamError:
            self._logger.debug("Camera doesn't seem to provide temperature information")

        self._setStaticSettings()

        # gain
        self._gains = self._get_gains()
        gain_choices = set(self._gains.values())
        self._gain = min(gain_choices)  # default to low gain (low noise)
        # self.gain = CameraParameter('gain')  # model.FloatEnumerated(self._gain, gain_choices, unit="", setter=self._setGain)
        self._set_gain(self._gain)

        # read out rate
        self._readout_rates = self._get_readout_rates()  # needed by _setReadoutRate()
        ror_choices = set(self._readout_rates.values())
        self._readout_rate = max(ror_choices)  # default to fast acquisition
        # self.readoutRate = model.FloatEnumerated(self._readout_rate, ror_choices,
        #                                          unit="Hz", setter=self._setReadoutRate)
        self._set_readout_rate(self._readout_rate)

        # binning is needed for _setResolution()
        self._binning = (1, 1)  # px
        max_bin = self._get_max_bin()
        self._image_rect = (0, self.resolution[0] - 1, 0, self.resolution[1] - 1)
        self._number_frames = 1

        self._min_res = self.get_min_resolution()
        minr = (int(math.ceil(self._min_res[0] / max_bin[0])),
                int(math.ceil(self._min_res[1] / max_bin[1])))
        # need to be before binning, as it is modified when changing binning
        #                   [self._transposeSizeToUser(minr),
        #                    self._transposeSizeToUser(resolution)],
        #                                      setter=self._setResolution)
        self._setResolution(self.resolution)
        self.background = np.zeros(self.resolution)

        # 2D binning is like a "small resolution"
        self.binning = self._binning  # model.ResolutionVA(self._transposeSizeToUser(self._binning),
        #                    [self._transposeSizeToUser((1, 1)),
        #                     self._transposeSizeToUser(max_bin)],
        #                                   setter=self._setBinning)

        # default values try to get live microscopy imaging more likely to show something
        try:
            minexp = self.get_param(pv.PARAM_EXP_MIN_TIME)  # s
        except PVCamError:
            # attribute doesn't exist
            minexp = 0  # same as the resolution
        minexp = max(1e-3, minexp)  # at least 1 x the exposure resolution (1 ms)
        # exposure is represented by unsigned int
        maxexp = (2 ** 32 - 1) * 1e-3  # s
        range_exp = (minexp, maxexp)  # s
        self._exposure_time = 0.01  # s
        # self.exposureTime = model.FloatContinuous(self.exposure, range_exp,
        #                                           unit="s", setter=self._setexposureTime)

        # To control the shutter: select the maximum frequency, aka minimum
        # period for the shutter. If it the acquisition time is below, the
        # shutter stays open all the time. So:
        # 0 => shutter always active
        # big value => shutter always opened
        self._shutter_period = 0.1
        # self.shutterMinimumPeriod = model.FloatContinuous(self._shutter_period, [0, 10],
        #                                       unit="s", setter=self._setShutterPeriod)
        self.acquisition_lock = threading.Lock()
        self.acquire_must_stop = threading.Event()
        self.acquire_thread = None
        # for synchronized acquisition
        self._cbuffer = None
        # self._got_event = threading.Event()
        # self._late_events = collections.deque() # events which haven't been handled yet

        self.data = None  # PVCamDataFlow(self)
        # Convenience event for the user to connect and fire
        # self.softwareTrigger = model.Event()
        self._logger.debug("Camera component ready to use.")

    def __del__(self):
        if self._temp_timer:
            self._temp_timer.cancel()
            self._temp_timer = None

        if self._handle is not None:
            # don't touch the temperature target/cooling

            # stop the acquisition thread if needed
            self.acquire_must_stop.set()
            # self.wait_stopped_flow()

            self._logger.debug("Shutting down the camera")
            self.pvcam.pl_cam_close(self._handle)
            self._handle = None
            del self.pvcam

    # Properties
    @NotifiedProperty
    def exposure(self):
        return self._exposure_time

    @exposure.setter
    def exposure(self, value):
        self._exposure_time = value

    @NotifiedProperty
    def number_frames(self):
        return self._number_frames

    @number_frames.setter
    def number_frames(self, value):
        self._number_frames = value

    def _setStaticSettings(self):
        """
        Set up all the values that we don't need to change after.
        Should only be called at initialisation
        """
        # Set the output amplifier to lowest noise
        try:
            # Try to set to low noise, if existing, otherwise: default value
            aos = self.get_enum_available(pv.PARAM_READOUT_PORT)
            if pv.READOUT_PORT_LOW_NOISE in aos:
                self.set_param(pv.PARAM_READOUT_PORT, pv.READOUT_PORT_LOW_NOISE)
            else:
                ao = self.get_param(pv.PARAM_READOUT_PORT, pv.ATTR_DEFAULT)
                self.set_param(pv.PARAM_READOUT_PORT, ao)
            self._output_amp = self.get_param(pv.PARAM_READOUT_PORT)
        except PVCamError:
            self._logger.debug("Failed to change readout speed")

        # Shutter mode (could be an init parameter?)
        try:
            # TODO: if the the shutter is in Pre-exposure mode, a short exposure
            # time can burn it.
            self.set_param(pv.PARAM_SHTR_OPEN_MODE, pv.OPEN_PRE_SEQUENCE)
        except PVCamError:
            self._logger.debug("Failed to change shutter mode")

        # Set to simple acquisition mode
        self.set_param(pv.PARAM_PMODE, pv.PMODE_NORMAL)
        # In PI cameras, this is fixed (so read-only)
        if self.get_param_access(pv.PARAM_CLEAR_MODE) == pv.ACC_READ_WRITE:
            self._logger.debug("Setting clear mode to pre sequence")
            # TODO: should be done pre-exposure? As we are not closing the shutter?
            self.set_param(pv.PARAM_CLEAR_MODE, pv.CLEAR_PRE_EXPOSURE)

        # set the exposure resolution. (choices are us, ms or s) => ms is best
        # for life imaging (us allows up to 71min)
        self.set_param(pv.PARAM_EXP_RES_INDEX, pv.EXP_RES_ONE_MILLISEC)

    # low level methods, wrapper to the actual SDK functions

    def Reinitialize(self):
        """
        Waits for the camera to reappear and reinitialise it. Typically
        useful in case the user switched off/on the camera.
        """
        # stop trying to read the temperature while we reinitialize
        if self._temp_timer is not None:
            self._temp_timer.cancel()
            self._temp_timer = None

        try:
            self.pvcam.pl_cam_close(self._handle)
        except PVCamError:
            pass
        self._handle = None

        # PVCam only update the camera list after uninit()/init()
        while True:
            self._logger.info("Waiting for the camera to reappear")
            self.pvcam.reinit()
            try:
                self._handle = self.cam_open(self._devname, pv.OPEN_EXCLUSIVE)
                break  # succeeded!
            except PVCamError:
                time.sleep(1)

        # reinitialise the sdk
        self._logger.info("Trying to reinitialise the camera %s...", self._devname)
        try:
            self.pvcam.pl_cam_get_diags(self._handle)
        except PVCamError:
            self._logger.info("Reinitialisation failed")
            raise

        self._logger.info("Reinitialisation successful")

        # put back the settings
        self._prev_settings = [None, None, None, None, None]
        self._setStaticSettings()
        
        # self.setTargetTemperature(self.targetTemperature.value)
        # self._temp_timer = util.RepeatingTimer(10, self.updateTemperatureVA,
        #                                  "PVCam temperature update")
        # self._temp_timer.start()

    def cam_get_name(self, num):
        """
        return the name, from the device number
        num (int >= 0): camera number
        return (string): name
        """
        assert (num >= 0)
        cam_name = ct.create_string_buffer(pv.CAM_NAME_LEN)
        self.pvcam.pl_cam_get_name(num, cam_name)
        return cam_name.value

    def cam_open(self, name, mode):
        """
        Reserve and initializes the camera hardware
        name (string): camera name
        mode (int): open mode
        returns (int): handle
        """
        handle = ct.c_int16()
        self.pvcam.pl_cam_open(name, ct.byref(handle), mode)
        return handle

    pv_type_to_ctype = {
        pv.TYPE_INT8: ct.c_int8,
        pv.TYPE_INT16: ct.c_int16,
        pv.TYPE_INT32: ct.c_int32,
        pv.TYPE_UNS8: ct.c_uint8,
        pv.TYPE_UNS16: ct.c_uint16,
        pv.TYPE_UNS32: ct.c_uint32,
        pv.TYPE_UNS64: ct.c_uint64,
        pv.TYPE_FLT64: ct.c_double,  # hopefully true on all platforms?
        pv.TYPE_BOOLEAN: ct.c_byte,
        pv.TYPE_ENUM: ct.c_uint32,
    }

    def get_param(self, param, value=pv.ATTR_CURRENT):
        """
        Read the current (or other) value of a parameter.
        Note: for the enumerated parameters, this it the actual value, not the
        index.
        param (int): parameter ID (cf pv.PARAM_*)
        value (int from pv.ATTR_*): which value to read (current, default, min, max, increment)
        return (value): the value of the parameter, whose type depend on the parameter
        """
        assert (value in (pv.ATTR_DEFAULT, pv.ATTR_CURRENT, pv.ATTR_MIN,
                          pv.ATTR_MAX, pv.ATTR_INCREMENT))

        # find out the type of the parameter
        tp = ct.c_uint16()
        self.pvcam.pl_get_param(self._handle, param, pv.ATTR_TYPE, ct.byref(tp))
        if tp.value == pv.TYPE_CHAR_PTR:
            # a string => need to find out the length
            count = ct.c_uint32()
            self.pvcam.pl_get_param(self._handle, param, pv.ATTR_COUNT, ct.byref(count))
            content = ct.create_string_buffer(count.value)
        elif tp.value in self.pv_type_to_ctype:
            # print 'Why?: ', tp.value
            content = self.pv_type_to_ctype[tp.value]()
        elif tp.value in (pv.TYPE_VOID_PTR, pv.TYPE_VOID_PTR_PTR):
            raise ValueError("Cannot handle arguments of type pointer")
        else:
            raise NotImplementedError("Argument of unknown type %d" % tp.value)

        # read the parameter
        self.pvcam.pl_get_param(self._handle, param, value, ct.byref(content))
        return content.value

    def get_param_access(self, param):
        """
        gives the access rights for a given parameter.
        param (int): parameter ID (cf pv.PARAM_*)
        returns (int): value as in pv.ACC_*
        """
        rights = ct.c_uint16()
        self.pvcam.pl_get_param(self._handle, param, pv.ATTR_ACCESS, ct.byref(rights))
        return rights.value

    def set_param(self, param, value):
        """
        Write the current value of a parameter.
        Note: for the enumerated parameter, this is the actual value to set, not
        the index.
        param (int): parameter ID (cf pv.PARAM_*)
        value (should be of the right type): value to write
        Warning: it seems to not always complain if the value written is incorrect,
        just using default instead.
        """
        # find out the type of the parameter
        tp = ct.c_uint16()
        self.pvcam.pl_get_param(self._handle, param, pv.ATTR_TYPE, ct.byref(tp))
        if tp.value == pv.TYPE_CHAR_PTR:
            content = str(value)
        elif tp.value in self.pv_type_to_ctype:
            # print tp.value
            content = self.pv_type_to_ctype[tp.value](value)
        elif tp.value in (pv.TYPE_VOID_PTR, pv.TYPE_VOID_PTR_PTR):
            raise ValueError("Cannot handle arguments of type pointer")
        else:
            raise NotImplementedError("Argument of unknown type %d" % tp.value)

        self.pvcam.pl_set_param(self._handle, param, ct.byref(content))

    def get_enum_available(self, param):
        """
        Get all the available values for a given enumerated parameter.
        param (int): parameter ID (cf pv.PARAM_*), it must be an enumerated one
        return (dict (int -> string)): value to description
        """
        count = ct.c_uint32()
        self.pvcam.pl_get_param(self._handle, param, pv.ATTR_COUNT, ct.byref(count))

        ret = {}  # int -> str
        for i in range(count.value):
            length = ct.c_uint32()
            content = ct.c_uint32()
            self.pvcam.pl_enum_str_length(self._handle, param, i, ct.byref(length))
            desc = ct.create_string_buffer(length.value)
            self.pvcam.pl_get_enum_param(self._handle, param, i, ct.byref(content),
                                         desc, length)
            ret[content.value] = desc.value
        return ret

    def exp_check_status(self):
        """
        Checks the status of the current exposure (acquisition)
        returns (int): status as in pv.* (cf documentation)
        """
        status = ct.c_int16()
        byte_cnt = ct.c_uint32()  # number of bytes already acquired: unused
        self.pvcam.pl_exp_check_status(self._handle, ct.byref(status), ct.byref(byte_cnt))
        return status.value

    @staticmethod
    def _int2version(raw):
        """
        Convert a raw value into version, according to the pvcam convention
        raw (int)
        returns (string)
        """
        ver = []
        ver.insert(0, raw & 0x0f)  # lowest 4 bits = trivial version
        raw >>= 4
        ver.insert(0, raw & 0x0f)  # next 4 bits = minor version
        raw >>= 4
        ver.insert(0, raw & 0xff)  # highest 8 bits = major version
        return '.'.join(str(x) for x in ver)

    def get_sw_version(self):
        """
        returns a simplified software version information
        or None if unknown
        """
        try:
            ddi_ver = ct.c_uint16()
            self.pvcam.pl_ddi_get_ver(ct.byref(ddi_ver))
            interface = self._int2version(ddi_ver.value)
        except PVCamError:
            interface = "unknown"

        try:
            pv_ver = ct.c_uint16()
            self.pvcam.pl_pvcam_get_ver(ct.byref(pv_ver))
            sdk = self._int2version(pv_ver.value)
        except PVCamError:
            sdk = "unknown"

        try:
            driver = self._int2version(self.get_param(pv.PARAM_DD_VERSION))
        except PVCamError:
            driver = "unknown"

        return "driver: %s, interface: %s, SDK: %s" % (driver, interface, sdk)

    def get_hw_version(self):
        """
        returns a simplified hardware version information
        """
        versions = {pv.PARAM_CAM_FW_VERSION: "firmware",
                    # Fails on PI pvcam (although PARAM_DD_VERSION manages to
                    # read the firmware version inside the kernel)
                    pv.PARAM_PCI_FW_VERSION: "firmware board",
                    pv.PARAM_CAM_FW_FULL_VERSION: "firmware (full)",
                    pv.PARAM_CAMERA_TYPE: "camera type",
                    }
        ret = ""
        for pid, name in list(versions.items()):
            try:
                value = self.get_param(pid)
                ret += "%s: %s " % (name, value)
            except PVCamError:
                #                self._logger.exception("param %x cannot be accessed", pid)
                pass  # skip

        # TODO: if we really want, we can try to look at the product name if it's
        # USB: from the name, find in in /dev/ -> read major/minor
        # -> /sys/dev/char/$major:$minor/device
        # -> read symlink canonically, remove last directory
        # -> read "product" file

        if ret == "":
            ret = "unknown"
        return ret

    def get_model(self):
        """
        returns (string): name of the camara
        """
        model_name = "Princeton Instruments camera"

        try:
            model_name += " with CCD '%s'" % self.get_param(pv.PARAM_CHIP_NAME)
        except PVCamError:
            pass  # unknown

        try:
            model_name += " (s/n: %s)" % self.get_param(pv.PARAM_SERIAL_NUM)
        except PVCamError:
            pass  # unknown

        return model_name

    def get_sensor_size(self):
        """
        return 2-tuple (int, int): width, height of the detector in pixel
        """
        width = self.get_param(pv.PARAM_SER_SIZE, pv.ATTR_DEFAULT)
        height = self.get_param(pv.PARAM_PAR_SIZE, pv.ATTR_DEFAULT)
        return width, height

    def get_min_resolution(self):
        """
        return 2-tuple (int, int): width, height of the minimum possible resolution
        """
        width = self.get_param(pv.PARAM_SER_SIZE, pv.ATTR_MIN)
        height = self.get_param(pv.PARAM_PAR_SIZE, pv.ATTR_MIN)
        return width, height

    def get_pixel_size(self):
        """
        return 2-tuple float, float: width, height of one pixel in m
        """
        # values from the driver are in nm
        width = self.get_param(pv.PARAM_PIX_SER_DIST, pv.ATTR_DEFAULT) * 1e-9
        height = self.get_param(pv.PARAM_PIX_PAR_DIST, pv.ATTR_DEFAULT) * 1e-9
        return width, height

    def get_temp(self):
        """
        returns (float) the current temperature of the captor in C
        """
        # it's in 1/100 of C
        # with self._online_lock:
        temp = self.get_param(pv.PARAM_TEMP) / 100
        return temp

    def get_temp_range(self):
        mint = self.get_param(pv.PARAM_TEMP_SETPOINT, pv.ATTR_MIN) / 100
        maxt = self.get_param(pv.PARAM_TEMP_SETPOINT, pv.ATTR_MAX) / 100
        return mint, maxt

    # High level methods
    def set_temp_target(self, temp):
        """
        Change the targeted temperature of the CCD. The cooler the less dark noise.
        temp (-300 < float < 100): temperature in C, should be within the allowed range
        """
        assert ((-300 <= temp) and (temp <= 100))
        # TODO: doublebuff_focus.c example code has big warnings to not read/write
        # the temperature during image acquisition. We might want to avoid it as
        # well. (as soon as the READOUT_COMPLETE state is reached, it's fine again)

        # it's in 1/100 of C
        # TODO: use increment? => doesn't seem to matter
        self.set_param(pv.PARAM_TEMP_SETPOINT, int(round(temp * 100)))

        # Turn off the cooler if above room temperature
        try:
            # Note: doesn't seem to have any effect on the PIXIS
            if temp >= 20:
                self.set_param(pv.PARAM_HEAD_COOLING_CTRL, pv.HEAD_COOLING_CTRL_OFF)
                self.set_param(pv.PARAM_COOLING_FAN_CTRL, pv.COOLING_FAN_CTRL_OFF)
            else:
                self.set_param(pv.PARAM_HEAD_COOLING_CTRL, pv.HEAD_COOLING_CTRL_ON)
                self.set_param(pv.PARAM_COOLING_FAN_CTRL, pv.COOLING_FAN_CTRL_ON)
        except PVCamError:
            pass

        temp = self.get_param(pv.PARAM_TEMP_SETPOINT) / 100
        return float(temp)

    def _get_gains(self):
        """
        Find the gains supported by the device
        returns (dict of int -> float): index -> multiplier
        """
        # Gains are special: they do not use a enum type, just min/max
        ming = self.get_param(pv.PARAM_GAIN_INDEX, pv.ATTR_MIN)
        maxg = self.get_param(pv.PARAM_GAIN_INDEX, pv.ATTR_MAX)
        gains = {}
        for i in range(ming, maxg + 1):
            # seems to be correct for PIXIS and ST133
            gains[i] = 2 ** (i - 1)
        return gains

    def _set_gain(self, value):
        """
        VA setter for gain (just save)
        """
        self._gain = value
        return value

    def _get_readout_rates(self):
        """
        Find the readout rates supported by the device
        returns (dict int -> float): for each index: frequency in Hz
        Note: this is for the current output amplifier and bit depth
        """
        # It depends on the port (output amplifier), bit depth, which we
        # consider both fixed.
        # PARAM_PIX_TIME (ns): the time per pixel
        # PARAM_SPDTAB_INDEX: the speed index
        # The only way to find out the rate of a speed, is to set the speed, and
        # see the new time per pixel.
        # Note: setting the spdtab idx resets the gain

        mins = self.get_param(pv.PARAM_SPDTAB_INDEX, pv.ATTR_MIN)
        maxs = self.get_param(pv.PARAM_SPDTAB_INDEX, pv.ATTR_MAX)
        # save the current value
        current_spdtab = self.get_param(pv.PARAM_SPDTAB_INDEX)
        current_gain = self.get_param(pv.PARAM_GAIN_INDEX)

        rates = {}
        for i in range(mins, maxs + 1):
            # Try with this given speed tab
            self.set_param(pv.PARAM_SPDTAB_INDEX, i)
            pixel_time = self.get_param(pv.PARAM_PIX_TIME)  # ns
            if pixel_time == 0:
                self._logger.warning("Camera reporting pixel readout time of 0 ns!")
                pixel_time = 1
            rates[i] = 1 / (pixel_time * 1e-9)

        # restore the current values
        self.set_param(pv.PARAM_SPDTAB_INDEX, current_spdtab)
        self.set_param(pv.PARAM_GAIN_INDEX, current_gain)
        return rates

    def _set_readout_rate(self, value):
        """
        VA setter for readout rate (just save)
        """
        self._readout_rate = value
        return value

    def _get_max_bin(self):
        """
        return the maximum binning in both directions
        returns (list of int): maximum binning in height, width
        """
        chip = self.get_param(pv.PARAM_CHIP_NAME)
        # FIXME: detect more generally if the detector supports binning or not?
        if "InGaAs" in chip:
            # InGaAs detectors don't support binning (written in the
            # specification). In practice, it stops sending images if binning > 1.
            return (1, 1)

        # other cameras seem to support up to the entire sensor resolution
        return self.get_sensor_size()

    def _set_binning(self, value):
        """
        Called when "binning" VA is modified. It also updates the resolution so
        that the AOI is approximately the same.
        value (int): how many pixels horizontally and vertically
         are combined to create "super pixels"
        """
        value = self._transposeSizeFromUser(value)
        prev_binning = self._binning
        self._binning = value

        # adapt resolution so that the AOI stays the same
        change = (prev_binning[0] / self._binning[0],
                  prev_binning[1] / self._binning[1])
        old_resolution = self._transposeSizeFromUser(self.resolution.value)
        new_resolution = (int(round(old_resolution[0] * change[0])),
                          int(round(old_resolution[1] * change[1])))

        self.resolution.value = self._transposeSizeToUser(new_resolution)  # will automatically call _storeSize
        return self._transposeSizeToUser(value)

    def _storeSize(self, size):
        """
        Check the size is correct (it should) and store it ready for SetImage
        size (2-tuple int): Width and height of the image. It will be centred
         on the captor. It depends on the binning, so the same region has a size
         twice smaller if the binning is 2 instead of 1. It must be a allowed
         resolution.
        """
        full_res = self._shape[:2]
        resolution = (int(full_res[0] // self._binning[0]),
                      int(full_res[1] // self._binning[1]))
        assert ((1 <= size[0]) and (size[0] <= resolution[0]) and
                (1 <= size[1]) and (size[1] <= resolution[1]))

        # Region of interest
        # center the image
        lt = ((resolution[0] - size[0]) // 2,
              (resolution[1] - size[1]) // 2)

        # the rectangle is defined in normal pixels (not super-pixels) from (0,0)
        self._image_rect = (lt[0] * self._binning[0], (lt[0] + size[0]) * self._binning[0] - 1,
                            lt[1] * self._binning[1], (lt[1] + size[1]) * self._binning[1] - 1)

    def _setResolution(self, value):
        # value = self._transposeSizeFromUser(value)
        new_res = self.resolutionFitter(value)
        self._storeSize(new_res)
        # return self._transposeSizeToUser(new_res)
        return new_res

    def resolutionFitter(self, size_req):
        """
        Finds a resolution allowed by the camera which fits best the requested
          resolution.
        size_req (2-tuple of int): resolution requested
        returns (2-tuple of int): resolution which fits the camera. It is equal
         or bigger than the requested resolution
        """
        # find maximum resolution (with binning)
        resolution = self._shape[:2]
        max_size = (int(resolution[0] // self._binning[0]),
                    int(resolution[1] // self._binning[1]))
        min_size = (int(math.ceil(self._min_res[0] / self._binning[0])),
                    int(math.ceil(self._min_res[1] / self._binning[1])))

        # smaller than the whole sensor
        size = (min(size_req[0], max_size[0]), min(size_req[1], max_size[1]))

        # bigger than the minimum
        size = (max(min_size[0], size[0]), max(min_size[0], size[1]))

        return size

    # def _setexposureTime(self, value):
    #     """
    #     Set the exposure time. It's automatically adapted to a working one.
    #     exp (0<float): exposure time in seconds
    #     returns the new exposure time
    #     """
    #     assert (0 < value)
    # 
    #     # The checks done in the VA should be enough
    #     # we cache it until just before the next acquisition
    #     self.exposure = value
    #     return self.exposure

    # def _setShutterPeriod(self, period):
    #     self._shutter_period = period
    #     return period

    def _need_update_settings(self):
        """
        returns (boolean): True if _update_settings() needs to be called
        """
        new_image_settings = self._binning + self._image_rect
        new_settings = [new_image_settings, self._exposure_time,
                        self._readout_rate, self._gain, self._shutter_period]
        return new_settings != self._prev_settings

    def _update_settings(self):
        """
        Commits the settings to the camera. Only the settings which have been
        modified are updated.
        Note: acquisition_lock must be taken, and acquisition must _not_ going on.
        returns (exposure, region, size):
                exposure: (float) exposure time in second
                region (pv.rgn_type): the region structure that can be used to set up the acquisition
                size (2-tuple of int): the size of the data array that will get acquired
        """
        (prev_image_settings, prev_exp_time,
         prev_readout_rate, prev_gain, prev_shut) = self._prev_settings

        if prev_readout_rate != self._readout_rate:
            self._logger.debug("Updating readout rate settings to %f Hz", self._readout_rate)
            i = index_closest(self._readout_rate, self._readout_rates)
            self.set_param(pv.PARAM_SPDTAB_INDEX, i)

            # self._metadata[MD_READOUT_TIME] = 1.0 / self._readout_rate  # s
            # rate might affect the BPP (although on the PIXIS, it's always 16)
            # self._metadata[MD_BPP] = self.get_param(pv.PARAM_BIT_DEPTH)

            # If readout rate is changed, gain is reset => force update
            prev_gain = None

        if prev_gain != self._gain:
            self._logger.debug("Updating gain to %f", self._gain)
            i = index_closest(self._gain, self._gains)
            self.set_param(pv.PARAM_GAIN_INDEX, i)
            # self._metadata[MD_GAIN] = self._gain

        # prepare image (region)
        region = pv.rgn_type()
        # region is 0 indexed
        region.s1, region.s2, region.p1, region.p2 = self._image_rect
        region.sbin, region.pbin = self._binning
        # self._metadata[MD_BINNING] = self._binning  # self._transposeSizeToUser(self._binning)
        new_image_settings = self._binning + self._image_rect
        # size = ((self._image_rect[1] - self._image_rect[0] + 1) // self._binning[0],
        #         (self._image_rect[3] - self._image_rect[2] + 1) // self._binning[1],
        #         self._number_frames)
        size = (self._number_frames,
                (self._image_rect[3] - self._image_rect[2] + 1) // self._binning[1],
                (self._image_rect[1] - self._image_rect[0] + 1) // self._binning[0]
                )

        # nothing special for the exposure time
        # self._metadata[MD_EXP_TIME] = self._exposure_time

        # Activate shutter closure whenever needed:
        # Shutter closes between exposures iif:
        # * period between exposures is long enough (>0.1s): to ensure we don't burn the mechanism
        # * readout time > exposure time/100 (when risk of smearing is possible)
        readout_time = np.prod(size) / self._readout_rate  # s
        tot_time = readout_time + self._exposure_time  # reality will be slightly longer
        self._logger.debug("exposure = %f s, readout = %f s", readout_time, self._exposure_time)
        try:
            if tot_time < self._shutter_period:
                self._logger.info("Disabling shutter because it would go at %g Hz",
                                  1 / tot_time)
                self.set_param(pv.PARAM_SHTR_OPEN_MODE, pv.OPEN_PRE_SEQUENCE)
            elif readout_time < (self._exposure_time / 100):
                self._logger.info("Disabling shutter because readout is %g times "
                                  "smaller than exposure",
                                  self._exposure_time / readout_time)
                self.set_param(pv.PARAM_SHTR_OPEN_MODE, pv.OPEN_PRE_SEQUENCE)
            elif self.get_param(pv.PARAM_SHTR_OPEN_MODE) != 0:
                self.set_param(pv.PARAM_SHTR_OPEN_MODE, pv.OPEN_PRE_EXPOSURE)
                self._logger.info("Shutter activated")
            else:
                self._logger.info("Shutter closed")
        except PVCamError:
            self._logger.debug("Failed to change shutter mode")

        self._prev_settings = [new_image_settings, self._exposure_time,
                               self._readout_rate, self._gain, self._shutter_period]

        return self._exposure_time, region, size

    def _allocate_buffer(self, length):
        """
        length (int): number of bytes requested by pl_exp_setup
        returns a cbuffer of the right type for an image
        """
        cbuffer = (ct.c_uint16 * (self._number_frames * length // 2))()  # empty array
        return cbuffer
    
    @staticmethod
    def _buffer_as_array(cbuffer, size):
        """
        Converts the buffer allocated for the image as an ndarray. zero-copy
        size (2-tuple of int): width, height
        return an ndarray
        """
        p = ct.cast(cbuffer, ct.POINTER(ct.c_uint16))
        # dataarray = np.ctypeslib.as_array(p, (size[2], size[1], size[0]))  # np shape is H, W
        dataarray = np.ctypeslib.as_array(p, size)  # np shape is H, W
        return dataarray  #

    # def start_flow(self, callback):
    #     """
    #     Set up the camera and acquireOne a flow of images at the best quality for the given
    #       parameters. Should not be called if already a flow is being acquired.
    #     callback (callable (DataArray) no return):
    #      function called for each image acquired
    #     """
    #     # if there is a very quick unsubscribe(), subscribe(), the previous
    #     # thread might still be running
    #     self.wait_stopped_flow() # no-op if the thread is not running
    #     self.acquisition_lock.acquire()
    #
    #     # Set up thread
    #     self.acquire_thread = threading.Thread(target=self._acquire_thread_run,
    #             name="PVCam acquire flow thread",
    #             args=(callback,))
    #     self.acquire_thread.start()

    def _init_seq(self):
        """Initialise sequence parameters"""

        exposure, region, size = self._update_settings()
        self.pvcam.pl_exp_init_seq()
        blength = ct.c_uint32()
        exp_ms = int(math.ceil(exposure * 1e3))  # ms
        # 1 image, with 1 region
        self.pvcam.pl_exp_setup_seq(self._handle, self._number_frames, 1, ct.byref(region),
                                    pv.TIMED_MODE, exp_ms, ct.byref(blength))
        self._logger.debug("acquisition setup report buffer size of %d", blength.value)
        cbuffer = self._allocate_buffer(blength.value)  # TODO shall allocate a new buffer every time?
        assert (blength.value / 2) >= (np.prod(size))

        readout_sw = np.prod(size) * 1.0 / self._readout_rate  # s
        # tends to be very slightly bigger:
        readout = self.get_param(pv.PARAM_READOUT_TIME) * 1e-3  # s
        self._logger.debug("exposure of %g s, readout %g s (expected %g s)", exp_ms * 1e-3, readout, readout_sw)
        duration = exposure + readout  # seems it actually takes +40ms
        return exposure, region, size, duration, cbuffer

    # def _acquire_thread_run(self, callback):
    #     """
    #     The core of the acquisition thread. Runs until acquire_must_stop is set.
    #     """
    #     need_init = True
    #     retries = 0
    #     cbuffer = None
    #     expected_end = 0
    #     readout = 0  # s
    #     try:
    #         while not self.acquire_must_stop.is_set():
    #             # need to stop acquisition to update settings
    #             if need_init or self._need_update_settings():
    #                 if cbuffer:
    #                     # finish the seq if it was started
    #                     self.pvcam.pl_exp_finish_seq(self._handle, cbuffer, None)
    #                     self.pvcam.pl_exp_uninit_seq()
    #
    #                 # With circular buffer, we could go about up to 10% faster, but
    #                 # everything is more complex (eg: odd buffer size will block the
    #                 # PIXIS), and not all hardware supports it. It would allow
    #                 # to do memory allocation during the acquisition, but would
    #                 # require a memcpy afterwards. So we keep it simple.
    #
    #                 exposure, region, size, duration, cbuffer = self._init_seq()
    #                 need_init = False
    #
    #             # Acquire the image
    #             # Note: might be unlocked slightly too early in case of must_stop,
    #             # but should be very rare and not too much of a problem hopefully.
    #             with self._online_lock:
    #                 self._start_acquisition(cbuffer)
    #                 start = time.time()
    #                 metadata = dict(self._metadata) # duplicate
    #                 metadata[MD_ACQ_DATE] = start
    #                 expected_end = start + duration
    #                 timeout = expected_end + 1
    #                 array = self._buffer_as_array(cbuffer, size, metadata)
    #
    #                 # wait a bounded time until the image is acquired
    #                 try:
    #                     # warning: in seq mode, it will only report once that status is done,
    #                     # and then automatically go to acquisition again
    #                     status = self.exp_check_status()
    #                     while status in STATUS_IN_PROGRESS:
    #                         now = time.time()
    #                         if now > timeout:
    #                             raise IOError("Timeout after %g s" % (now - start))
    #                         # check if we should stop (sleeping less and less)
    #                         left = expected_end - now
    #                         if self.acquire_must_stop.wait(max(0.01, left / 2)):
    #                             raise CancelledError()
    #                         status = self.exp_check_status()
    #
    #                     if status != pv.READOUT_COMPLETE:
    #                         raise IOError("Acquisition status is unexpected %d" % status)
    #                 except (IOError, PVCamError):
    #                     self.pvcam.pl_exp_abort(self._handle, pv.CCS_NO_CHANGE)
    #                     if retries > 5:
    #                         self._logger.error("Too many failures to acquire an image")
    #                         raise
    #
    #                     self._logger.exception("trying again to acquire image after error")
    #                     try:
    #                         self.pvcam.pl_exp_abort(self._handle, pv.CCS_HALT_CLOSE_SHTR)
    #                     except PVCamError:
    #                         pass
    #                     self._online_lock.release()
    #
    #                     self.pvcam.pl_exp_finish_seq(self._handle, cbuffer, None)
    #                     self.pvcam.pl_exp_uninit_seq()
    #
    #                     # Always assume the "worse": the camera has been turned off
    #                     self.Reinitialize() #returns only once the camera is working again
    #                     self._online_lock.acquire()
    #
    #                     retries += 1
    #                     cbuffer = None
    #                     need_init = True
    #                     continue
    #
    #             retries = 0
    #             self._logger.debug("image acquired successfully after %g s", time.time() - start)
    #             callback(self._transposeDAToUser(array))
    #
    #             # force the GC to non-used buffers, for some reason, without this
    #             # the GC runs only after we've managed to fill up the memory
    #             gc.collect()
    #     except CancelledError:
    #         # received a must-stop event
    #         pass
    #     except Exception:
    #         self._logger.exception("Unexpected failure during image acquisition")
    #     else:
    #         # we know it finished fine, so stop imediately
    #         # (also stop the pvcam background thread in _seq acquisition)
    #         self.pvcam.pl_exp_abort(self._handle, pv.CCS_HALT_CLOSE_SHTR)
    #     finally:
    #         # ending cleanly
    #
    #         # if end is soon, just wait for it (because the camera hates
    #         # being aborted during the end of acquisition (ie, during readout?)
    #         left = expected_end - time.time()
    #         # proportional to readout
    #         margin = max(readout * 2, 2) # at least 2s
    #         while left < margin and left > -1: # between margin s ahead up to 1 s late
    #             if not self.exp_check_status() in STATUS_IN_PROGRESS:
    #                 self._logger.debug("not aborting acquisition as it's already finished")
    #                 break
    #             time.sleep(0.01)
    #             left = expected_end - time.time()
    #         else:
    #             try:
    #                 if self.exp_check_status() in STATUS_IN_PROGRESS:
    #                     self._logger.debug("aborting acquisition, left = %g s", left)
    #                     self.pvcam.pl_exp_abort(self._handle, pv.CCS_HALT_CLOSE_SHTR)
    #             except PVCamError:
    #                 self._logger.exception("Failed to abort acquisition")
    #                 pass # status reported an error
    #
    #         # only required with multiple images, but just in case, we do it
    #         try:
    #             if cbuffer:
    #                 self.pvcam.pl_exp_finish_seq(self._handle, cbuffer, None)
    #         except PVCamError:
    #             self._logger.exception("Failed to finish the acquisition properly")
    #
    #         try:
    #             if cbuffer:
    #                 self.pvcam.pl_exp_uninit_seq()
    #         except PVCamError:
    #             self._logger.exception("Failed to finish the acquisition properly")
    #
    #         self.acquisition_lock.release()
    #         self._logger.debug("Acquisition thread closed")
    #         self.acquire_must_stop.clear()

    def capture(self):
        """Modified from odemis, but removing the locking"""
        exposure, region, size, duration, cbuffer = self._init_seq()
        self.pvcam.pl_exp_start_seq(self._handle, cbuffer)
        start = time.time()
        # metadata = dict(self._metadata)  # duplicate
        # metadata[MD_ACQ_DATE] = start
        expected_end = start + duration
        timeout = expected_end + 1

        # wait a bounded time until the image is acquired
        try:
            # warning: in seq mode, it will only report once that status is done,
            # and then automatically go to acquisition again
            status = self.exp_check_status()
            while status in STATUS_IN_PROGRESS:
                now = time.time()
                if now > timeout:
                    raise IOError("Timeout after %g s" % (now - start))
                # check if we should stop (sleeping less and less)
                left = expected_end - now
                if self.acquire_must_stop.wait(max(0.01, left / 2)):
                    raise CancelledError()
                status = self.exp_check_status()

            if status != pv.READOUT_COMPLETE:
                raise IOError("Acquisition status is unexpected %d" % status)
        except (IOError, PVCamError):
            try:
                self.pvcam.pl_exp_abort(self._handle, pv.CCS_HALT_CLOSE_SHTR)
            except PVCamError:
                self._logger.warn("Failed aborting")

        data_array = self._buffer_as_array(cbuffer, size)

        try:
            if cbuffer:
                self.pvcam.pl_exp_finish_seq(self._handle, cbuffer, None)
        except PVCamError:
            self._logger.exception("Failed to finish the acquisition properly")

        try:
            if cbuffer:
                self.pvcam.pl_exp_uninit_seq()
        except PVCamError:
            self._logger.exception("Failed to finish the acquisition properly")

        self.current_image = data_array

        return data_array

    def dark_exposure(self):
        _current_value = self.get_param(pv.PARAM_SHTR_OPEN_MODE)
        self.set_param(pv.PARAM_SHTR_OPEN_MODE, pv.OPEN_NEVER)
        array = self.capture()
        self.background = array
        self.set_param(pv.PARAM_SHTR_OPEN_MODE, _current_value)
        return array

    # def _start_acquisition(self, cbuf):
    #     """
    #     Triggers the start of the acquisition on the camera. If the DataFlow
    #      is synchronized, wait for the Event to be triggered.
    #     cbuf (ctype): buffer to contain the data
    #     raises CancelledError if the acquisition must stop
    #     """
    #     assert cbuf
    #
    #     # catch up late events if we missed the start
    #     if self._late_events:
    #         event_time = self._late_events.pop()
    #         self._logger.warning("starting acquisition late by %g s", time.time() - event_time)
    #         self.pvcam.pl_exp_start_seq(self._handle, cbuf)
    #         return
    #
    #     self._cbuffer = cbuf
    #     try:
    #         # wait until onEvent was called (it will directly start acquisition)
    #         # or must stop
    #         while not self.acquire_must_stop.is_set():
    #             if not self.data._sync_event: # not synchronized (anymore)?
    #                 self._logger.debug("starting acquisition")
    #                 self.pvcam.pl_exp_start_seq(self._handle, cbuf)
    #                 return
    #             # doesn't need to be very frequent, just not too long to delay
    #             # cancelling the acquisition, and to check for the event frequently
    #             # enough
    #             if self._got_event.wait(0.01):
    #                 self._got_event.clear()
    #                 return
    #     finally:
    #         self._cbuffer = None
    #
    #     raise CancelledError()

    # @oneway
    # def onEvent(self):
    #     """
    #     Called by the Event when it is triggered
    #     """
    #     cbuf = self._cbuffer
    #     # FIXME: there is a small chance for race conditions:
    #     # (onEvent) cbuf is None
    #     # (start acq) no late_events
    #     # (start acq) set cbuf
    #     # (start acq) wait
    #     # (onEvent) add late events & return
    #     # => need lock (or something else?)
    #     if not cbuf:
    #         if self.acquire_thread and self.acquire_thread.isAlive():
    #             self._logger.warning("Received synchronization event but acquisition not ready")
    #             # queue the events, it's bad but less bad than skipping it
    #             self._late_events.append(time.time())
    #         return
    #
    #     self._logger.debug("starting sync acquisition")
    #     self.pvcam.pl_exp_start_seq(self._handle, cbuf)
    #     self._got_event.set() # let the acquisition thread know it's starting
    #
    # def req_stop_flow(self):
    #     """
    #     Cancel the acquisition of a flow of images: there will not be any notify() after this function
    #     Note: the thread should be already running
    #     Note: the thread might still be running for a little while after!
    #     """
    #     assert not self.acquire_must_stop.is_set()
    #     self.acquire_must_stop.set()
    #
    # def wait_stopped_flow(self):
    #     """
    #     Waits until the end acquisition of a flow of images. Calling from the
    #      acquisition callback is not permitted (it would cause a dead-lock).
    #     """
    #     if not self.acquire_thread: # no thread ever created
    #         return
    #
    #     # "if" is to not wait if it's already finished
    #     if self.acquire_must_stop.is_set():
    #         self.acquire_thread.join(20) # 20s timeout for safety
    #         if self.acquire_thread.isAlive():
    #             raise OSError("Failed to stop the acquisition thread")
    #         # ensure it's not set, even if the thread died prematurately
    #         self.acquire_must_stop.clear()

    @staticmethod
    def scan():
        """
        List all the available cameras.
        Note: it's not recommended to call this method when cameras are being used
        return (list of 2-tuple: name (strin), device number (int))
        """
        pvcam = PVCamDLL()
        num_cam = ct.c_short()
        pvcam.pl_cam_get_total(ct.byref(num_cam))
        print("Found %d devices." % num_cam.value)

        cameras = []
        for i in range(num_cam.value):
            cam_name = ct.create_string_buffer(pv.CAM_NAME_LEN)
            try:
                pvcam.pl_cam_get_name(i, cam_name)
            except PVCamError:
                print("Couldn't access camera %d" % i)

            # TODO: append the resolution to the name of the camera?
            cameras.append((cam_name.value, {"device": i}))

        return cameras


class Pvcam(CameraRoiScale, PvcamSdk):
    metadata_property_names = ('exposure', 'binning', 'roi')

    def __init__(self, device, **kwargs):
        # super(Pvcam, self).__init__(device, logger=self._logger)
        CameraRoiScale.__init__(self)
        PvcamSdk.__init__(self, device, logger=self._logger)
        self.background = None
        self.backgrounded = False

    def raw_snapshot(self):
        """
        If only one frame, returns a 2D array. If multiple frames, returns a 3D array, where the first dimension is
        frame number
        :return: ndarray
        """
        array = self.capture()
        if array.shape[0] == 1:
            array = array[0]
        return True, array

    def filter_function(self, frame):
        if self.backgrounded:
            return np.asarray(frame, float) - np.asarray(self.background, float)
        else:
            return frame

    def get_camera_parameter(self, parameter_name):
        return self.get_param(getattr(pv, parameter_name))

    def set_camera_parameter(self, parameter_name, parameter_value):
        try:
            self.set_param(getattr(pv, parameter_name), getattr(pv, parameter_value))
        except Exception as e:
            self._logger.warn('paramter ' +parameter_name+' could not be set with the value '+parameter_value+
                     ' due to error '+str(e))

    def get_control_widget(self):
        return pvcamUI(self)

    def get_preview_widget(self):
        self._logger.debug('Getting preview widget')
        if self._preview_widgets is None:
            self._preview_widgets = WeakSet()
        new_widget = DisplayWidgetRoiScale()
        self._preview_widgets.add(new_widget)

        return new_widget

    @NotifiedProperty
    def roi(self):
        return self._image_rect

    @roi.setter
    def roi(self, value):
        self._image_rect = value

    @property
    def binning(self):
        return self._binning

    @binning.setter
    def binning(self, value):
        self._binning = value


class pvcamUI(QtWidgets.QWidget, UiTools):

    def __init__(self, camera):
        assert isinstance(camera, Pvcam), "instrument must be an camera"
        self._logger = create_logger("pvcam.GUI")

        super(pvcamUI, self).__init__()
        self.captureThread = None
        self.camera = camera
        self.DisplayWidget = None

        self._binning_changed = False
        self._prev_bin = camera.binning

        uic.loadUi((os.path.dirname(__file__) + '/camera.ui'), self)
        self._setup_signals()
        self.data_file = None
        self.save_all_parameters = False
        self.backgrounded = False

        self._func_dict = {}
        for param in self.camera.metadata_property_names:
            try:
                func = self.callback_to_update_prop(param)
                self._func_dict[param] = func
                register_for_property_changes(self.camera, param, self._func_dict[param])
            except AssertionError:
                self._logger.info("%s is not a property so cannot be monitored" % param)
        # register_for_property_changes(self.camera, "latest_raw_frame", self.update_image)

    def __del__(self):
        self._stopTemperatureThread = True
        if self.DisplayWidget is not None:
            self.DisplayWidget.hide()
            self.DisplayWidget.close()

    def _setup_signals(self):
        # self.comboBoxAcqMode.activated.connect(self.AcquisitionModeChanged)
        # self.comboBoxReadMode.activated.connect(self.ReadModeChanged)
        # self.comboBoxTrigMode.activated.connect(self.TrigChanged)
        # self.spinBoxNumFrames.valueChanged.connect(self.NumFramesChanged)
        # self.spinBoxNumFrames.setRange(1, 1000000)
        # self.spinBoxNumAccum.valueChanged.connect(self.NumAccumChanged)
        # self.spinBoxNumRows.valueChanged.connect(self.NumRowsChanged)
        # self.spinBoxCenterRow.valueChanged.connect(self.NumRowsChanged)
        self.checkBoxROI.stateChanged.connect(self.ROI)
        # self.checkBoxCrop.stateChanged.connect(self.IsolatedCrop)
        # self.checkBoxCooler.stateChanged.connect(self.Cooler)
        # # self.checkBoxAutoExp.stateChanged.connect(self.AutoExpose)
        # self.checkBoxEMMode.stateChanged.connect(self.OutputAmplifierChanged)
        # self.spinBoxEMGain.valueChanged.connect(self.EMGainChanged)
        self.lineEditExpT.editingFinished.connect(self.changed_exposure)
        # self.lineEditExpT.setValidator(QtGui.QDoubleValidator())
        self.pushButtonDiv5.clicked.connect(lambda: self.changed_exposure('/'))
        self.pushButtonTimes5.clicked.connect(lambda: self.changed_exposure('x'))
        self.spinBox_binx.valueChanged.connect(self.changed_binning)
        self.spinBox_biny.valueChanged.connect(self.changed_binning)

        self.pushButtonCapture.clicked.connect(self.Capture)
        self.pushButtonLive.clicked.connect(self.Live)
        self.pushButtonAbort.clicked.connect(self.Abort)
        self.save_pushButton.clicked.connect(self.Save)
        self.pushButtonTakeBG.clicked.connect(self.take_background)
        self.checkBoxRemoveBG.stateChanged.connect(self.remove_background)
        # self.referesh_groups_pushButton.clicked.connect(self.update_groups_box)

    def update_exposure(self, value):
        self.lineEditExpT.setText(str(value))

    def update_binning(self, value):
        self._binning_changed = True
        self.spinBox_binx.setValue(value[0])
        self.spinBox_biny.setValue(value[1])

    def callback_to_update_prop(self, propname):
        """Return a callback function that refreshes the named parameter."""

        def callback(value=None):
            # print 'Callback: ', propname
            getattr(self, 'update_' + propname)(value)

        return callback

    def changed_binning(self):
        if not self._binning_changed:
            self._binning_changed = True
            self._prev_bin = self.camera.binning
        xbin = self.spinBox_binx.value()
        ybin = self.spinBox_biny.value()
        self.camera.binning = (xbin, ybin)

    def changed_exposure(self, variable=None):
        if variable is None:
            exp_time = float(self.lineEditExpT.text())
        elif variable == 'x':
            exp_time = float(self.lineEditExpT.text()) * 5
        elif variable == '/':
            exp_time = float(self.lineEditExpT.text()) / 5
        else:
            raise ValueError("Unrecognised exposure time")
        self.camera.exposure = exp_time
        self.update_exposure(exp_time)

    def take_background(self):
        # self.camera.background = self.camera.dark_exposure()
        self.camera.dark_exposure()
        self.backgrounded = True
        self.checkBoxRemoveBG.setChecked(True)

    def remove_background(self):
        if self.checkBoxRemoveBG.isChecked():
            self.camera.backgrounded = True
        else:
            self.camera.backgrounded = False

    def Save(self):
        if self.data_file is None:
            self.data_file = df.current()
        data = self.camera.current_image

        if self.lineEdit_groupname.text():
            group = self.data_file.create_group(self.lineEdit_groupname.text())
        else:
            group = self.data_file

        if self.lineEdit_datasetname.text():
            dataset_name = self.lineEdit_datasetname.text()
        else:
            idx = 1
            while "pvcam%d" % idx in list(group.keys()):
                idx += 1
            dataset_name = "pvcam%d" % idx

        if self.backgrounded:
            self._logger.info("Saving backgrounded image. Remember to save the background separately")
            data = np.array(data, np.float)
            data -= self.camera.background

        try:
            data_set = group.create_dataset(name=dataset_name, data=data)
            if self.checkBox_attrs.isChecked():
                attrs = dict()
                for param in self.camera.metadata_property_names:
                    attrs[param] = getattr(self.camera, param)
                if self.description_plainTextEdit.toPlainText():
                    attrs['Description'] = self.description_plainTextEdit.toPlainText()
                df.attributes_from_dict(data_set, attrs)
        except Exception as e:
            self._logger.warn(e)

    def ROI(self):
        if self.checkBoxROI.isChecked():
            self.camera.roi = self.camera.gui_roi
        else:
            shape = self.camera._shape
            self.camera.roi = (0, shape[0] - 1, 0, shape[1] - 1)

    def Capture(self):
        self.camera.raw_image(update_latest_frame=True)

    def Live(self):
        self.camera.live_view = True

    def Abort(self):
        self.camera.live_view = False
