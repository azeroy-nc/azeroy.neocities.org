# coding: utf-8
"""
The primary data dictionary uses the following format:
  {
    "item-id": {
      ...item data
    },
    "item2-id": {
      ...item data
    },
  }

This utility can convert the input data files into an HTML table.
"""

class AlbumTrack:
    def __init__(self, parent, id, data):
        self.parent = parent
        self.id = str(id)
        self.data = data

        required_keys = ['title', 'track_number']
        for key in required_keys:
            if key not in data:
                raise KeyError(f'item {self.id} (of {parent.id}) missing required key {key}')

    def format(self, value):
        if value == 'title':
            return self.title
        elif value == 'track_number':
            return self.track_number
        elif value == 'length':
            return self.length
        elif value == 'links':
            return self.links
        elif value == 'notes':
            return self.notes
        elif value == 'original_description':
            return self.original_description
        elif value == 'sources':
            return self.sources

    @property
    def account(self):
        return self.parent.account

    @property
    def track_number(self):
        return self.data['track_number']

    @property
    def title(self):
        return self.data['title']

    @property
    def length(self):
        try:
            _length = int(self.data['length'])
        except KeyError:
            return None

        # Get human-readable version of length
        length_min, length_sec = divmod(_length, 60)
        length_hour, length_min = divmod(length_min, 60)

        if length_hour:
            length_readable = '{h}∶{m}∶{s}'.format(
                h=str(length_hour).rjust(2, '0'),
                m=str(length_min).rjust(2, '0'),
                s=str(length_sec).rjust(2, '0')
            )
        else:
            length_readable = '{m}∶{s}'.format(
                m=str(length_min).rjust(2, '0'),
                s=str(length_sec).rjust(2, '0')
            )

        return length_readable

    @property
    def links(self):
        try:
            return self.data['links']
        except KeyError:
            return None

    @property
    def notes(self):
        try:
            return self.data['notes']
        except KeyError:
            return None

    @property
    def sources(self):
        try:
            return self.data['sources']
        except KeyError:
            return None

    @property
    def original_description(self):
        try:
            return self.data['original_description']
        except KeyError:
            return None

class Item:
    """
    A class representing an item (song, album/ep or video).
    """
    def __init__(self, item_type, id, data=None):
        self.item_type = item_type
        self.id = str(id)
        self.data = data

        required_keys = ['title', 'type', 'status']
        for key in required_keys:
            if key not in data:
                raise KeyError(f'item "{self.id}" missing required key "{key}"')

        if (item_type == 'video' and self.type not in ['lore', 'mv', 'misc']) or \
                (item_type == 'music' and self.type not in ['single', 'ep', 'album']):
            raise ValueError('invalid type "{type}" for item "{id}"'.format(type=_type, id=self.id))

        if self.type in ['ep', 'album'] and 'tracks' not in self.data:
            raise KeyError(f'item "{self.id}" missing required key "tracks"')

        if self.status != 'lost' and 'links' not in self.data:
            print(f'WARNING: no links in item "{self.id}"')

        #if 'release_date' not in self.data:
        #   print(f'WARNING: item {self.id} missing release date; assuming lost!')

    def __str__(self):
        return f'Item {self.id}: {self.title}'

    def format(self, value):
        if value == 'title':
            return self.title
        elif value == 'type':
            return self.type
        elif value == 'account':
            return self.account
        elif value == 'channel':
            return self.channel
        elif value == 'status':
            return self.status
        elif value == 'length':
            return self.length
        elif value == 'release_date':
            return self.release_date
        elif value == 'links':
            return self.links
        elif value == 'content_warnings':
            return self.content_warnings
        elif value == 'notes':
            return self.notes
        elif value == 'original_description':
            return self.original_description
        elif value == 'sources':
            return self.sources
        elif value == 'series':
            return self.series
        elif value == 'tracks':
            return self.tracks
        elif value == 'views':
            return self.views
        elif value == 'plays':
            return self.plays

    @property
    def title(self):
        return self.data['title']

    @property
    def account(self):
        return self.data['account']

    @property
    def account_readable(self):
        if self.data['account'] == 'yabujin':
            return 'YABUJIN'
        elif self.data['account'] == 'gyrotta':
            return 'DJ GYROTTA ZAO'
        return self.data['account']

    @property
    def status(self):
        return self.data['status']

    @property
    def thumbnail(self):
        try:
            return self.data['thumbnail']
        except KeyError:
            return None

    @property
    def links(self):
        try:
            return self.data['links']
        except KeyError:
            return None

    @property
    def content_warnings(self):
        try:
            return self.data['content_warnings']
        except KeyError:
            return None

    @property
    def type(self):
        return self.data['type']

    @property
    def release_date(self):
        # This is either:
        #  - a tuple containing the YEAR, MONTH and DAY, or
        #  - None if the date is unknown.
        # The MONTH or DAY can be set to 0 if they're not known.
        try:
            _date = self.data['release_date']
            assert _date
        except (KeyError, AssertionError):
            return None

        if _date and len(_date) != 3:
            error = (len(_date) > 3 and 'more') or 'less'
            raise ValueError('release_date tuple in item "{id}" has {error} than 3 items'.format(id=self.id, error=error))

        if not _date:
            return None
        elif str(_date[1]) == '0':
            return _date[0]
        return '{y}-{m}-{d}'.format(
            y=str(_date[0]).rjust(2, '0'),
            m=str(_date[1]).rjust(2, '0'),
            d=str(_date[2]).rjust(2, '0'),
            )

        return _date

    @property
    def length(self):
        try:
            _length = int(self.data['length'])
        except KeyError:
            return None

        # Get human-readable version of length
        length_min, length_sec = divmod(_length, 60)
        length_hour, length_min = divmod(length_min, 60)

        if length_hour:
            length_readable = '{h}∶{m}∶{s}'.format(
                h=str(length_hour).rjust(2, '0'),
                m=str(length_min).rjust(2, '0'),
                s=str(length_sec).rjust(2, '0')
            )
        else:
            length_readable = '{m}∶{s}'.format(
                m=str(length_min).rjust(2, '0'),
                s=str(length_sec).rjust(2, '0')
            )

        return length_readable

    @property
    def original_description(self):
        try:
            _original_description = self.data['original_description']
        except KeyError:
            return None

        return str(_original_description)

    @property
    def notes(self):
        try:
            return self.data['notes']
        except KeyError:
            return None

    @property
    def sources(self):
        try:
            return self.data['sources']
        except KeyError:
            return None

    @property
    def series(self):
        try:
            return self.data['series']
        except KeyError:
            return None

    @property
    def tracks(self):
        if self.type not in ['ep', 'album']:
            return None

        try:
            _tracks = self.data['tracks']
        except KeyError:
            raise KeyError('item "{id}" missing required key "tracks"'.format(id=self.id))

        output = []
        for track_id, track in _tracks.items():
            output.append(AlbumTrack(self, track_id, track))

        return output

    @property
    def views(self):
        try:
            return self.data['views']
        except KeyError:
            return None

    @property
    def plays(self):
        try:
            return self.data['plays']
        except KeyError:
            return None

def dict_to_item_list(item_type, input_dict, _id=None):
    """Takes a dictionary containing track data and returns a list of Item objects."""
    output = []
    for id, data in input_dict.items():
        if _id and not id == _id:
            continue
        output.append(Item(item_type, id, data))
    return output
