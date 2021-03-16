---
title: "Use Automation for Site and CV"
description: "Automate the creation of your CV with Gitlab-CI and your site"
tags: ["hugo", "cv", "site", "automation", "gitlab", "gitlab-runner", "latex",
"html"]
date: 2019-06-21T14:00:00+02:00
---

# Use Automation for this site and my CV

## Introduction

During the last week, I have been contacted by a head hunter about a position
and the main question was "Do you have an updated Curriculum Vitae?"

Unfortunately, my answer was "no" sorry, I don't update my CV every day. And
during the week-end, I started to work on my CV, try to get the last version,
update it etc... In fact, you know, all these boring things ;-)

But I have a problem, I am a developer and normally I don't like to repeat me
for this kind of stuff. So, during the next weeks/months, I will work on my site
and the auto-generation of my CV.

The idea, generate the needed data for my CV since my web site, with all the
references, all the projects and my talks/conferences, etc...

I think, but not yet sure, I will use the [json-resume
format](https://jsonresume.org/) (based on json) for
the data and will parse it for the generation of my cv.pdf file, ditto for the
HTML version.

Currently, I have a personal Gitlab instance which hosts my web site and the cv,
I will merge them and when there is a enhancement I will publish it here on this
site. Since yesterday, my CV is automatically built via gitlab-runner and deploy
on my web site. For that, I use a docker image of latex.

```yaml
stages:
  - build
  - deploy

build:
  stage: build
  image: aergus/latex:latest

  script:
    - pdflatex StephaneWirtel.tex
    - pdflatex StephaneWirtel.tex

  artifacts:
    paths:
      - StephaneWirtel.pdf
    expire_in: 1 week
    
deploy:
  stage: deploy

  image: alpine:latest

  dependencies:
    - build

  script:
    - apk add rsync openssh-client
    - eval $(ssh-agent -s)
    - echo "$SSH_PRIVATE_KEY" | tr -d '\r' | ssh-add - > /dev/null
    - mkdir -p ~/.ssh
    - echo "${SSH_HOST_KEY}" > $HOME/.ssh/known_hosts
    - echo -e "Host * \n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config
    - rsync -hrvz --chown=www-data:www-data --exclude=_ -e 'ssh -i id_rsa' StephaneWirtel.pdf ${SSH_USER}@${SSH_HOST}:${SSH_PATH}
```

Maybe it's not perfect, but at least, it works fine!

Of course, I think I will update the theme of the site etc....

In fact, I am a developer and I need to prove it and because I like automation
and DevOps, in fact, the Best Practices, I want to apply them for myself.

For the curious, you can find my [CV](/StephaneWirtel.pdf) at this address.

Have a nice day,

Stéphane
