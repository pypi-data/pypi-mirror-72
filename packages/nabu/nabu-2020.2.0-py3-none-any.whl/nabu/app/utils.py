#
# Decorators and callback mechanism
#

def use_options(step_name, step_attr):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if step_name not in self.processing_steps:
                self.__setattr__(step_attr, None)
                return
            self._steps_name2component[step_name] = step_attr
            self._steps_component2name[step_attr] = step_name
            return func(*args, **kwargs)
        return wrapper
    return decorator


def pipeline_step(step_attr, step_desc):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.__getattribute__(step_attr) is None:
                return
            self.logger.info(step_desc)
            res = func(*args, **kwargs)
            self.logger.debug("End " + step_desc)
            callback = self._callbacks.get(self._steps_component2name[step_attr], None)
            if callback is not None:
                callback()
            return res
        return wrapper
    return decorator
