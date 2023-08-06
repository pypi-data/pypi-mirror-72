# youtubepy
youtubepy is a package to search for youtube videos through python code.

# Usage
```python
from youtubepy import Video
video = Video("me at the zoo")
result = video.search()
print(result)
> https://www.youtube.com/watch?v=A8AlbaDmaec
```

Attributes available for Video
```
search()
title()
channel_url()
thumbnail()
duration()
view_count()
like_count()
dislike_count()
average_rating()
```

Note - This package is currently under development