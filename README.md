# CMStuff
Useful stuff for the CMSocial coding platform.
### Contents: ###
* [CMScarica](#cmscarica)
* [CMScaricasingle](#cmscaricasingle)
* [CMSdiff](#cmsdiff)

## CMScarica
this script allows you to download all the fastest solutions for the problems an user solved.

input:
* username
* password
* directory

username and password are needed for the authentication in order to download the files.

directory is the directory you want the program to download the solutions in.

The first line of output will contain information about the number of files the script is about to download.

In each of the next lines information about what file is currently being downloaded is displayed.

note: this script does not download partial solutions.

## CMScaricasingle
this script allows you to download the fastest solution for a specific problem a user solved.

input:
* username
* password
* problem

username and password are needed for the authentication in order to download the file.

problem is the name of the problem one wants to download.

## CMSdiff
this script allows you to quickly view the difference between two users' solved problems sets.

input:
* user1
* user2

user1 and user2 are the usernames of the users you want to see the diff for.

output:
* in the first part the list of problem user1 solved and user2 didn't is displayed.
* in the second part the list of problem user2 solved and user1 didn't is displayed.
