import os
from typing import Optional

def this_video_exists(path: Optional[str]) -> bool:
    if not path:
        return False
    return os.path.exists(path) and os.path.isfile(path)