# objects

| id    | INT  | PRIMARY KEY, Object ID       |
| value | TEXT | Raw argument value as Object |

# images

| id    | INT  | Object ID             |
| value | TEXT | Image Url, Image Path |

If the `value` is simply a URL or a Path, `objects` and `images` have one-to-one mapping.
In general, they are in one-to-many relation. For example, one tweet can have multiple photos.

# tags

| id  | INT  | Object ID |
| tag | TEXT | Tag name  |

