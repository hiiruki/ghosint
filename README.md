<div align="justify">

<div align="center">


```
   _____ _    _  ____   _____ _____ _   _ _______ 
  / ____| |  | |/ __ \ / ____|_   _| \ | |__   __|
 | |  __| |__| | |  | | (___   | | |  \| |  | |   
 | | |_ |  __  | |  | |\___ \  | | | . ` |  | |   
 | |__| | |  | | |__| |____) |_| |_| |\  |  | |   
  \_____|_|  |_|\____/|_____/|_____|_| \_|  |_|   

GitHub OSINT Tool

```

</div>

## INSTALLATION

``` bash
$ git clone https://github.com/hiiruki/ghosint
$ cd ghosint
$ pip3 install requests
```

> **Note**: GitHub API Token is required to use this tool. You can use the [Personal access tokens (classic)](https://github.com/settings/tokens) or  [Fine-grained personal access tokens (beta)](https://github.com/settings/tokens?type=beta).

Put your GitHub API Token in the (`"Authorization": "<YOUR_GITHUB_TOKEN>"`) at file [`ghosint.py` on line 26](https://github.com/hiiruki/ghosint/blob/main/ghosint.py#L26).

## USAGE

``` bash
$ python3 ghosint.py
```

## SCREENSHOT

![ghosint ss](https://user-images.githubusercontent.com/36108013/226153392-34c3ac19-6206-4ea0-9a57-7719edd02311.png)

## ISSUES & CONTRIBUTING

> **Note**: Please make sure to read the full guidelines. Your issue may be closed without warning if you do not.

<details><summary>Issues</summary>

**Before reporting a new issue, take a look at the already opened [issues](https://github.com/hiiruki/ghosint/issues).**

</details>

<details><summary>Contributing</summary>

See [CONTRIBUTING.md](./CONTRIBUTING.md).
</details>

<details><summary>Code of Conduct</summary>

See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
</details>

## LICENSE

This software is licensed under the terms of the [MIT License](./LICENSE.md).
