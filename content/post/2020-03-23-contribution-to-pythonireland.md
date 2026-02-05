---
modified: 2025-09-02T18:56:50+02:00
tags:
- contribution
- personal/travel
- python
ContentType: post
title: Contribution to Python Ireland
decription: Working on the sites of the previous editions
date: 2020-03-23T14:31:15.243000Z
image: /project/python-ireland/python-ireland.png
slug: contribution-to-pythonireland
Status: published
author:

---

# Contribution to Python Ireland
At the end of February, I was in Limerick to help the [Python Ireland](https://python.ie) team for the PyCon Limerick held there during the weekend of February 29th.

And because I wanted to help them, I have started to rewrite the web site of PyCon Limerick 2020. The current version of PyCon Limerick uses a Wordpress instance, I have no issues with the set up. But I prefer to work with a static site, and with some other members of the team, I have started to work on a static version with [Hugo](https://gohugo.io).

Of course, you can find the source code on <https://github.com/matrixise/pycon-limerick-2020>. 

Now, I am not really sure to use Hugo, I love the tool, but by looking at the existing sites, I have discovered they already use Jekyll for the previous editions of PyCon Ireland.

So, during the past week-end, I have downloaded the repository of PyCon 2019, and started to clean it. After a few minutes, I have seen that repository has several version of the same site. Edition 2017, 2018 and 2019. So, in this case, I have created the branches for each year and moved the commits in the right branch. Don't ask why all the versions were in the same repository, but the reason is just because GitHub has only one CNAME (ok, there were others solutions).

After that, I started to work on the build, and fortunately, 1. There is a docker image for Jekyll, 2. I can use it for the three versions.

So, you can start to read the result on <https://pyconie-2017.wirtel.be>, <https://pyconie-2018.wirtel.be> and <https://pyconie-2019.wirtel.be>

I will continue on these sites and will ask to the Python Ireland team to take a VPS and host them.

So, I am just happy because yesterday evening, I have published the full schedule of PyCon IE 2018, PyCon IE 2019 and I think to continue with a new version of PyCon Limerick 2020 with the same template.

In the future, I would like to use Hugo.

Have a nice day,

Stéphane