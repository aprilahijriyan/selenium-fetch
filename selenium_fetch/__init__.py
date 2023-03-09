from typing import Literal, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel
from pydantic.networks import AnyHttpUrl
from selenium.webdriver import Remote
import json
from functools import lru_cache

DictStrAny = dict[str, Any]

class FetchMode(str, Enum):
    CORS = "cors"
    NO_CORS = "no-cors"
    SAME_ORIGIN = "same-origin"
    NAVIGATE = "navigate"

class FetchCredentials(str, Enum):
    OMIT = "omit"
    SAME_ORIGIN = "same-origin"
    INCLUDE = "include"

class FetchCache(str, Enum):
    """
    https://developer.mozilla.org/en-US/docs/Web/API/Request/cache#value
    """
    DEFAULT = "default"
    NO_STORE = "no-store"
    RELOAD = "reload"
    NO_CACHE = "no-cache"
    FORCE_CACHE = "force-cache"
    ONLY_IF_CACHED = "only-if-cached"

class FetchRedirect(str, Enum):
    FOLLOW = "follow"
    ERROR = "error"
    MANUAL = "manual"

class FetchReferer(str, Enum):
    NO_REFERRER = "no-referrer"
    CLIENT = "client"

class FetchOptions(BaseModel):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    headers: DictStrAny = {}
    body: Union[DictStrAny, list[Any], Any]
    mode: FetchMode = FetchMode.CORS
    credentials: FetchCredentials = None
    cache: FetchCache = FetchCache.DEFAULT
    redirect: FetchRedirect = FetchRedirect.FOLLOW
    referrer: Optional[Union[FetchReferer, AnyHttpUrl]]
    referrerPolicy: Optional[str]
    integrity: Optional[str]
    keepalive: Optional[bool]
    priority: Literal["high", "low", "auto"] = "auto"

FETCH_JS_SCRIPT = """
var url = arguments[0];
var options = JSON.parse(arguments[1]);
var callback = arguments[arguments.length - 1];
async function dispatch() {
    var data = null;
    try {
        const resp = await fetch(url, options);
        data = {
            'headers': Object.fromEntries(resp.headers.entries()),
            'ok': resp.ok,
            'status': {
                'code': resp.status,
                'text': resp.statusText,
            },
            'text': await resp.text(),
        }
        callback(data);
    } catch (error) {
        callback(data);
    }
};
dispatch();
"""

class ResponseStatus(BaseModel):
    code: int
    text: Optional[str]

class Response(BaseModel):
    headers: DictStrAny
    ok: bool
    status: ResponseStatus
    text: str

@lru_cache(maxsize=1)
def get_browser_user_agent(driver: Remote) -> str:
    return driver.execute_script("return navigator.userAgent")

def fetch(driver: Remote, url: str, options: FetchOptions) -> Optional[Response]:
    opt = options.copy()
    if isinstance(options.body, (dict, list)):
        body = json.dumps(options.body)
        opt.body = body
        opt.headers["content-type"] = "application/json"

    opt_string = opt.json(exclude_none=True)
    result = driver.execute_async_script(FETCH_JS_SCRIPT, url, opt_string)
    if result:
        result = Response(**result)
    return result

# alias
Options = FetchOptions
