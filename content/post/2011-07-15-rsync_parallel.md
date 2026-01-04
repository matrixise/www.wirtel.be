---
date: 2011-07-15
tags:
- parallel
- pg_dump
- backup
- postgresql
title: "PostgreSQL: Use GNU/Parallel and pg_dump"
slug: rsync_parallel

---

# How to use GNU/Parallel and pg_dump ?

I work with the [PostgreSQL database server](http://www.postgresql.org)
and for the backup process, I use the
[pg_dump](http://www.postgresql.org/docs/8.4/static/app-pgdump.html)
utility.

If you have many databases, you know there is a problem with this tool.
In fact, it's a serial process, it saves database after another and if
you have a big one, you risk to wait for longtime. In my situation, this
is problematic and I looked to use an other tool to parallelize the
process.

But I discovered the tool
[GNU/Parallel](http://www.gnu.org/s/parallel/).

GNU/Parallel is a shell tool for executing jobs in parallel using one or
more computers.

- [Site](http://www.gnu.org/s/parallel/)
- [Download](http://ftp.gnu.org/gnu/parallel/parallel-20110722.tar.bz2)
- [Documentation](http://www.gnu.org/s/parallel/man.html)

## Installation

```bash
wget http://ftp.gnu.org/gnu/parallel/parallel-20110722.tar.bz2
tar xfj parallel-20110722.tar.bz2
cd parallel-20110722
./configure --prefix=/opt/local
make
make install
```

# The Script

```sql
#!/usr/bin/env bash
# Path to the GNU/Parallel tool
PARALLEL=/opt/local/bin/parallel

# We select all the databases we want to backup except the 'template0', 
# 'template1' and 'postgres' databases
INPUTLIST=`psql -d postgres -A -t <<EOF
    SELECT datname FROM pg_database 
    WHERE datname NOT IN ('template0','template1','postgres')
    ORDER BY datname ASC;
EOF`

# And we call the parallel tool with the right arguments
CMD='pg_dump --no-owner {} | gzip -9 > ${OUTPUT_DIR}/{}.dump.sql.gz'
(echo "$INPUTLIST") | $PARALLEL "$CMD"
```

If you have an other solution to this problem, I'm interrested

In a future post, I will show you how to use
[GNU/Parallel](http://www.gnu.org/s/parallel/) and rsnapshot to
parallelize the rsync tool.