""" all filters and the data types of their input """
# used with get_mentions() in queries/groups and with filters in rules
params = {
    "author": str,
    "xauthor": str,
    "exactAuthor": str,
    "xexactAuthor": str,
    "authorGroup": list,  # user passes in a string which gets converted to a list of ids
    "xauthorGroup": list,  # user passes in a string which gets converted to a list of ids
    "category": list,
    # user passes in a dictionary {parent:[child1, child2, etc]} which gets converted to a list of ids
    "xcategory": list,
    # user passes in a dictionary {parent:[child, child2, etc]} which gets converted to a list of ids
    "parentCategory": list,  # user passes in a string which gets converted to a list of ids
    "xparentCategory": list,  # user passes in a string which gets converted to a list of ids
    "facebookAuthorId": int,
    "xfacebookAuthorId": int,
    "facebookRole": str,
    "xfacebookRole": str,
    "facebookSubtype": str,
    "xfacebookSubtype": str,
    "facebookCommentsMin": int,
    "facebookCommentsMax": int,
    "facebookLikesMin": int,
    "facebookLikesMax": int,
    "facebookSharesMin": int,
    "facebookSharesMax": int,
    "resourceType": str,
    "xresourceType": str,
    "impactMin": int,
    "impactMax": int,
    "instagramFollowersMax": int,
    "instagramFollowersMin": int,
    "instagramFollowingMax": int,
    "instagramFollowingMin": int,
    "instagramPostsMax": int,
    "instagramPostsMin": int,
    "instagramLikesMax": int,
    "instagramLikesMin": int,
    "instagramCommentsMax": int,
    "instagramCommentsMin": int,
    "instagramInteractionsMax": int,
    "instagramInteractionsMin": int,
    "language": str,
    "xlanguage": str,
    "locationGroup": list,  # user passes in a string which gets converted to a list of ids
    "xlocationGroup": list,  # user passes in a string which gets converted to a list of ids
    "location": str,
    "xlocation": str,
    "starred": bool,
    "search": str,
    "pageType": (str, list),
    "xpageType": (str, list),
    "sentiment": str,
    "siteGroup": list,  # user passes in a string which gets converted to a list of ids
    "xsiteGroup": list,  # user passes in a string which gets converted to a list of ids
    "domain": str,
    "xdomain": str,
    "monthlyVisitorsMin": int,
    "monthlyVisitorsMax": int,
    "tag": list,  # user passes in a string which gets converted to a list of ids
    "xtag": list,  # user passes in a string which gets converted to a list of ids
    "twitterFollowersMin": int,
    "twitterFollowersMax": int,
    "twitterFollowingMin": int,
    "twitterFollowingMax": int,
    "twitterReplyTo": str,
    "xtwitterReplyTo": str,
    "twitterRetweetOf": str,
    "xtwitterRetweetOf": str,
    "twitterPostCountMin": int,
    "twitterPostCountMax": int,
    "twitterRetweetsMin": int,
    "twitterRetweetsMax": int,
    "reachEstimateMin": int,
    "reachEstimateMax": int,
    "twitterVerified": bool,
    "twitterRole": str,
    "twitterAuthorId": int,
    "xtwitterAuthorId": int,
    "impressionsMin": int,
    "impressionsMax": int,
    "gender": str,
    "accountType": (str, list),  # one or more filters
    "profession": (str, list),  # one or more filters
    "xprofession": (str, list),  # one or more filters
    "interest": (str, list),  # one or more filters
    "xinterest": (str, list),  # one or more filters
    "geolocated": bool,
    "latitudeMin": int,
    "latitudeMax": int,
    "longitudeMin": int,
    "longitudeMax": int,
    "status": str,
    "xstatus": str,
    "priority": str,
    "xpriority": str,
    "checked": bool,
    "assigned": str,
    "xassigned": str,
    "threadId": int,
    "xthreadId": int,
    "threadEntryType": str,
    "xthreadEntryType": str,
    "threadAuthor": str,
    "xthreadAuthor": str,
    "postByAuthor": str,
    "xpostByAuthor": str,
    "shareOfAuthor": str,
    "xshareOfAuthor": str,
    "replyToAuthor": str,
    "xreplyToAuthor": str,
    "insightsEmoticon": str,
    "xinsightsEmoticon": str,
    "insightsHashtag": str,
    "xinsightsHashtag": str,
    "insightsMentioned": str,
    "xinsightsMentioned": str,
    "insightsUrl": str,
    "xinsightsUrl": str,
    "exclusiveLocation": str,
    "hourOfDay": str,
    "dayOfWeek": str,
    "untilAssignmentUpdated": str,
    "sinceAssignmentUpdated": str,
}

""" filters which are limited to a set of options """
special_options = {
    "sentiment": ["positive", "negative", "neutral"],
    "gender": ["male", "female"],
    "status": ["open", "pending", "closed"],
    "xstatus": ["open", "pending", "closed"],
    "priority": ["high", "medium", "low"],
    "xpriority": ["high", "medium", "low"],
    "facebookRole": ["owner", "audience"],
    "xfacebookRole": ["owner", "audience"],
    "facebookSubtype": ["link", "other", "photo", "status", "video"],
    "xfacebookSubtype": ["link", "other", "photo", "status", "video"],
    "resourceType": ["public-facebook-post", "public-facebook-comment"],
    "xresourceType": ["public-facebook-post", "public-facebook-comment"],
    "pageType": [
        "blog",
        "forum",
        "news",
        "twitter",
        "review",
        "instagram",
        "facebook",
        "qq",
        "reddit",
        "tumblr",
        "vk",
        "youtube",
        "lexis_nexis_licensed_news",
        "dark_web",
        "sina_weibo",
        "four_chan",
    ],
    "xpageType": [
        "blog",
        "forum",
        "news",
        "twitter",
        "review",
        "instagram",
        "facebook",
        "qq",
        "reddit",
        "tumblr",
        "vk",
        "youtube",
        "lexis_nexis_licensed_news",
        "dark_web",
        "sina_weibo",
        "four_chan",
    ],
    "accountType": ["individual", "organizational"],
    "xaccountType": ["individual", "organizational"],
    "profession": [
        "Executive",
        "Student",
        "Politician",
        "Artist",
        "Scientist & Researcher",
        "Journalist",
        "Software developer & IT",
        "Legal",
        "Health practitioner",
        "Sportpersons & Trainer",
        "Sales/Marketing/PR",
        "Teacher & Lecturer",
    ],
    "xprofession": [
        "Executive",
        "Student",
        "Politician",
        "Artist",
        "Scientist & Researcher",
        "Journalist",
        "Software developer & IT",
        "Legal",
        "Health practitioner",
        "Sportpersons & Trainer",
        "Sales/Marketing/PR",
        "Teacher & Lecturer",
    ],
    "interest": [
        "Animals & Pets",
        "Fine arts",
        "Automotive",
        "Beauty/Health & Fitness",
        "Books",
        "Business",
        "Environment",
        "Family & Parenting",
        "Fashion",
        "Movies",
        "Food & Drinks",
        "Games",
        "Music",
        "Photo & Video",
        "Politics",
        "Science",
        "Shopping",
        "Sports",
        "Technology",
        "Travel",
        "TV",
    ],
    "xinterest": [
        "Animals & Pets",
        "Fine arts",
        "Automotive",
        "Beauty/Health & Fitness",
        "Books",
        "Business",
        "Environment",
        "Family & Parenting",
        "Fashion",
        "Movies",
        "Food & Drinks",
        "Games",
        "Music",
        "Photo & Video",
        "Politics",
        "Science",
        "Shopping",
        "Sports",
        "Technology",
        "Travel",
        "TV",
    ],
}

""" mention attribultes which can be changed """
# used with patch_mentions() in queries/groups and with uploads in rules
mutable = {
    "addTag": list,
    "removeTag": list,
    "addCategories": list,
    "removeCategories": list,
    "priority": str,
    "removePriority": str,
    "status": str,
    "removeStatus": str,
    "assignment": str,
    "removeAssignment": str,
    "sentiment": str,
    "checked": bool,
    "starred": bool,
    "location": str,
}

mutable_options = {
    "sentiment": ["positive", "negative", "neutral"],
    "status": ["open", "pending", "closed"],
    "removeStatus": ["open", "pending", "closed"],
    "priority": ["high", "medium", "low"],
    "removePriority": ["high", "medium", "low"],
}
