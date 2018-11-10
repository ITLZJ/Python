#------------------Bird Code----------------------------
#线程清理
import inspect
import ctypes
def _async_raise(tid, exctype):
    """引发异常，需要执行清理"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("线程ID无效")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc Error")
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
