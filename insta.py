import instaloader


def get_latest_post(username):
    l = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(l.context, username)
    latest_post = next(profile.get_posts())
    return latest_post


def get_latest_posts(username, number_of_posts):
    l = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(l.context, username)
    posts = profile.get_posts()
    latest_posts = []
    for i in range(number_of_posts):
        post = next(posts)
        latest_posts.append(post)
    return latest_posts