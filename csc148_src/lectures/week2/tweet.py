from datetime import date


class Tweet:
    """
    A tweet

    === Attributes ===
    content: the content of this tweet.
    author: the id of the user who wrote this tweet
    created_at: the date the tweet was written
    likes: the number of likes this tweet has received.

    ===Representational Invariants===
    - self.likes >= 0
    - len(self.content) <= 140
    - self.created_at <= date(2006, 3, 21)
    """

    # Attribute types
    contents: str
    author: str
    created_at: date
    likes: int

    def __init__(self, contents: str, author: str, created_at: date, likes: int = 0) -> None:
        self.contents = contents[:140] # truncate at 140.
        self.author = author
        self.created_at = created_at
        self.likes = likes

    def like(self, n: int) -> None:
        """
        Record the fact that this tweet receives <n> likes.
        :param n:
        :return:
        """
        pass

if __name__ == '__main__':
    d = date(2017, 9, 18)
    t = Tweet("Hello World", "David", d)
    print(t.created_at)
