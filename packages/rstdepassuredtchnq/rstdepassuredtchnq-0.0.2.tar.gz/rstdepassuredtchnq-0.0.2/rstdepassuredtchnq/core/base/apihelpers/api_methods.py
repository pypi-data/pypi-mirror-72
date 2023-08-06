from rstdepassuredtchnq.core.base.apihelpers.request_methods import BaseAPIHelper
from rstdepassuredtchnq.core.base.format.pretty_base import PrettyFormat
from rstdepassuredtchnq.core.base.log.custom_logger import get_logger


class APIMethods(BaseAPIHelper):
    pretty_format = PrettyFormat()
    log = get_logger("APIMethods")
