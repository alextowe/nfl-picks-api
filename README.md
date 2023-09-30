# Django REST API for weekly NFL picks.

This API stores user information, weekly matchups, groups for making picks, and the picks for each group. The endpoints are listed below. 

    /api/users
    /api/matchups
    /api/groups
    /api/picks



## /api/users 

The users endpoint contains information about each user. Users can view and edit their own information but can only view that of others. The email field is only shown for the user that it belongs to. Passwords can be updated but are not visible by anyone. 

The information stored for each user:

- **username** - public username
- **email** - email address for user
- **following** - list of other users the user follows 
- **description** - description for profile
- **profile image** - image for profile



## /api/matchups

This endpoint contains information about each weekly matchup. New matchups are pulled in every Wednesday by making a request to ESPN's API. The endpoint for it is listed below. It accesses the current weeks scoreboard and contains a list of every matchup that week. 

    https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard

When a matchup is created, a pick for each user in each group is also created. Scores are updated every 3 minutes, starting when the first matchup in a game day begins and ending 5 hours after the last matchup begins. When a matchup is completed, the winner is determined and picks for that matchup are updated to reflect if it was correct or not. The endpoint used is listed below. It contains information about each matchup for a given day. 

    https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=YYYYMMDD


The information stored for each matchup:

- **uid** - unique identifier 
- **name** - name of matchup
- **short_name** - short name for matchup 
- **week** - current week in season
- **year** - current year for season
- **home_team** - home team
- **away_team** - away team
- **home_score** - score for home team
- **away_score** - score for away team
- **date** - start date and time 
- **completed** - boolean field for active/completed game
- **winner** - winner of the matchup



## /api/groups

This endpoint contains information about each group. Any user can create a new group and add other users to that group. Users can only view the groups they belong to. When a new group is created, picks for each matchup are created for the owner of the group. Any time another user is added, more picks are created for that user. 

The information stored for each group:

- **title** - title of group
- **owner** - owner of group  
- **members** - members of the group (includes owner)
- **picks_for_group** - all picks for each member of the group



## /api/picks

This endpoint contains information about the picks for each user in a group. Users can see their own picks and the picks of other users in mutual groups. Picks are created for existing groups when new matchups are created. For new groups, picks are created for the owner and for each user added to that group. Pick outcomes are determined when a matchup is marked as completed.  

The information stored for each pick:

- **owner** - user making the selection
- **pick_group** - group for the pick
- **matchup** - matchup for the pick
- **selection** - selection made by the user
- **is_correct** - boolean field to determine if the pick is correct for not