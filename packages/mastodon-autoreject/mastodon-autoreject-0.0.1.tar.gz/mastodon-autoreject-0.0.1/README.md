# autoreject

a tool to automatically reject follow requests for mastodon accounts

criteria:

- account age
- whether a bio has been set
- whether an account is a bot
- no profile picture set
- min/max followers count
- min/max follow count
- min/max post count

important to note: this tool will never *accept* a follow request. only reject based on these criteria.

## current working level

you can define criteria and reject via the API

## defining criteria

when providing criteria to the functions that accept it, you provide a dict with the criteria to reject on.

If you don't want to reject based on a certain criteria, simply exclude it from the dict.

| key           | value type         | description                                                                                                         |
|---------------|--------------------|---------------------------------------------------------------------------------------------------------------------|
| min_follows   | integer            | reject accounts who have fewer than this number of follows                                                          |
| min_followers | integer            | reject accounts who have fewer than this number of followers                                                        |
| max_follows   | integer            | reject accounts who have more than this number of follows                                                           |
| max_followers | integer            | reject accounts who have more than this number of followers                                                         |
| has_bio       | boolean            | if True, reject accounts if they do not have a bio defined. If False, reject accounts that *do* have a bio defined. |
| has_avatar    | boolean            | if True, reject accounts if they have a default avatar. If False, reject accounts that have a custom avatar set.    |
| min_posts     | integer            | reject accounts with fewer than this number of statuses/posts/toots/whatever                                        |
| max_posts     | integer            | reject accounts with more than this number of statuses/posts/toots/whatever                                         |
| min_age       | datetime.timedelta | reject accounts that are younger than the given timedelta duration                                                  |
| no_bots       | boolean            | if True, rejects accounts if they have the `bot` flag set. If False, reject accounts that are not bots.             |

here's an example

```python
criteria = {
    "min_follows": 10,
    "min_followers": 10,
    "max_follows": 100,
    "max_followers": 100,
    "has_bio": True,
    "has_avatar": True,
    "min_posts": 10,
    "max_posts": 100,
    "min_age": timedelta(days=7),
    "no_bots": True
}

# masto is a logged in instance of Mastodon.py, see here: https://mastodonpy.readthedocs.io/en/stable/#module-mastodon
masto = ... 

autoreject.reject_follows(masto, criteria) # will return a list of accounts that were rejected along with the reasons why
```