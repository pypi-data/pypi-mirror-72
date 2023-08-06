# get-pypi-statistics

Get statistics of pypi.org. How many projects, how many releases, how many files and how many users?

## Install

```shell
pip install get-pypi-statistics
```

## Usage

```shell
C:\Code\get-pypi-statistics>get-pypi-statistics
Usage: get-pypi-statistics [OPTIONS] COMMAND [ARGS]...

  Get statistics of pypi.org. How many projects, how many releases, how many
  files and how many users?

Options:
  --help  Show this message and exit.

Commands:
  all       Get how many projects, release, files and users on pypi.org.
  files     Get how many files on pypi.org.
  projects  Get how many projects on pypi.org.
  releases  Get how many releases on pypi.org.
  users     Get how many users on pypi.org.
```

## Example

```shell
C:\Code\get-pypi-statistics>get-pypi-statistics all
     207114 projects
    1563853 releases
    2338758 files
     388982 users


C:\Code\get-pypi-statistics>get-pypi-statistics projects
207114

C:\Code\get-pypi-statistics>get-pypi-statistics releases
1563854

C:\Code\get-pypi-statistics>get-pypi-statistics files
2338760

C:\Code\get-pypi-statistics>get-pypi-statistics users
388982
```

## Bug Reports

Please report any issues at https://github.com/zencore-cn/zencore-issues.

## Releases

### v0.1.1 2020/06/28

- Fix problem in extracting real data. Thanks to @Bob Hancock for reporting the issue.

### v0.1.0 2019/12/01

- First release
- Get statistics of projects, releases, files and users.
